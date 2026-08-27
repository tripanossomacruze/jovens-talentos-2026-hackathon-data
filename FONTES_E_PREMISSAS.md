# Fontes e premissas — de onde vem cada número da solução

Este documento rastreia a origem de **todo número** usado na recomendação, separando o que é (A) dado real das bases do desafio, (B) dado pesquisado no mercado com fonte pública, e (C) premissa assumida — com a justificativa e o grau de incerteza de cada uma. A regra foi: nunca inventar número; quando não há dado local confirmado, usar referência de mercado e sinalizar.

---

## A) Dados extraídos das 5 bases do desafio (fonte primária, alta confiança)

| Número | Valor | Origem |
|---|---|---|
| Total de anúncios Airbnb em Itapema | 4.441 | `Details_Itapema.csv` |
| Anúncios com dado de preço/calendário | 999 (22,5%) | `Price_AV_Itapema.csv` cruzado com Details |
| Amostra confiável (janela ≥60 dias) | 925 | filtro sobre a base de preços |
| Receita mensal mediana por tipologia (studio→4Q: R$ 3.705 a R$ 12.692) | — | ADR × ocupação proxy, `Price_AV` |
| Receita/m² por tipologia (1Q = R$ 1.235/m²/ano, o melhor) | — | receita Airbnb ÷ área mediana VivaReal |
| Ranking de bairros por receita (Meia Praia lidera, R$ 7.443/mês) | — | `Details` + `Mesh_Ids_Data` |
| 3 studios no Centro (de 657 anúncios) | — | `Details` + `Mesh` |
| Preço de venda mediano Morretes 2Q | R$ 750.000 (R$ 11.100/m², 69m²) | `VivaReal_Itapema.csv` |
| Preço de venda 1Q Meia Praia | R$ 21.125/m² | `VivaReal_Itapema.csv` |
| Taxa de limpeza mediana cobrada (Morretes 2Q) | R$ 250 | campo `cleaning_fee` de `Details` |
| Condomínio + IPTU medianos por segmento | — | `VivaReal_Itapema.csv` |
| Distância dos bairros à orla (Morretes ~3 km) | — | haversine sobre centróides de `Mesh` |
| Correlações de receita (banheiros +0,19, star rating ~0) | — | `Details` + preços |

**Ressalva-chave sobre esses dados:** ADR e ocupação são **proxies** derivadas do calendário de preços futuros (3 capturas em jan/2025), não dados diretos de reserva. "Dia que sumiu do calendário mais recente" foi tratado como provável reserva. É uma aproximação padrão do setor, mas pode confundir bloqueio manual do anfitrião com reserva real — por isso a análise de sensibilidade testa haircuts de até -30% na receita.

**Ressalva round 2 (condomínio/IPIU):** a base `VivaReal` tem em `monthly_condo_fee` e `yearly_iptu` muitos placeholders (vazio, `0`, `1`) e valores triviais que, se agregados pela mediana bruta, subestimam drasticamente o custo de carrego (ex.: Morretes 2Q passaria de R$3/mês para um valor real de ~R$350/mês). A partir desta revisão, os yields passaram a usar **apenas valores reais** (`>R$30` para condomínio, `>R$50` para IPTU) na mediana de cada segmento. Isso **reduziu** os yields: Morretes 2Q de ~7,9% → ~7,3%; Meia Praia 1Q de ~7,2% → ~6,2%.

---

## B) Dados pesquisados no mercado (fonte pública, ago/2026)

