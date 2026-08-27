"""
Etapa 7 - Consolidação final: receita bruta revisada (ADR médio x ocupação média,
removendo outlier) + ROI final combinando os ajustes discutidos ao longo da análise
(custos operacionais reais, repasse de limpeza/taxa Airbnb ao hóspede, e a régua
simplificada usada para comparar com os números publicados pela Seazone).

Depende dos outputs de 01_build_dataset.py (listings_full.csv) e
03_thesis_and_vivareal.py (yield_by_segment.csv).
"""
import pandas as pd
import numpy as np
import os

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
df = pd.read_csv(f"{BASE}/listings_full.csv")

SUBURB, BEDROOM_BUCKET, LISTING_TYPE = "Morretes", "2", "apartamento"
seg = df[(df["suburb"] == SUBURB) & (df["bedroom_bucket"] == BEDROOM_BUCKET) &
         (df["listing_type"] == LISTING_TYPE) & (df["has_price_data"]) &
         (df["window_days"] >= 60)].copy()
print(f"Segmento: {SUBURB} / {BEDROOM_BUCKET} quarto(s) / {LISTING_TYPE} -- n={len(seg)}")

# ---------- 1) Receita bruta revisada: ADR médio x ocupação média, removendo outlier ----------
seg_sem_outlier = seg[seg["adr_proxy"] < 2000]  # remove 1 anúncio com preço implausível (R$10.000/noite)
adr_medio = seg_sem_outlier["adr_proxy"].mean()
occ_media = seg_sem_outlier["occ_proxy"].mean()
receita_bruta_revisada = adr_medio * occ_media * 365
receita_bruta_original = (seg["revenue_month_proxy"] * 12).median()

print(f"\nADR medio (sem outlier): R$ {adr_medio:,.2f}   Ocupacao media: {occ_media*100:.1f}%")
print(f"Receita bruta anual ORIGINAL (mediana por anuncio): R$ {receita_bruta_original:,.2f}")
print(f"Receita bruta anual REVISADA (media ADR x media occ): R$ {receita_bruta_revisada:,.2f}  "
      f"({(receita_bruta_revisada/receita_bruta_original-1)*100:+.1f}%)")

# ---------- 2) Parâmetros de custo (pesquisa de mercado, ver relatorio.md) ----------
PRECO = 750_000.0
ITBI_PCT, ESCRITURA_PCT = 0.015, 0.02
MOBILIA = 35_000.0
CAPITAL_AVISTA = PRECO * (1 + ITBI_PCT + ESCRITURA_PCT) + MOBILIA
CONDO_IPTU_ANO = 4800.0  # real: condominio R$350/mes + IPTU R$600/ano (round 2)
RESERVA_MANUT_PCT = 0.05
IR_PJ_SIMPLES_PCT = 0.06
CUSTO_LIMPEZA_UNIT, ESTADIA_MEDIA = 190.0, 4


def modelo(nome, receita, taxa_gestora, taxa_airbnb, repassar_limpeza=False):
    noites_ocupadas = receita / adr_medio if adr_medio else 0
    turnovers = noites_ocupadas / ESTADIA_MEDIA
    limpeza = 0.0 if repassar_limpeza else turnovers * CUSTO_LIMPEZA_UNIT
    gestora = receita * taxa_gestora
    airbnb = receita * taxa_airbnb
    reserva = receita * RESERVA_MANUT_PCT
    ir = receita * IR_PJ_SIMPLES_PCT
    custos = gestora + airbnb + limpeza + CONDO_IPTU_ANO + reserva + ir
    noi = receita - custos
    yld = noi / CAPITAL_AVISTA * 100
    payback = CAPITAL_AVISTA / noi if noi > 0 else float("inf")
    print(f"\n[{nome}]")
    print(f"  Receita bruta: R$ {receita:,.2f} | NOI: R$ {noi:,.2f} | "
          f"Yield: {yld:.2f}% a.a. | Payback: {payback:.1f} anos")
    return noi, yld, payback


print("\n" + "=" * 80)
print("RESUMO DE TODOS OS CENÁRIOS DE ROI DISCUTIDOS (autogestão, compra à vista)")
print("=" * 80)
modelo("V1 original - receita mediana, custos reais completos", receita_bruta_original, 0.0, 0.04)
modelo("V1 - receita revisada, custos reais completos", receita_bruta_revisada, 0.0, 0.04)
modelo("V2 - receita mediana, limpeza+Airbnb repassados ao hospede", receita_bruta_original, 0.0, 0.0, repassar_limpeza=True)
modelo("V2 - receita revisada, limpeza+Airbnb repassados ao hospede", receita_bruta_revisada, 0.0, 0.0, repassar_limpeza=True)

print("\n--- Régua 'estilo Seazone' (só desconta IR, sem custos operacionais) ---")
for label, receita in [("receita mediana", receita_bruta_original), ("receita revisada", receita_bruta_revisada)]:
    liq = receita * (1 - IR_PJ_SIMPLES_PCT)
    yld = liq / PRECO * 100
    print(f"  {label}: receita liquida de IR R$ {liq:,.2f} / preco do imovel = {yld:.2f}% a.a.")
