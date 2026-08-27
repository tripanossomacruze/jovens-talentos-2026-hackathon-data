# Como cheguei nas estimativas do projeto

Este texto resume, de forma curta, **de onde vêm os números** que sustentam as conclusões. A regra foi uma só: **nunca inventar número** — tudo ou saiu das 5 bases reais do desafio, ou veio de pesquisa de mercado com fonte, ou foi assumido com justificativa e com o grau de incerteza sinalizado. O detalhe completo está em `FONTES_E_PREMISSAS.md`.

---

## 1. Receita dos imóveis (a base de tudo)

As bases de Airbnb não dão receita pronta — elas dão o **calendário de preços futuros** (`Price_AV`). Então estimamos, por anúncio:
- **ADR** = preço médio anunciado por diária.
- **Ocupação (proxy)** = dias que "sumiram" do calendário mais recente ÷ total de dias, tratados como reserva.

Com isso, **receita mensal ≈ ADR × ocupação × 30**, restrita a uma amostra confiável de **925 anúncios** (janela de calendário ≥ 60 dias, de 4.441 totais). Essa é uma **proxy** — pode confundir bloqueio manual do anfitrião com reserva real. Por isso toda conclusão foi testada com **haircuts de −10%, −20% e −30%** na receita.

## 2. Custo de compra (mercado real)

Do **VivaReal** (8.329 imóveis à venda), tiramos o **preço mediano por bairro × nº de quartos**: ex. Morretes 2Q = R$ 750 mil (R$ 11.100/m²), Meia Praia 1Q = R$ 883 mil (R$ 21.125/m²).

## 3. Custo de carregar (condomínio + IPTU)

Aqui houve uma **correção importante (rodada 2)**: a base VivaReal tem muitos placeholders (`0`, `1`, vazio) em condomínio/IPTU, o que subestimava o custo. Passamos a usar **apenas valores reais** (condomínio > R$ 30/mês, IPTU > R$ 50/ano, por segmento). Resultado: Morretes 2Q condomínio real de **R$ 350/mês** (não R$ 3). Isso **reduziu os yields honestamente**: Morretes 2Q de ~7,9% → **~7,3%**; Meia Praia 1Q de ~7,2% → **~6,2%**.

## 4. Retorno (ROI)

Com receita e custo de compra, calculamos:
- **Yield** = (receita anual − condomínio − IPTU) ÷ preço de compra.
- Ajustes operacionais de mercado: custo de **mobília** (~R$ 35 mil), **limpeza** por virada (~R$ 190), **taxa Airbnb** (4% a 15% conforme modelo), **gestão** (~25%), reserva de manutenção (5%) e **IR** (6%, PJ Simples). Todos com fonte.
- **Returno de compra pronto: 4,9% a 9,0% a.a.** (cenário realista de autogestão ~6–7%), payback 13,7–20,3 anos. Financiar (~11,2% a.a.) **destrói** o retorno — o custo da dívida supera o yield.

## 5. Decidindo por um imóvel PRONTO (aquisição)

O desafio é decidir a **aquisição de um imóvel pronto**. Por isso o critério é o **retorno sobre o capital de compra** (yield), não a receita por m² de uma incorporação. Entre os segmentos com amostra confiável, o que combina **maior yield + amostra adequada + menor ticket** é o **apartamento de 2 quartos em Morretes**:
- Preço mediano ~R$ 750 mil (R$ 11.100/m²); receita ~R$ 59,8 mil/ano.
- Yield líquido **~7,3%** (já descontado condomínio/IPTU reais). Empata, dentro do erro, com Meia Praia 1Q (~6,2%) — e Morretes vence pelo preço de entrada menor.
- Morretes 3Q rende mais (13,7%) mas é piloto (n=9). Alternativa mais líquida: 1Q em Meia Praia.

### Precisão honesta (custo de carregar)
O yield foi recalculado com **condomínio/IPTU reais** (não placeholders 0/1 da base). Isso reduziu o retorno de forma honesta: Morretes 2Q de ~7,9% para ~7,3%. Também testamos haircuts de −10/−20/−30% na receita (fragilidade da proxy de ocupação).

---

## Resumo das 4 conclusões
1. **Perfil:** apartamento de 2 quartos — capacidade e elevador.
2. **Melhor localização por receita:** Meia Praia; por retorno sobre capital, Morretes.
3. **Drivers de receita:** capacidade (quartos/banheiros), elevador, estacionamento — não localização central nem reputação.
4. **O que comprar hoje:** **apartamento de 2 quartos em Morretes, com elevador**, ~R$ 750 mil, retorno líquido ~7% ao ano (à vista). Alternativa mais líquida: 1Q em Meia Praia.

**Tese da Seazone (studio/1Q Centro): contrariada pelos dados** — só existem 3 studios no Centro e rendem menos da metade de um apartamento maior no mesmo bairro.

---

*Todo número das seções acima roda com os scripts em `analise/` e é validado por um segundo cálculo independente. Limitações: receita por proxy de calendário, custos de obra/mobília de mercado, e taxa de gestão real da Seazone não é pública (usamos faixa de mercado).*