"""
Etapa 5 - ROI revisado: taxa de limpeza e taxa Airbnb tratadas como repasse ao hóspede
(pass-through), não como custo líquido do proprietário.

Racional do usuário: a taxa de limpeza é cobrada separadamente do hóspede (existe
como campo próprio `cleaning_fee` na base Details_Itapema.csv, mediana real de
R$ 250 no segmento Morretes/2Q/apartamento) e é repassada para pagar a diarista -
não sai do bolso do proprietário. A taxa do Airbnb, no modelo de "split-fee"
(padrão para anfitrião autônomo no Brasil), também é majoritariamente paga pelo
hóspede como "taxa de serviço" separada, não descontada do valor que o anfitrião recebe.
Logo, essas duas linhas de custo do modelo anterior (04_roi_model.py) são zeradas
(ou quase) no cálculo do NOI do proprietário.
"""
import pandas as pd

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

# ---------- Dados-base do segmento (Morretes, 2 quartos, apartamento) ----------
PRECO = 750_000.0
RECEITA_BRUTA_ANO = 59_778.03
CONDO_IPTU_ANO = 4800.0  # real: condominio R$350/mes (med valida) + IPTU R$600/ano (round 2)
CLEANING_FEE_MEDIANO_REAL = 250.0   # confirmado na própria base (Details_Itapema.csv), n=47

# custos de transação + mobília (mantidos do modelo anterior)
CUSTO_TRANSACAO_PCT = 0.015 + 0.02       # ITBI 1,5% + escritura/registro 2,0%
MOBILIA = 35_000.0
capital_transacao = PRECO * CUSTO_TRANSACAO_PCT
CAPITAL_AVISTA = PRECO + capital_transacao + MOBILIA

RESERVA_MANUTENCAO_PCT = 0.05
IR_PJ_SIMPLES_PCT = 0.06


def cenario_v2(nome, taxa_gestora, taxa_airbnb_residual, incluir_limpeza=False):
    """
    taxa_airbnb_residual: parte da taxa Airbnb que ainda fica com o anfitrião
       (0% = 100% repassada ao hóspede/split-fee integral;
        residual >0 cobre casos onde parte da taxa não é repassável, ex. gestão
        profissional via API que usa modelo host-only)
    incluir_limpeza: se True, mantém o custo de limpeza como no modelo v1 (para
       comparação); se False (novo cenário do usuário), a limpeza é 100% repassada
       ao hóspede via cleaning_fee e não entra como custo líquido do proprietário.
    """
    receita_bruta = RECEITA_BRUTA_ANO
    custo_gestora = receita_bruta * taxa_gestora
    custo_airbnb = receita_bruta * taxa_airbnb_residual
    custo_limpeza = 6_668.0 if incluir_limpeza else 0.0  # valor do modelo v1, p/ referência
    custo_condo_iptu = CONDO_IPTU_ANO
    reserva_manut = receita_bruta * RESERVA_MANUTENCAO_PCT
    ir = receita_bruta * IR_PJ_SIMPLES_PCT

    custos_totais = custo_gestora + custo_airbnb + custo_limpeza + custo_condo_iptu + reserva_manut + ir
    noi = receita_bruta - custos_totais

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
        "yield_avista_pct": noi / CAPITAL_AVISTA * 100,
        "payback_anos": CAPITAL_AVISTA / noi,
    }


print("=" * 78)
print(f"Cleaning fee mediano real cobrado do hóspede no segmento: R$ {CLEANING_FEE_MEDIANO_REAL:,.2f} (dado da base)")
print(f"Capital investido à vista (preço + transação + mobília): R$ {CAPITAL_AVISTA:,.2f}")
print("=" * 78)

# Cenário A v1 (referência, modelo anterior com limpeza e taxa airbnb como custo)
cA_v1 = cenario_v2("A v1 - autogestão (modelo anterior, c/ limpeza R$6.668 e Airbnb split-fee 4%)",
                    0.0, 0.04, incluir_limpeza=True)

# Cenário A v2 (novo): limpeza 100% repassada (custo=0), Airbnb split-fee com taxa
# residual do anfitrião zerada (100% repassada ao hóspede como taxa de serviço)
cA_v2 = cenario_v2("A v2 - autogestão, limpeza e taxa Airbnb 100% repassadas ao hóspede",
                    0.0, 0.0, incluir_limpeza=False)

