"""
Etapa 9 - A recomendação pode ser CONSTRUIR UM NOVO SPOT (modelo de negócio da Seazone),
não só comprar pronto. A métrica do incorporador é RECEITA POR M² CONSTRUÍDO
(o custo de construção por m² é aproximadamente fixo; quem maximiza receita/m² ganha).

Isso testa a tese interna sob outra ótica: "compacto" pode ser CERTO para um
incorporador (alta receita/m²) mesmo sendo ruim para quem compra pronto.
"""
import pandas as pd
import numpy as np
import os

pd.set_option("display.float_format", lambda x: f"{x:,.1f}")
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
df = pd.read_csv(f"{BASE}/listings_full.csv")
viva = pd.read_csv(f"{BASE}/vivareal.csv")
reliable = df[(df["has_price_data"]) & (df["window_days"] >= 60)].copy()

def bucket(n):
    if n == 0: return "0 studio"
    if n >= 4: return "4+"
    return str(int(n))
reliable["bb"] = reliable["number_of_bedrooms"].apply(bucket)
viva["bb"] = viva["bedrooms"].apply(bucket)
viva["suburb_n"] = viva["suburb"].astype(str).str.strip().str.title().replace({"Meia Praia - Frente Mar":"Meia Praia"})

# área mediana confiável por nº de quartos (VivaReal, filtrando áreas plausíveis p/ apto)
# studios reais ~ 20-45m²; o VivaReal tem "0 quartos" com 300m² (casas/terrenos mal rotulados) -> filtrar
apt = viva[(viva["business_types"]=="Venda") & (viva["property_type"]=="UNIT")].copy()
apt = apt[apt["usable_area"].between(18, 400)]

print("="*80)
print("Área mediana por nº de quartos (VivaReal apto, área 18-400m²)")
print("="*80)
area_by_bb = {}
for bb in ["0 studio","1","2","3","4+"]:
    s = apt[apt["bb"]==bb]
    # para studio, restringir a áreas <55m² (senão pega casa mal rotulada)
    if bb == "0 studio":
        s = s[s["usable_area"] < 55]
    med_area = s["usable_area"].median()
    area_by_bb[bb] = med_area
    print(f"  {bb:9s}: area med={med_area:.0f}m²  (n={len(s)})")

print("\n" + "="*80)
print("RECEITA POR M² CONSTRUÍDO (métrica do INCORPORADOR/SPOT)")
print("receita anual mediana Airbnb ÷ área mediana do tipo")
print("="*80)
rev_by_bb = reliable[reliable["listing_type"]=="apartamento"].groupby("bb")["revenue_year_proxy"].median()
rows = []
for bb in ["0 studio","1","2","3","4+"]:
    if bb in rev_by_bb.index and not np.isnan(area_by_bb.get(bb, np.nan)):
        rev = rev_by_bb[bb]
        area = area_by_bb[bb]
        rows.append((bb, rev, area, rev/area, rev/area/12))
r = pd.DataFrame(rows, columns=["quartos","rev_ano","area_m2","rev_m2_ano","rev_m2_mes"])
print(r.to_string(index=False))
print("\n>>> Quanto MAIOR a receita/m², melhor para um SPOT (custo de obra/m² ~ fixo)")

print("\n" + "="*80)
print("RECEITA/M² POR BAIRRO x TIPO COMPACTO (onde construir o SPOT compacto?)")
print("="*80)
for bb in ["1","2"]:
    print(f"\n-- {bb} quarto(s) --")
    sub = reliable[(reliable["listing_type"]=="apartamento") & (reliable["bb"]==bb)]
    g = sub.groupby("suburb")["revenue_year_proxy"].agg(["count","median"])
    g = g[g["count"]>=10]
    area = area_by_bb[bb]
    g["rev_m2_ano"] = g["median"]/area
    print(g.sort_values("rev_m2_ano", ascending=False).to_string())

print("\n" + "="*80)
print("VALIDAÇÃO DA TESE INTERNA sob a ótica do incorporador")
print("Studio no Centro tem dados? E qual bairro tem melhor receita/m² p/ compacto?")
print("="*80)
studio_data = reliable[(reliable["bb"]=="0 studio")]
print(f"Studios com dado de receita: {len(studio_data)} total")
print(studio_data.groupby("suburb")["revenue_year_proxy"].agg(["count","median"]).to_string())
