"""
Etapa 1 - Construção do dataset analítico (listing-level)
Une Details + Mesh (bairro) + Hosts (perfil do anfitrião) + Price_AV
(proxy de ADR e ocupação a partir do calendário de preços futuros).
"""
import pandas as pd
import numpy as np
import os

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 220)

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

details = pd.read_csv(f"{BASE}/details.csv")
hosts = pd.read_csv(f"{BASE}/hosts.csv")
mesh = pd.read_csv(f"{BASE}/mesh.csv")
price = pd.read_csv(f"{BASE}/price.csv")

# --- Hosts: pode haver mais de um snapshot por owner_id; ficamos com o mais recente
hosts["host_snapshot_date"] = pd.to_datetime(hosts["host_snapshot_date"])
hosts_dedup = hosts.sort_values("host_snapshot_date").drop_duplicates("owner_id", keep="last")
print("hosts raw:", hosts.shape, "hosts dedup:", hosts_dedup.shape)

# --- Price_AV: proxy de ADR (preço médio anunciado) e ocupação
# Cada linha = preço anunciado para uma data futura de estadia, em uma data de captura.
# Ausência de uma data no calendário mais recente é o melhor proxy que temos de "já reservado/bloqueado".
price["date"] = pd.to_datetime(price["date"])
price["aquisition_date"] = pd.to_datetime(price["aquisition_date"])
price["snap_day"] = price["aquisition_date"].dt.date

# fica com o snapshot mais recente disponível por listing (maior aquisition_date)
last_snap = price.groupby("airbnb_listing_id")["aquisition_date"].transform("max")
price_last = price[price["aquisition_date"] == last_snap].copy()

def summarize(g):
    window_start = g["aquisition_date"].iloc[0].normalize()
    window_end = g["date"].max()
    window_days = (window_end - window_start).days + 1
    avail_days = g["date"].nunique()
    occ_proxy = 1 - (avail_days / window_days) if window_days > 0 else np.nan
    return pd.Series({
        "adr_proxy": g["price"].mean(),
        "median_price_proxy": g["price"].median(),
        "min_price_proxy": g["price"].min(),
        "max_price_proxy": g["price"].max(),
        "avail_days_scraped": avail_days,
        "window_days": window_days,
        "occ_proxy": np.clip(occ_proxy, 0, 1),
        "price_snapshot_date": window_start,
    })

price_agg = price_last.groupby("airbnb_listing_id").apply(summarize).reset_index()
price_agg["revenue_month_proxy"] = price_agg["adr_proxy"] * price_agg["occ_proxy"] * 30
price_agg["revenue_year_proxy"] = price_agg["revenue_month_proxy"] * 12

print("\nprice_agg shape:", price_agg.shape)
print(price_agg[["adr_proxy", "occ_proxy", "avail_days_scraped", "window_days", "revenue_month_proxy"]].describe())

# --- Merge principal
df = details.merge(mesh[["airbnb_listing_id", "suburb", "latitude", "longitude"]],
                    on="airbnb_listing_id", how="left", suffixes=("", "_mesh"))
df = df.merge(hosts_dedup, on="owner_id", how="left")
df = df.merge(price_agg, on="airbnb_listing_id", how="left")

df["has_price_data"] = df["adr_proxy"].notna()
print("\nTotal listings:", len(df))
print("Com dado de preço/ocupação:", df["has_price_data"].sum(),
      f"({df['has_price_data'].mean()*100:.1f}%)")

df.to_csv(f"{BASE}/listings_full.csv", index=False)
print("\nSalvo em listings_full.csv")
print(df["suburb"].value_counts(dropna=False))
