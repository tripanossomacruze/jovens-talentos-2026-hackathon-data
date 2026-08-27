"""
Etapa 11 - Regenera os dois gráficos do relatório a partir das tabelas corrigidas
(round 2). Os dados vêm de reliable_sample.csv e yield_by_segment.csv.
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT, exist_ok=True)

rel = pd.read_csv(f"{BASE}/reliable_sample.csv")
yield_by = pd.read_csv(f"{BASE}/yield_by_segment.csv")

# --- Gráfico 1: receita mensal mediana por bairro (mesma agregação do relatório, n>=10) ---
g = rel.groupby("suburb")["revenue_month_proxy"]
gg = g.agg(n="count", med="median").query("n >= 10").sort_values("med", ascending=True)
fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(gg.index, gg["med"], color="#2a6f97")
for i, v in enumerate(gg["med"]):
    ax.text(v + 300, i, f"R${v:,.0f}", va="center", fontsize=9)
ax.set_title("Receita mensal mediana por bairro (Airbnb, Itapema)")
ax.set_xlabel("R$/mês (mediana)")
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT}/chart_revenue_by_suburb.png", dpi=120)
plt.close()

# --- Gráfico 2: yield líquido por segmento bairro x nº quartos (corrigido) ---
df = yield_by.sort_values("yield_liquido_pct", ascending=True).head(12)
label = df["suburb"] + " " + df["bedroom_bucket"]
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(label, df["yield_liquido_pct"], color="#b8860b")
for i, v in enumerate(df["yield_liquido_pct"]):
    ax.text(v + 0.1, i, f"{v:.1f}%", va="center", fontsize=8)
ax.set_title("Yield líquido (receita - condomínio/IPTU) / preço, por segmento")
ax.set_xlabel("Yield líquido anual (%)")
ax.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUT}/chart_yield_by_segment.png", dpi=120)
plt.close()

print("Charts regenerados em outputs/")
print(gg.to_string())