# Revisão crítica e recomendação revisada
### Testando a própria conclusão — para uma decisão de AQUISIÇÃO de imóvel

Este documento faz três coisas que o relatório original não fazia: (1) submete a recomendação anterior (comprar um apartamento de 2 quartos em Morretes) a testes que tentam **derrubá-la**; (2) testa um ângulo alternativo — a Seazone poderia **construir SPOTs** em vez de comprar pronto — que **não** é o foco do desafio (que pede aquisição), e por isso o tratamento dado a essa opção é de contexto; e (3) ancora a solução em **anúncios reais** do mercado. **Conclusão: para a decisão de compra, permanece recomendado adquirir 2 quartos em Morretes** (melhor yield ajustado), com o compacto de Meia Praia como alternativa mais líquida.

---

## Parte 1 — A recomendação anterior sobrevive ao escrutínio? Parcialmente.

Rodei cinco testes contra o "comprar 2Q em Morretes" (código em `analise/08_revisao_critica.py`):

**a) O preço baixo de Morretes é parte só tamanho menor.** Os apartamentos de 2 quartos em Morretes têm 69m² de mediana, contra 85m² em Meia Praia e 86m² no Centro. O R$/m² de Morretes (R$ 11.100) é de fato mais barato que Meia Praia (R$ 12.929), mas a diferença é bem menor do que o preço absoluto sugere — parte do "desconto" é simplesmente unidade menor.

**b) O intervalo de confiança derruba a ideia de "o melhor".** Bootstrap (2.000 reamostragens) da receita mensal mediana:

| Bairro (2Q) | n | Mediana | IC 95% |
|---|---|---|---|
| Morretes | 47 | R$ 4.982 | **[R$ 4.067 – R$ 6.215]** |
| Meia Praia | 175 | R$ 6.245 | [R$ 5.736 – R$ 6.811] |
| Centro | 63 | R$ 6.467 | [R$ 5.599 – R$ 7.252] |

A receita de Morretes é **estatisticamente mais baixa** que Meia Praia e Centro — o limite superior do IC de Morretes (R$ 6.215) mal alcança a mediana dos outros. O yield de Morretes vem inteiramente do preço de compra menor, não de receita maior. E o topo do ranking de yield (Morretes 2Q 7,3%; Casa Branca 2Q 6,9%; Meia Praia 2Q 6,3%; Meia Praia 1Q 6,2%) está agrupado dentro de menos de 1 ponto percentual — **empate técnico**, não um vencedor claro.

**c) A vantagem é frágil à premissa de ocupação.** Se a ocupação real de Morretes estiver 20% acima do verdadeiro (a proxy de calendário pode confundir bloqueio manual com reserva), o yield cai de 7,3% para ~6,5% — abaixo de Meia Praia 1Q. A conclusão dependia de uma premissa que não consigo verificar com os dados.

**d) Não dá para confirmar que os imóveis de Morretes estão longe da praia.** Os 56 anúncios de Morretes 2Q têm coordenadas zeradas na base — o argumento de "3 km da orla" veio do centróide do bairro, não dos imóveis em si.

**Conclusão da Parte 1:** "comprar 2Q em Morretes" é uma escolha **defensável**, mas chamá-la de "a melhor" superestima a evidência. Ela empata, dentro do ruído estatístico, com comprar um compacto (1 quarto) em Meia Praia — que tem receita mais previsível, muito mais liquidez (Meia Praia = 64% do mercado) e demanda turística comprovada. Se o critério for risco-ajustado, **1 quarto em Meia Praia é a compra pronta mais segura**, não Morretes.

---

## Parte 2 — E se o caminho fosse construir (SPOT)? É descartado: a decisão é aquisição

Uma hipótese alternativa é a Seazone não comprar e sim construir um SPOT próprio. É uma opção real para o negócio da empresa, mas **está fora do escopo deste desafio**, que pergunta explicitamente "se a Seazone fosse investir hoje, o que você compraria" — decisão de **aquisição de imóvel pronto**. Mesmo assim, avaliei esse ângulo para garantir senso crítico e confirmar que a compra continua sendo a resposta certa no escopo.

**Se o critério fosse "construir" (não é o caso), a receita por m² construído favoreceria:**
- **1 quarto** = R$ 1.235/m²/ano (o melhor em eficiência).
- Studio = R$ 872/m² — o pior entre compactos; **2 quartos** = R$ 1.036.
- Entre bairros, para 1Q, Meia Praia (~R$ 1.491/m²) > Centro (~R$ 1.220).

Ou seja: mesmo pelo viés de construção, a intuição de "compacto" aponta para **1 quarto em Meia Praia** — não studio e não Centro. Isso reforça, por outra ótica, que o **studio no Centro é má aposta**.

