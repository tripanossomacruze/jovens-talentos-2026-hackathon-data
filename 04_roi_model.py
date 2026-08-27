"""
Etapa 4 - Modelo financeiro detalhado de ROI para o apartamento recomendado
(2 quartos, bairro Morretes, Itapema-SC)

Premissas de mercado (pesquisadas via web, com fonte documentada no relatório):
- ITBI Itapema: 1,5%
- Escritura + registro: ~2,0% (ponto médio da faixa 1-2%)
- Mobília/decoração completa para temporada (2 quartos, ~69m²): R$ 35.000 (ponto médio 30-45k)
- Limpeza por virada de hóspede: R$ 190 (ponto médio 180-200)
- Estadia média por reserva: 4 noites (premissa padrão do setor para litoral, não medida diretamente na base)
- Taxa de gestão terceirizada tipo Seazone: 25% da receita bruta (ponto médio 20-30%)
- Taxa Airbnb host-only (gestoras profissionais/API): 15% | modelo split-fee (autogestão via app): 4%
- Reserva de manutenção: 5% da receita bruta (heurística padrão do setor imobiliário)
- IR PJ Simples Nacional Anexo III: 6% da receita bruta (faixa até R$180k/ano)
- Financiamento SFH (Caixa, imóvel financiado): TR + 11,2% a.a. (ponto médio 10,99-11,49%),
  entrada de 30% (premissa conservadora para 2º imóvel/investimento), SAC 20 anos
"""
import pandas as pd
import numpy as np

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# ---------- Dados-base do segmento (saída da Etapa 3) ----------
PRECO = 750_000.0
AREA_M2 = 69.0
RECEITA_BRUTA_ANO = 59_778.03   # rev_ano_med, Morretes 2Q
CONDO_IPTU_ANO = 4800.0  # real: condominio R$350/mes (med valida) + IPTU R$600/ano (round 2)
ADR_MEDIANO = 454.76
OCC_MEDIANA = 0.3846
NOITES_OCUPADAS_ANO = OCC_MEDIANA * 365

# ---------- Premissas de custo (pesquisa de mercado) ----------
ITBI_PCT = 0.015
ESCRITURA_REGISTRO_PCT = 0.02
CUSTO_TRANSACAO_PCT = ITBI_PCT + ESCRITURA_REGISTRO_PCT  # 3,5%
MOBILIA = 35_000.0
CUSTO_LIMPEZA_UNIT = 190.0
ESTADIA_MEDIA_NOITES = 4
N_TURNOVERS_ANO = NOITES_OCUPADAS_ANO / ESTADIA_MEDIA_NOITES
CUSTO_LIMPEZA_ANO = N_TURNOVERS_ANO * CUSTO_LIMPEZA_UNIT

TAXA_GESTORA_PCT = 0.25
TAXA_AIRBNB_HOSTONLY_PCT = 0.15   # usado quando há gestora profissional (API)
TAXA_AIRBNB_SPLITFEE_PCT = 0.04   # usado em autogestão via app
RESERVA_MANUTENCAO_PCT = 0.05
IR_PJ_SIMPLES_PCT = 0.06

# Financiamento
ENTRADA_PCT = 0.30
TAXA_FINANC_ANO = 0.112
PRAZO_ANOS = 20

capital_transacao = PRECO * CUSTO_TRANSACAO_PCT
capital_total_avista = PRECO + capital_transacao + MOBILIA

print("=" * 70)
print("CAPEX - capital necessário (compra à vista)")
print("=" * 70)
print(f"Preço do imóvel:                 R$ {PRECO:>12,.2f}")
print(f"Custos de transação (ITBI+cart.): R$ {capital_transacao:>12,.2f}  ({CUSTO_TRANSACAO_PCT*100:.1f}%)")
print(f"Mobília/decoração p/ temporada:   R$ {MOBILIA:>12,.2f}")
print(f"TOTAL investido (à vista):        R$ {capital_total_avista:>12,.2f}")
print(f"\nNoites ocupadas/ano (proxy):      {NOITES_OCUPADAS_ANO:.0f}")
print(f"Turnovers estimados/ano (÷{ESTADIA_MEDIA_NOITES} noites/estadia): {N_TURNOVERS_ANO:.1f}")
print(f"Custo de limpeza anual estimado:  R$ {CUSTO_LIMPEZA_ANO:>12,.2f}")


