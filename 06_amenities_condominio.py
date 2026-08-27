"""
Etapa 6 - Quais instalações DE CONDOMÍNIO (área comum) maximizam receita?
Controla por tamanho do imóvel (nº de quartos) para não confundir "prédio com
piscina" com "unidade pequena" (viés já detectado na Etapa 2/Q3).
"""
import pandas as pd
import numpy as np
import os
import re

pd.set_option("display.float_format", lambda x: f"{x:,.1f}")

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
df = pd.read_csv(f"{BASE}/listings_full.csv")
details_full = pd.read_csv(f"{BASE}/details.csv", usecols=["airbnb_listing_id", "amenities"])
df = df.merge(details_full, on="airbnb_listing_id", how="left", suffixes=("", "_dup"))
reliable = df[(df["has_price_data"]) & (df["window_days"] >= 60)].copy()

# --- instalações de CONDOMÍNIO (área comum do prédio, não da unidade) ---
condo_features = {
    "piscina": r"[Pp]iscina",
    "academia": r"[Aa]cademia|Gym|Fitness",
    "elevador": r"[Ee]levador",
    "salao_festas": r"[Ss]al[aã]o de festas|[Ss]al[aã]o de jogos",
    "playground": r"[Pp]layground|[Bb]rinquedoteca",
    "portaria_seguranca": r"[Pp]ortaria|[Ss]eguran[cç]a 24|[Cc]oncierge",
    "quadra": r"[Qq]uadra",
    "sauna": r"[Ss]auna",
    "espaco_gourmet": r"[Ee]spa[cç]o gourmet|[Cc]hurrasqueira",  # churrasqueira geralmente é da área comum do predio
    "coworking": r"[Cc]oworking|[Ee]spa[cç]o de trabalho",
    "vista_mar": r"[Vv]ista.{0,4}mar|[Ff]rente.{0,4}mar|[Pp][eé] na areia",
    "estacionamento": r"[Ee]stacionamento|[Vv]aga",
}

for name, pat in condo_features.items():
    reliable[name] = reliable["amenities"].fillna("").str.contains(pat, regex=True)

print("=" * 90)
print("PARTE 1 - Efeito bruto (sem controlar tamanho) - já sabemos que é confundido")
print("=" * 90)
rows = []
for name in condo_features:
    yes = reliable[reliable[name]]["revenue_month_proxy"]
    no = reliable[~reliable[name]]["revenue_month_proxy"]
    diff = (yes.median() / no.median() - 1) * 100 if no.median() else np.nan
    rows.append((name, len(yes), yes.median(), len(no), no.median(), diff))
res = pd.DataFrame(rows, columns=["instalacao", "n_com", "rev_med_com", "n_sem", "rev_med_sem", "diff_pct"])
print(res.sort_values("diff_pct", ascending=False).to_string(index=False))

print("\n" + "=" * 90)
print("PARTE 2 - Efeito CONTROLADO por tamanho (dentro do mesmo nº de quartos)")
print("=" * 90)
for bucket in ["1", "2", "3", "4+"]:
    sub = reliable[reliable["bedroom_bucket"] == bucket]
    if len(sub) < 15:
        continue
    print(f"\n--- Segmento: {bucket} quarto(s), n={len(sub)} ---")
    rows = []
    for name in condo_features:
        yes = sub[sub[name]]["revenue_month_proxy"]
        no = sub[~sub[name]]["revenue_month_proxy"]
        if len(yes) < 5 or len(no) < 5:
            continue
        diff = (yes.median() / no.median() - 1) * 100 if no.median() else np.nan
        rows.append((name, len(yes), yes.median(), len(no), no.median(), diff))
    if rows:
        r = pd.DataFrame(rows, columns=["instalacao", "n_com", "rev_med_com", "n_sem", "rev_med_sem", "diff_pct"])
        print(r.sort_values("diff_pct", ascending=False).to_string(index=False))

print("\n" + "=" * 90)
print("PARTE 3 - Regressão simples: receita ~ quartos + instalações (efeito isolado)")
print("=" * 90)
import numpy as np
X_cols = ["number_of_bedrooms"] + list(condo_features.keys())
X = reliable[X_cols].copy()
X["number_of_bedrooms"] = reliable["number_of_bedrooms"].clip(upper=5)
for c in condo_features:
    X[c] = X[c].astype(int)
y = np.log1p(reliable["revenue_month_proxy"])  # log para efeito percentual aproximado
X = X.assign(const=1)
# minimos quadrados via numpy (sem sklearn)
Xm = X.values.astype(float)
coef, *_ = np.linalg.lstsq(Xm, y.values, rcond=None)
coef_map = dict(zip(X.columns, coef))
print("Efeito percentual aproximado na receita, isolando o número de quartos (coef log-linear):")
for k in condo_features:
    pct = (np.exp(coef_map[k]) - 1) * 100
    print(f"  {k:20s}: {pct:+.1f}%")
print(f"  {'numero_quartos':20s}: {(np.exp(coef_map['number_of_bedrooms'])-1)*100:+.1f}% por quarto adicional")
