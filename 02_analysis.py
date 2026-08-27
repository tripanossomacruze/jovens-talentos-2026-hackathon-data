"""
Etapa 2 - Perfil ideal (Q1), Localização (Q2), Drivers (Q3), Tese studio/Centro
"""
import pandas as pd
import numpy as np
import os

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 220)
pd.set_option("display.float_format", lambda x: f"{x:,.1f}")

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
df = pd.read_csv(f"{BASE}/listings_full.csv")

# Amostra confiável: precisa ter dado de preço, janela de calendário >= 60 dias
reliable = df[(df["has_price_data"]) & (df["window_days"] >= 60)].copy()
print("Amostra confiável (window_days>=60):", len(reliable), "de", df["has_price_data"].sum(), "com dado de preço")

# bucket de quartos
def bedroom_bucket(n):
    if n == 0:
        return "0 (studio)"
    if n >= 4:
        return "4+"
    return str(int(n))

reliable["bedroom_bucket"] = reliable["number_of_bedrooms"].apply(bedroom_bucket)
df["bedroom_bucket"] = df["number_of_bedrooms"].apply(bedroom_bucket)

print("\n=== Q1: Perfil por listing_type ===")
g = reliable.groupby("listing_type").agg(
    n=("airbnb_listing_id", "count"),
    adr_med=("adr_proxy", "median"),
    occ_med=("occ_proxy", "median"),
    rev_mes_med=("revenue_month_proxy", "median"),
    rev_mes_mean=("revenue_month_proxy", "mean"),
).sort_values("rev_mes_med", ascending=False)
print(g)

print("\n=== Q1: Perfil por nº de quartos (bedroom_bucket) ===")
g2 = reliable.groupby("bedroom_bucket").agg(
    n=("airbnb_listing_id", "count"),
    adr_med=("adr_proxy", "median"),
    occ_med=("occ_proxy", "median"),
    rev_mes_med=("revenue_month_proxy", "median"),
).sort_values("rev_mes_med", ascending=False)
print(g2)

print("\n=== Q1: Cruzando listing_type x bedroom_bucket (apenas apartamento/casa, n>=8) ===")
g3 = reliable[reliable["listing_type"].isin(["apartamento", "casa"])].groupby(
    ["listing_type", "bedroom_bucket"]
).agg(
    n=("airbnb_listing_id", "count"),
    adr_med=("adr_proxy", "median"),
    occ_med=("occ_proxy", "median"),
    rev_mes_med=("revenue_month_proxy", "median"),
).query("n >= 8").sort_values("rev_mes_med", ascending=False)
print(g3)

print("\n=== Q2: Localização (suburb) - receita, n>=10 ===")
gloc = reliable.groupby("suburb").agg(
    n=("airbnb_listing_id", "count"),
    adr_med=("adr_proxy", "median"),
    occ_med=("occ_proxy", "median"),
    rev_mes_med=("revenue_month_proxy", "median"),
    rev_mes_p25=("revenue_month_proxy", lambda x: x.quantile(0.25)),
    rev_mes_p75=("revenue_month_proxy", lambda x: x.quantile(0.75)),
).query("n >= 10").sort_values("rev_mes_med", ascending=False)
print(gloc)

print("\n=== Contagem de oferta total por bairro (todos os 4441, não só amostra c/ preço) ===")
print(df["suburb"].value_counts())

# --- Q3: drivers de receita - correlação numérica
print("\n=== Q3: Correlação com revenue_month_proxy (amostra confiável) ===")
num_cols = ["revenue_month_proxy", "star_rating", "number_of_reviews", "guest_satisfaction_overall",
            "picture_count", "cleaning_fee", "number_of_bathrooms", "number_of_beds",
            "number_of_guests", "min_nights", "location_rating", "cleanliness_rating",
            "value_rating", "years_host", "number_of_reviews_host"]
corr = reliable[num_cols].corr(numeric_only=True)["revenue_month_proxy"].sort_values(ascending=False)
print(corr)

print("\n=== Q3: Superhost vs não-superhost ===")
print(reliable.groupby("is_superhost").agg(n=("airbnb_listing_id","count"),
                                             rev_med=("revenue_month_proxy","median"),
                                             occ_med=("occ_proxy","median")))

print("\n=== Q3: is_guest_favorite ===")
print(reliable.groupby("is_guest_favorite").agg(n=("airbnb_listing_id","count"),
                                                   rev_med=("revenue_month_proxy","median")))

print("\n=== Q3: can_instant_book ===")
print(reliable.groupby("can_instant_book").agg(n=("airbnb_listing_id","count"),
                                                  rev_med=("revenue_month_proxy","median")))

print("\n=== Q3: is_professional ===")
print(reliable.groupby("is_professional").agg(n=("airbnb_listing_id","count"),
                                                 rev_med=("revenue_month_proxy","median")))

# --- Distância até a praia mais próxima (proxy simples usando bounding aproximado)
# Praia central de Itapema ~ -27.0930, -48.6110 (aprox. região Centro / orla)
# calculamos distância euclidiana em graus só p/ ranquear (não é a métrica final do relatório)
reliable.to_csv(f"{BASE}/reliable_sample.csv", index=False)
df.to_csv(f"{BASE}/listings_full.csv", index=False)
print("\nSalvo reliable_sample.csv")
