"""
Etapa 8 - REVISÃO CRÍTICA da recomendação (Morretes 2Q).
Objetivo: tentar DERRUBAR a própria conclusão. Se ela sobreviver, é robusta.
Testes:
  A) Comparabilidade do estoque Airbnb vs VivaReal em cada bairro (o yield cruza
     duas amostras diferentes - será que são o mesmo tipo de imóvel?)
  B) Distribuição do ADR de Morretes vs demais (ADR igual a Meia Praia é plausível?)
  C) Intervalo de confiança (bootstrap) da receita mediana por segmento
  D) Ranking alternativo: NOI ABSOLUTO em R$ (perspectiva Seazone-operador)
  E) Sensibilidade: e se a ocupação de Morretes estiver superestimada?
  F) Geografia: os imóveis de Morretes estão mesmo longe da praia? (dispersão)
"""
import pandas as pd
import numpy as np
import os

pd.set_option("display.float_format", lambda x: f"{x:,.1f}")
pd.set_option("display.width", 200)
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

df = pd.read_csv(f"{BASE}/listings_full.csv")
viva = pd.read_csv(f"{BASE}/vivareal.csv")
reliable = df[(df["has_price_data"]) & (df["window_days"] >= 60)].copy()

def bucket(n):
    if n == 0: return "0"
    if n >= 4: return "4+"
    return str(int(n))
reliable["bb"] = reliable["number_of_bedrooms"].apply(bucket)
viva["bb"] = viva["bedrooms"].apply(bucket)
viva["suburb_n"] = viva["suburb"].astype(str).str.strip().str.title().replace({
    "Meia Praia - Frente Mar": "Meia Praia"})
viva["ppm2"] = viva["sale_price"] / viva["usable_area"].replace(0, np.nan)

# round 2: limpar placeholders de condominio/IPTU antes da mediana
def clean_monetary(s, min_val):
    num = pd.to_numeric(s, errors="coerce")
    return num.where(num > min_val)
viva["condo_ok"] = clean_monetary(viva["monthly_condo_fee"], min_val=30)
viva["iptu_ok"] = clean_monetary(viva["yearly_iptu"], min_val=50)

print("="*80)
print("A) COMPARABILIDADE: área útil (m²) do estoque VivaReal 2Q por bairro")
print("   (se Morretes tem imóveis MENORES, o preço baixo pode ser só tamanho)")
print("="*80)
for b in ["Morretes", "Meia Praia", "Centro", "Casa Branca"]:
    s = viva[(viva["suburb_n"]==b) & (viva["bb"]=="2") & (viva["business_types"]=="Venda")]
    print(f"{b:14s} n={len(s):4d} | area med={s['usable_area'].median():.0f}m² | "
          f"preco med=R${s['sale_price'].median():,.0f} | R$/m² med={s['ppm2'].median():,.0f}")

print("\n" + "="*80)
print("B) ADR de Morretes 2Q vs Meia Praia 2Q - distribuição completa")
print("   (ADR igual, com Morretes 3km da praia, é suspeito - checar)")
print("="*80)
for b in ["Morretes", "Meia Praia", "Centro"]:
    s = reliable[(reliable["suburb"]==b) & (reliable["bb"]=="2") & (reliable["listing_type"]=="apartamento")]
    q = s["adr_proxy"].quantile([.1,.25,.5,.75,.9])
    print(f"{b:12s} n={len(s):3d} | p10={q[.1]:.0f} p25={q[.25]:.0f} p50={q[.5]:.0f} p75={q[.75]:.0f} p90={q[.9]:.0f}")

print("\n" + "="*80)
print("C) BOOTSTRAP: IC 95% da receita mensal mediana (Morretes 2Q vs pares)")
print("="*80)
rng = np.random.default_rng(42)
def boot_ci(x, n=2000):
    x = x.dropna().values
    if len(x) < 5: return (np.nan, np.nan)
    meds = [np.median(rng.choice(x, len(x), replace=True)) for _ in range(n)]
    return np.percentile(meds, 2.5), np.percentile(meds, 97.5)
for b in ["Morretes", "Meia Praia", "Centro", "Casa Branca"]:
    s = reliable[(reliable["suburb"]==b) & (reliable["bb"]=="2") & (reliable["listing_type"]=="apartamento")]
    lo, hi = boot_ci(s["revenue_month_proxy"])
    print(f"{b:14s} n={len(s):3d} | mediana=R${s['revenue_month_proxy'].median():,.0f} | IC95=[R${lo:,.0f}, R${hi:,.0f}]")

print("\n" + "="*80)
print("D) RANKING ALTERNATIVO: NOI ABSOLUTO em R$/ano (perspectiva OPERADOR)")
print("   Seazone ganha % sobre receita - imovel de receita alta rende mais fee")
print("="*80)
rev_seg = reliable[reliable["listing_type"]=="apartamento"].groupby(["suburb","bb"]).agg(
    n=("airbnb_listing_id","count"),
    rev_ano=("revenue_year_proxy","median")).reset_index()
gv = viva[viva["business_types"]=="Venda"].groupby(["suburb_n","bb"]).agg(
    nv=("listing_id","count"), preco=("sale_price","median"),
    condo=("condo_ok","median"), iptu=("iptu_ok","median")).reset_index().rename(columns={"suburb_n":"suburb"})
m = rev_seg.merge(gv, on=["suburb","bb"]).query("n>=10 and nv>=10").copy()
m["custos_ano"] = m["condo"].fillna(0)*12 + m["iptu"].fillna(0)
m["noi_ano"] = m["rev_ano"] - m["custos_ano"]
m["yield_liq"] = m["noi_ano"]/m["preco"]*100
print("\nPor NOI ABSOLUTO (R$/ano):")
print(m.sort_values("noi_ano", ascending=False)[["suburb","bb","n","rev_ano","preco","noi_ano","yield_liq"]].head(10).to_string(index=False))
print("\nPor YIELD (%):")
print(m.sort_values("yield_liq", ascending=False)[["suburb","bb","n","rev_ano","preco","noi_ano","yield_liq"]].head(10).to_string(index=False))

print("\n" + "="*80)
print("E) SENSIBILIDADE: e se a ocupação real de Morretes for menor que a proxy?")
print("   Recalcula yield de Morretes 2Q com haircuts de -10%, -20%, -30% na receita")
print("="*80)
morr = m[(m["suburb"]=="Morretes") & (m["bb"]=="2")].iloc[0]
for hc in [0, 0.10, 0.20, 0.30]:
    rev = morr["rev_ano"]*(1-hc)
    noi = rev - morr["custos_ano"]
    print(f"  haircut -{hc*100:.0f}%: receita=R${rev:,.0f} | yield bruto={noi/morr['preco']*100:.1f}%")

print("\n" + "="*80)
print("F) GEOGRAFIA: dispersão dos imóveis de Morretes (lat/long) - longe da praia?")
print("="*80)
# praia central aprox -27.093, -48.611 (orla). Meia Praia orla ~ -27.13, -48.60
morr_pts = reliable[(reliable["suburb"]=="Morretes") & (reliable["bb"]=="2")]
print(f"Morretes 2Q: lat[{morr_pts['latitude'].min():.4f},{morr_pts['latitude'].max():.4f}] "
      f"long[{morr_pts['longitude'].min():.4f},{morr_pts['longitude'].max():.4f}]")
print(f"  n com coord validas (!=0): {(morr_pts['latitude']!=0).sum()} de {len(morr_pts)}")
