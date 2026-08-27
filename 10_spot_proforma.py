"""
Etapa 10 - Pro-forma de um SPOT (novo desenvolvimento) vs comprar pronto.
Testa a hipótese: para a Seazone (incorporadora-operadora), construir um SPOT de
unidades de 1 quarto em Meia Praia rende mais que comprar pronto, porque captura
a MARGEM DE INCORPORAÇÃO em vez de pagá-la ao vendedor.

TODAS as premissas de custo estão explícitas e sinalizadas. FAR (índice de
aproveitamento) exige o plano diretor de Itapema; usamos cenário conservador.
"""
import numpy as np

# ---- Produto ótimo pela análise de receita/m² (Etapa 9): 1 quarto em Meia Praia ----
AREA_PRIVATIVA = 43.0          # m² (área mediana de 1Q, VivaReal)
EFICIENCIA = 0.75              # área privativa / área construída (comum+circulação)
AREA_CONSTRUIDA = AREA_PRIVATIVA / EFICIENCIA
REV_ANO_1Q_MEIAPRAIA = 64_097  # receita bruta anual mediana (Airbnb, Meia Praia 1Q, n=20)

# ---- Custos (pesquisa de mercado, ago/2026) ----
CUB_SC = 3_122                 # R$/m² (Sinduscon-SC)
CONSTRUCAO_ALLIN = 5_500       # R$/m² construído all-in (CUB + BDI + acabamento p/ short-stay ~1.75x CUB)
MOBILIA_UNIT = 25_000          # mobiliar 1 studio/1Q p/ temporada
TERRENO_M2 = 8_319             # R$/m² de terreno (anúncio real Meia Praia, 300m² por R$2,5M)
SOFT_COST_PCT = 0.15           # projeto, aprovações, incorporação, comercialização, impostos de obra

# ---- VALOR DE MERCADO (round 2): âncora corrigida em FAIXA, não número único ----
# O valor "pronto" da unidade depende do R$/m² realizado no mercado. A mediana
# VivaReal de 1Q Meia Praia é R$21.125/m², mas há enorme dispersão (p10≈R$13.900)
# e os anúncios reais de lançamento citados rodam bem abaixo (~R$9.400/m², La Maison).
# Testamos 3 cenários + calculamos o break-even (m² mínimo para o SPOT valer a pena).
PRECO_MERCADO_M2 = {
    "Cenário baixo (anúncios reais ~R$9.400/m²)": 9_400,
    "P10 da VivaReal 1Q Meia Praia (~R$13.900/m²)": 13_900,
    "Mediana VivaReal 1Q Meia Praia (R$21.125/m²)": 21_125,
}

# ---- Operação (modelo realista de autogestão, consistente com ROI anterior) ----
def noi(receita):
    # custos operacionais como % da receita (reserva 5% + IR 6%); limpeza/Airbnb repassados
    return receita * (1 - 0.05 - 0.06)

print("="*78)
print("PRO-FORMA: SPOT de 1 quarto em Meia Praia (por unidade)")
print("="*78)

construcao = AREA_CONSTRUIDA * CONSTRUCAO_ALLIN
print(f"Area privativa: {AREA_PRIVATIVA:.0f}m² | Area construida: {AREA_CONSTRUIDA:.0f}m²")
print(f"Construcao all-in ({CONSTRUCAO_ALLIN}/m² constr.): R$ {construcao:,.0f}")

print("\n" + "-"*78)
print("CUSTO DE DESENVOLVIMENTO por unidade (por cenário de FAR)")
print("-"*78)
custos_por_far = {}
for FAR in [4, 6]:  # índice de aproveitamento (m² construído por m² de terreno)
    terreno_por_unidade = (AREA_CONSTRUIDA / FAR) * TERRENO_M2
    hard_cost = construcao + terreno_por_unidade + MOBILIA_UNIT
    soft = hard_cost * SOFT_COST_PCT
    custo_total = hard_cost + soft
    custos_por_far[FAR] = custo_total
    break_even_m2 = custo_total / AREA_PRIVATIVA
    print(f"\n--- FAR={FAR} ---")
    print(f"  Terreno/unidade:        R$ {terreno_por_unidade:,.0f}")
    print(f"  Mobilia:                R$ {MOBILIA_UNIT:,.0f}")
    print(f"  Soft costs ({SOFT_COST_PCT*100:.0f}%):        R$ {soft:,.0f}")
    print(f"  CUSTO TOTAL de criar a unidade: R$ {custo_total:,.0f}")
    print(f"  >> BREAK-EVEN de valor de venda: R$ {break_even_m2:,.0f}/m² privativo")

print("\n" + "="*78)
print("VALOR DE MERCADO x MARGEM, por cenário de R$/m² (recomendação FRÁGIL ao preço)")
print("="*78)
rev = REV_ANO_1Q_MEIAPRAIA
noi_ano = noi(rev)
print(f"NOI anual (autogestão): R$ {noi_ano:,.0f}\n")
for nome, pm2 in PRECO_MERCADO_M2.items():
    valor_mercado = AREA_PRIVATIVA * pm2
    for FAR in [4, 6]:
        custo_total = custos_por_far[FAR]
        margem = valor_mercado - custo_total
        valorizacao = margem / custo_total * 100
        y_custo = noi_ano / custo_total * 100
        y_mercado = noi_ano / valor_mercado * 100
        flag = "   (SPOT vale a pena)" if margem > 0 else "   (<- SPOT NAO compensa)"
        print(f"[{nome} | FAR={FAR}]  valor pronto={valor_mercado:,.0f} | "
              f"margem={margem:+,.0f} ({valorizacao:+.0f}%) | y/custo={y_custo:.1f}% | y/mercado={y_mercado:.1f}%{flag}")

print("\n" + "="*78)
print("COMPARACAO FINAL (honesta)")
print("="*78)
print("Comprar 1Q PRONTO em Meia Praia (mediana VivaReal ~R$908k): ~7,1% a.a., sem ganho de capital")
print("CONSTRUIR SPOT 1Q em Meia Praia (custo de dev ~R$480-530k):")
print("  -> yield sobre CUSTO ~11-12% a.a. (solidez da operação, independente do valor de venda)")
print("  -> ganho de capital (margem de incorporação) é POSITIVO e grande SÓ se o valor de venda")
print("     realizado estiver acima do BREAK-EVEN (~R$11-12k/m²). No cenário de lançamento real")
print("     (~R$9,4k/m², abaixo do break-even) a vantagem do SPOT sobre 'comprar pronto' COLAPSA,")
print("     pois você pagaria a margem em vez de capturá-la. Não é um retorno garantido (+80%):")
print("     é uma FAIXA que vai de negativo (cenário baixo) a ~+80% (mediana VivaReal).")