| Número | Valor | Fonte |
|---|---|---|
| CUB-SC (custo de construção civil) | R$ 3.122/m² (jul/2026) | [Sinduscon-SC via MySide](https://myside.com.br/guia-balneario-camboriu/cub-sc) |
| Preço médio do m² em Meia Praia | R$ 15.089/m² (geral); R$ 11.861/m² (2Q) | [Proprietário Direto](https://www.proprietariodireto.com.br/preco-m2/meia_praia-itapema) |
| Preço de terreno em Meia Praia | R$ 8.319/m² (300m² por R$ 2,5M) | [Marcus Imóveis](https://marcusimoveis.com.br/imovel/1475077-terreno-em-meia-praia-a-venda) |
| ITBI de Itapema | 1,5% (sobe a 2% em 2027) | pesquisa (agente), legislação municipal |
| Taxa de gestão de temporada no Brasil | 20–30% da receita bruta | pesquisa de mercado (gestoras de temporada) |
| Taxa Airbnb (split-fee vs host-only) | ~4% vs ~15% | pesquisa de mercado |
| Financiamento SFH (Caixa) | ~11,2% a.a., entrada 20-30% | pesquisa de mercado |
| IR aluguel PJ Simples (Anexo III) | 6% até R$ 180k/ano de receita | pesquisa de mercado |
| Retornos anunciados pela Seazone (SPOTs 13-23%; Manhattan Flats 8,1%; "R$45 mil+/unidade") | — | [seazone.com.br/marketplace](https://seazone.com.br/marketplace), [Manhattan Flats](https://seazone.com.br/blog/manhattan-flats-itapema), [Grandes Operações](https://seazone.com.br/lps/grandes-operacoes) |
| Atrativos turísticos (praias, mirantes, Balneário Camboriú ~13km) | — | [Litoral de SC](https://www.litoraldesantacatarina.com/itapema/pontos-turisticos-de-itapema.php), [Blog de Viagem](https://blogdeviagemeturismo.com.br/o-que-fazer-em-itapema-sc/) |
| Anúncios reais de imóveis (Ilha dos Açores II, La Maison, Oben 230) | — | [MySide Itapema](https://myside.com.br/apartamentos-venda-morretes-itapema-sc) |

**Ressalva:** os retornos da Seazone são material comercial da própria empresa (com disclaimer de "não constitui promessa") — usados só para comparação "nos termos deles", nunca como verdade auditada. A taxa de administração exata da Seazone **não é divulgada publicamente** — usei a faixa de mercado (25%).

---

## C) Premissas assumidas (com justificativa e incerteza)

| Premissa | Valor usado | Justificativa | Incerteza |
|---|---|---|---|
| Custo de mobília (1 unidade temporada) | R$ 25–35 mil | ponto médio de faixas de mercado (não achei dado específico de SC) | **Alta** — pode variar ±30% |
| Estadia média por reserva | 4 noites | padrão do setor p/ litoral (campo `min_nights` veio zerado na base) | Média |
| Construção all-in | R$ 5.500/m² (~1,75× CUB) | CUB é custo-base; all-in inclui BDI, acabamento e mobília p/ short-stay | Média-alta |
| Eficiência (privativa/construída) | 75% | típico de torres residenciais | Baixa-média |
| FAR / índice de aproveitamento | 4 a 6 | exigiria o Plano Diretor de Itapema; usei faixa conservadora p/ Meia Praia | **Alta** — não confirmado |
| Soft costs (projeto, aprovação, venda, impostos de obra) | 15% do hard cost | heurística de incorporação | Média |
| Reserva de manutenção | 5% da receita | heurística padrão do setor imobiliário | Baixa |
| Taxa de gestão da Seazone | 25% | ponto médio da faixa 20-30% (não é pública) | Média |

> **Nota (decisão de aquisição):** as premissas de incorporação da tabela acima — custo de construção all-in, eficiência, FAR/índice de aproveitamento e soft costs — pertencem ao cenário de **construir um SPOT**, que foi avaliado **apenas como contexto** e **não é a decisão final** (o desafio pede aquisição de imóvel pronto). A resposta final usa as premissas de compra/operação: custo de aquisição, condomínio/IPTU reais, mobília, limpeza, taxa Airbnb, gestão e IR.

---

## Como a incerteza foi tratada

Onde uma premissa é frágil, a análise **não escondeu** — mostrou faixas em vez de número único:
- ROI apresentado como **faixa de 4,9% a 9,0%** (round 2, após condomínio/IPTU reais) conforme a metodologia de custos, não um valor cravado.
- Análise de **sensibilidade** explícita: haircuts de -10/-20/-30% na receita, e o efeito de cada premissa no yield.
- Decisão final é de **aquisição** (compra de imóvel pronto); o pro-forma de construção (SPOT) foi avaliado **apenas como contexto** para confirmar o escopo, com break-even de ~R$ 11-12 mil/m².
- Cada afirmação "estilo Seazone" acompanhada da ressalva de que é régua da própria empresa, não auditada.

**O que eu validaria com mais tempo / acesso:** (i) dados reais de reserva (não a proxy de calendário); (ii) geolocalização exata dos imóveis (não apenas o centróide do bairro); (iii) cotação real de aquisição/mobília e de gestão com fornecedores locais; (iv) a taxa de administração interna real da Seazone.

---

*Todo o código que gera os números da seção (A) está em [`analise/`](./analise) e é reprodutível a partir das 5 bases originais do desafio. Os números das seções (B) e (C) alimentam os scripts `04`, `05`, `07` e `10` como constantes no topo de cada arquivo, comentadas com a fonte.*