# Cenário B v1 (referência, gestão terceirizada, host-only fee 15%, limpeza custo)
cB_v1 = cenario_v2("B v1 - gestão terceirizada (modelo anterior, host-only 15% + limpeza)",
                    0.25, 0.15, incluir_limpeza=True)

# Cenário B v2 (novo): limpeza repassada; taxa Airbnb host-only geralmente NÃO é
# repassável ao hóspede (é descontada do repasse ao anfitrião pela própria plataforma/
# gestora no modelo API/profissional) - mantemos o custo real de 15% aqui, só
# zeramos a limpeza, que é sempre repassável independente do modelo de gestão
cB_v2 = cenario_v2("B v2 - gestão terceirizada, limpeza repassada mas Airbnb host-only mantido",
                    0.25, 0.15, incluir_limpeza=False)

for c in (cA_v1, cA_v2, cB_v1, cB_v2):
    print(f"\n[{c['cenario']}]")
    print(f"  Receita bruta:        R$ {c['receita_bruta']:>10,.2f}")
    print(f"  (-) Gestora:          R$ {c['custo_gestora']:>10,.2f}")
    print(f"  (-) Taxa Airbnb:      R$ {c['custo_airbnb']:>10,.2f}")
    print(f"  (-) Limpeza:          R$ {c['custo_limpeza']:>10,.2f}")
    print(f"  (-) Condo+IPTU:       R$ {c['custo_condo_iptu']:>10,.2f}")
    print(f"  (-) Reserva manut.:   R$ {c['reserva_manutencao']:>10,.2f}")
    print(f"  (-) IR (PJ Simples):  R$ {c['ir_pj_simples']:>10,.2f}")
    print(f"  = NOI:                R$ {c['noi']:>10,.2f}  (margem {c['noi_margem_pct']:.1f}%)")
    print(f"  Yield à vista:        {c['yield_avista_pct']:.1f}% a.a.")
    print(f"  Payback:              {c['payback_anos']:.1f} anos")

print("\n" + "=" * 78)
print("GANHO DE YIELD (v2 vs v1)")
print("=" * 78)
print(f"Cenário A (autogestão):        {cA_v1['yield_avista_pct']:.1f}%  ->  {cA_v2['yield_avista_pct']:.1f}%  "
      f"(+{cA_v2['yield_avista_pct']-cA_v1['yield_avista_pct']:.1f} p.p.)")
print(f"Cenário B (gestão terceirizada): {cB_v1['yield_avista_pct']:.1f}%  ->  {cB_v2['yield_avista_pct']:.1f}%  "
      f"(+{cB_v2['yield_avista_pct']-cB_v1['yield_avista_pct']:.1f} p.p.)")

# ---------- Financiamento (recalculado com NOI v2) ----------
print("\n" + "=" * 78)
print("COMPRA FINANCIADA (SFH, SAC, entrada 30%, 20 anos, 11,2% a.a.) - com NOI v2")
print("=" * 78)
ENTRADA_PCT = 0.30
TAXA_FINANC_ANO = 0.112
PRAZO_ANOS = 20
entrada = PRECO * ENTRADA_PCT
principal_financiado = PRECO * (1 - ENTRADA_PCT)
capital_investido_financ = entrada + capital_transacao + MOBILIA
n_meses = PRAZO_ANOS * 12
taxa_mensal = (1 + TAXA_FINANC_ANO) ** (1 / 12) - 1
amortizacao_mensal = principal_financiado / n_meses

saldo = principal_financiado
juros_ano1 = 0.0
for m in range(12):
    juros_ano1 += saldo * taxa_mensal
    saldo -= amortizacao_mensal
amort_ano1 = amortizacao_mensal * 12
servico_divida_ano1 = juros_ano1 + amort_ano1

print(f"Capital investido (financiado): R$ {capital_investido_financ:,.2f}")
print(f"Serviço da dívida (ano 1):      R$ {servico_divida_ano1:,.2f}")
for c in (cA_v2, cB_v2):
    fluxo = c["noi"] - servico_divida_ano1
    coc = fluxo / capital_investido_financ * 100
    print(f"\n[{c['cenario']}]")
    print(f"  NOI:                    R$ {c['noi']:,.2f}")
    print(f"  (-) Serviço da dívida:  R$ {servico_divida_ano1:,.2f}")
    print(f"  = Fluxo do investidor:  R$ {fluxo:,.2f}")
    print(f"  Cash-on-cash financiado: {coc:.1f}% a.a.")
