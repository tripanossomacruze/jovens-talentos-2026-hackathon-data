"""
Etapa 3 - Testar a tese "studio/1Q no Centro" + cruzar com VivaReal (custo de aquisição -> yield)
"""
import pandas as pd
import numpy as np
import os

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 220)
pd.set_option("display.float_format", lambda x: f"{x:,.1f}")

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
reliable = pd.read_csv(f"{BASE}/reliable_sample.csv")
df = pd.read_csv(f"{BASE}/listings_full.csv")
viva = pd.read_csv(f"{BASE}/vivareal.csv")

print("=== TESE: studio/1Q no Centro vs demais segmentos ===")
tese = reliable[reliable["listing_type"] == "apartamento"].groupby(
    ["suburb", "bedroom_bucket"]
).agg(
    n=("airbnb_listing_id", "count"),
    adr_med=("adr_proxy", "median"),
    occ_med=("occ_proxy", "median"),
    rev_mes_med=("revenue_month_proxy", "median"),
).reset_index().sort_values("rev_mes_med", ascending=False)
print(tese.to_string(index=False))

print("\n--- Centro studio/1Q especificamente ---")
centro_compact = reliable[(reliable["suburb"] == "Centro") &
                            (reliable["bedroom_bucket"].isin(["0 (studio)", "1"]))]
print("n =", len(centro_compact))
print(centro_compact[["adr_proxy", "occ_proxy", "revenue_month_proxy"]].describe())

print("\n--- Ranking geral de segmentos (suburb x bedroom_bucket), apartamento, n>=5 ---")
rank = tese.query("n >= 5").sort_values("rev_mes_med", ascending=False)
print(rank.to_string(index=False))

# posição do Centro-compacto no ranking geral
print("\nPosição do 'Centro / 0-1 quarto' no ranking (se existir com n>=5):")
print(rank[(rank["suburb"] == "Centro") & (rank["bedroom_bucket"].isin(["0 (studio)", "1"]))])

# ================= VIVAREAL: custo de aquisição =================
print("\n\n=== VIVAREAL: preço de venda por bairro (mediana, n>=10) ===")
# normaliza nomes de bairro (mesma grafia variando)
viva["suburb_norm"] = viva["suburb"].astype(str).str.strip().str.title()
fix_map = {
    "Meia Praia - Frente Mar": "Meia Praia",
    "Tabuleiro": "Tabuleiro Dos Oliveiras",
    "Taboleiro": "Tabuleiro Dos Oliveiras",
    "Sertão Do Trombudo": "Sertao Do Trombudo",
    "Alto São Bento": "Alto Sao Bento",
}
viva["suburb_norm"] = viva["suburb_norm"].replace(fix_map)

viva["bedroom_bucket"] = viva["bedrooms"].apply(lambda n: "0 (studio)" if n == 0 else ("4+" if n >= 4 else str(int(n))))
viva["price_per_m2"] = viva["sale_price"] / viva["usable_area"].replace(0, np.nan)

# ---- Correcao (round 2): condominio e IPTU tem placeholders na base (0, 1, e
# valores triviais) que distorcem a mediana. Limpamos antes de agregar ----
def clean_monetary(s, min_val):
    num = pd.to_numeric(s, errors="coerce")
    return num.where(num > min_val)

viva["condo_ok"] = clean_monetary(viva["monthly_condo_fee"], min_val=30)
viva["iptu_ok"] = clean_monetary(viva["yearly_iptu"], min_val=50)

gv = viva[viva["business_types"] == "Venda"].groupby(["suburb_norm", "bedroom_bucket"]).agg(
    n=("listing_id", "count"),
    preco_med=("sale_price", "median"),
    preco_m2_med=("price_per_m2", "median"),
    area_med=("usable_area", "median"),
    condo_med=("condo_ok", "median"),
    iptu_med=("iptu_ok", "median"),
    n_condo_validos=("condo_ok", "count"),
    n_iptu_validos=("iptu_ok", "count"),
).query("n >= 5").sort_values(["suburb_norm", "bedroom_bucket"])
print(gv.to_string())

gv.to_csv(f"{BASE}/vivareal_by_segment.csv")
rank.to_csv(f"{BASE}/revenue_rank_by_segment.csv", index=False)

# ================= CRUZAMENTO: yield estimado =================
print("\n\n=== YIELD ESTIMADO (receita anual proxy / preço mediano de compra) por segmento ===")
rev_seg = reliable[reliable["listing_type"] == "apartamento"].groupby(
    ["suburb", "bedroom_bucket"]
).agg(
    n_airbnb=("airbnb_listing_id", "count"),
    rev_ano_med=("revenue_year_proxy", "median"),
).reset_index()

merged = rev_seg.merge(
    gv.reset_index().rename(columns={"suburb_norm": "suburb"}),
    on=["suburb", "bedroom_bucket"], how="inner"
)
merged["yield_bruto_pct"] = (merged["rev_ano_med"] / merged["preco_med"]) * 100
merged["custos_anuais"] = merged["condo_med"].fillna(0) * 12 + merged["iptu_med"].fillna(0)
merged["rev_liquida_ano"] = merged["rev_ano_med"] - merged["custos_anuais"]
merged["yield_liquido_pct"] = (merged["rev_liquida_ano"] / merged["preco_med"]) * 100
merged["payback_anos"] = merged["preco_med"] / merged["rev_liquida_ano"]
merged = merged.sort_values("yield_liquido_pct", ascending=False)
print(merged[["suburb", "bedroom_bucket", "n_airbnb", "n", "rev_ano_med", "preco_med",
              "preco_m2_med", "custos_anuais", "yield_bruto_pct", "yield_liquido_pct", "payback_anos"]].to_string(index=False))

merged.to_csv(f"{BASE}/yield_by_segment.csv", index=False)