**Conclusão da Parte 2 — por que não seguimos o SPOT:** além de estar fora do escopo (o desafio pede aquisição), o ganho de capital de uma construção é **altamente condicional** — depende de o imóvel pronto valer acima de **~R$ 11–12 mil/m²** (break-even). No cenário mais real (~R$ 9,4 mil/m²), a "vantagem" do SPOT **colapsa** e a margem fica negativa. Portanto, para uma decisão de compra, a via robusta e direta é **comprar pronto** — e a melhor opção é o **2 quartos em Morretes** (yield ~7,3% a.a. na amostra confiável).

---

## Parte 3 — Ancorando em imóveis reais (busca no mercado, ago/2026)

**Para o ponto original (comprar 2Q pronto em Morretes):**
- **Ilha dos Açores II** — Rua 410, Morretes. 70m², 2 suítes, 1 vaga, varanda com churrasqueira, piscina, salão de festas, portaria eletrônica. **R$ 740–750 mil.** Confirma que o meu número (R$ 750k / 69m² / 2Q) é o preço real de mercado. *Observação crítica:* é **lançamento** (entrega prevista 2031), não pronto — e essa é a regra, não a exceção: quase todo o estoque de Morretes no MySide é lançamento. Isso explica o R$/m² baixo (preço de lançamento) e serve de alerta na decisão de **aquisição**: é preciso garantir um imóvel pronto para operar já, não um lançamento para entrega futura. [ver anúncio](https://myside.com.br/apartamento-venda-ilha-dos-acores-ii-itapema-sc)
- Outros lançamentos 2Q ~68-70m² na mesma faixa: Cattleya (R$ 702k+), Delta Tower (R$ 590–806k), Ilha Li Galli T3 (R$ 757k+). [busca Morretes](https://myside.com.br/apartamentos-venda-morretes-itapema-sc)

**Para o ponto revisado (compacto em Meia Praia):**
- **La Maison de Versailles** — Meia Praia, unidades a partir de **R$ 394 mil** (1 quarto, 42m²), com piscina, salão, mercado interno. [ver anúncio](https://myside.com.br/apartamento-venda-la-maison-de-versailles-itapema-sc)
- **Oben 230** — Meia Praia, 1 quarto 42-68m², piscina aquecida, 4 elevadores, rooftop. [ver anúncio](https://myside.com.br/apartamento-venda-oben-230-itapema-sc)

> Estes anúncios ancoram, em preço real de mercado, os dois cenários da decisão de **aquisição**: o 2Q em Morretes (~R$ 750 mil) e o compacto de Meia Praia como alternativa mais líquida. Não se consideram terrenos de incorporação, pois a decisão é de compra pronta.

---

## Veredito revisado

**O desafio é a decisão de adquirir um imóvel pronto.** Para essa decisão, a recomendação mais defensável continua sendo **comprar um apartamento de 2 quartos em Morretes, com elevador, ~R$ 750 mil**. A revisão crítica que fiz neste documento mostrou que essa escolha **não** é destacadamente "a melhor" num número único bonito — ela **empata** (dentro do erro estatístico) com o compacto de Meia Praia —, mas mantém a vantagem que interessa: **menor preço de entrada (~R$ 750 mil vs ~R$ 883 mil) com yield similar (~7,3% vs ~6,2%)**, na amostra mais confiável do grupo (n=47) e na região de menor custo por m².

**Alternativas mais alinhadas ao risco da Seazone (todas de compra pronta):**
- **Mais líquida / previsível:** 1 quarto em **Meia Praia** (~6,2%, bairro = 64% do mercado, demanda turística comprovada).
- **Maior yield com amostra fina (piloto):** 3 quartos em Morretes (~13,7%, mas n=9).
- A tese interna "compacto (studio/1Q) no Centro" **não se sustenta** — pouca adesão de mercado e receita baixa.

**Nota de rigor (round 2 e 3):** os yields foram recalculados com **condomínio/IPTU reais** (não placeholders da base) e com haircuts de ocupação, deixando o retorno mais honesto (Morretes 2Q ~7,3%). Toda estimativa é **retorno sobre o capital de compra (yield)**, coerente com uma decisão de aquisição — e não receita por m² de incorporação.

Esta revisão é, ela própria, a resposta ao pedido do desafio de mostrar **senso crítico**: a conclusão inicial foi testada, uma delas não se sustentou como "a melhor", e a análise evoluiu — como a decisão é de **compra** (não de desenvolvimento), a forma mais defensável é **2 quartos em Morretes** (melhor yield ajustado por amostra e capital).