def cenario(nome, taxa_gestora, taxa_airbnb):
    receita_bruta = RECEITA_BRUTA_ANO
    custo_gestora = receita_bruta * taxa_gestora
    custo_airbnb = receita_bruta * taxa_airbnb
    custo_limpeza = CUSTO_LIMPEZA_ANO
    custo_condo_iptu = CONDO_IPTU_ANO
    reserva_manut = receita_bruta * RESERVA_MANUTENCAO_PCT
    ir = receita_bruta * IR_PJ_SIMPLES_PCT

    custos_totais = custo_gestora + custo_airbnb + custo_limpeza + custo_condo_iptu + reserva_manut + ir
    noi = receita_bruta - custos_totais  # net operating income (antes de financiamento)

    return {
        "cenario": nome,
        "receita_bruta": receita_bruta,
        "custo_gestora": custo_gestora,
        "custo_airbnb": custo_airbnb,
        "custo_limpeza": custo_limpeza,
        "custo_condo_iptu": custo_condo_iptu,
        "reserva_manutencao": reserva_manut,
        "ir_pj_simples": ir,
        "custos_totais": custos_totais,
        "noi": noi,
        "noi_margem_pct": noi / receita_bruta * 100,
    }


cA = cenario("A - Autogestão (split-fee Airbnb, sem gestora)", 0.0, TAXA_AIRBNB_SPLITFEE_PCT)
cB = cenario("B - Gestão terceirizada tipo Seazone (host-only fee)", TAXA_GESTORA_PCT, TAXA_AIRBNB_HOSTONLY_PCT)

print("\n" + "=" * 70)
print("DRE OPERACIONAL ANUAL - por cenário de gestão")
print("=" * 70)
dre = pd.DataFrame([cA, cB]).set_index("cenario").T
print(dre)

print("\n" + "=" * 70)
print("RETORNO - COMPRA À VISTA (sem financiamento)")
print("=" * 70)
for c in (cA, cB):
    yield_liq = c["noi"] / capital_total_avista * 100
    payback = capital_total_avista / c["noi"]
    print(f"\n[{c['cenario']}]")
    print(f"  NOI anual:               R$ {c['noi']:>12,.2f}  (margem {c['noi_margem_pct']:.1f}% da receita bruta)")
    print(f"  Capital investido:       R$ {capital_total_avista:>12,.2f}")
    print(f"  Yield líquido (cash-on-cash, à vista): {yield_liq:.1f}% a.a.")
    print(f"  Payback simples:         {payback:.1f} anos")

# ---------- Financiamento SAC ----------
print("\n" + "=" * 70)
print("RETORNO - COMPRA FINANCIADA (SFH, SAC, entrada 30%, 20 anos, TR+11,2% a.a.)")
print("=" * 70)

entrada = PRECO * ENTRADA_PCT
principal_financiado = PRECO * (1 - ENTRADA_PCT)
capital_investido_financ = entrada + capital_transacao + MOBILIA

n_meses = PRAZO_ANOS * 12
taxa_mensal = (1 + TAXA_FINANC_ANO) ** (1 / 12) - 1
amortizacao_mensal = principal_financiado / n_meses

saldo = principal_financiado
juros_ano1 = 0.0
amort_ano1 = 0.0
for m in range(12):
    juros_mes = saldo * taxa_mensal
    juros_ano1 += juros_mes
    saldo -= amortizacao_mensal
    amort_ano1 += amortizacao_mensal

servico_divida_ano1 = juros_ano1 + amort_ano1

print(f"Entrada (30%):                    R$ {entrada:>12,.2f}")
print(f"Principal financiado:              R$ {principal_financiado:>12,.2f}")
print(f"Capital investido (financiado):    R$ {capital_investido_financ:>12,.2f}")
print(f"Amortização SAC (ano 1):           R$ {amort_ano1:>12,.2f}")
print(f"Juros (ano 1):                     R$ {juros_ano1:>12,.2f}")
print(f"Serviço da dívida total (ano 1):   R$ {servico_divida_ano1:>12,.2f}")

for c in (cA, cB):
    fluxo_ano1 = c["noi"] - servico_divida_ano1
    coc = fluxo_ano1 / capital_investido_financ * 100
    print(f"\n[{c['cenario']}]")
    print(f"  NOI anual:                       R$ {c['noi']:>12,.2f}")
    print(f"  (-) Serviço da dívida ano 1:      R$ {servico_divida_ano1:>12,.2f}")
    print(f"  = Fluxo de caixa do investidor:   R$ {fluxo_ano1:>12,.2f}")
    print(f"  Cash-on-cash (financiado, ano 1): {coc:.1f}% a.a.")

print("\n" + "=" * 70)
print("COMPARATIVO: taxa de financiamento vs yield do imóvel")
print("=" * 70)
print(f"Taxa de financiamento:  {TAXA_FINANC_ANO*100:.1f}% a.a.")
print(f"Yield bruto do imóvel (NOI cenário B / preço): {cB['noi']/PRECO*100:.1f}% a.a.")
print("=> Quando a taxa de financiamento supera o yield do imóvel, a alavancagem")
print("   é NEGATIVA: financiar reduz o retorno em vez de ampliá-lo.")
