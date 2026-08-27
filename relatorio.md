# Recomendação de Investimento — Mercado Imobiliário de Itapema (SC)
### Hackathon Seazone · Jovens Talentos AI Builder 2026 · Vinicius Azevedo

> Análise construída a partir de `Details_Itapema.csv`, `Hosts_ids_Itapema.csv`, `Mesh_Ids_Data_Itapema.csv`, `Price_AV_Itapema.csv` e `VivaReal_Itapema.csv`. Código reprodutível em [`analise/`](./analise). Metodologia detalhada na Seção 8.

> ⚠️ **NOTA IMPORTANTE (decisão = aquisição de imóvel pronto):** a decisão do desafio é **qual imóvel adquirir hoje** (compra, não desenvolvimento/SPOT). Este relatório recomenda **comprar um apartamento de 2 quartos em Morretes, com elevador, ~R$ 750 mil** (melhor retorno sobre o capital na amostra confiável, ~7,3% a.a.). A [`REVISAO_E_RECOMENDACAO_REVISADA.md`](./REVISAO_E_RECOMENDACAO_REVISADA.md) testou essa conclusão de forma crítica e confirmou que ela se mantém para decisão de aquisição (SPOT é avaliado apenas como contexto, não como a decisão). Leia os dois: este documento cobre as 4 perguntas do desafio; a revisão mostra o senso crítico sobre a escolha. As fontes estão em [`FONTES_E_PREMISSAS.md`](./FONTES_E_PREMISSAS.md).

---

## Resumo executivo

Os dados **não sustentam** a tese interna de que apartamentos compactos (studio/1 quarto) no Centro são a aposta mais eficiente — esse segmento tem adesão de mercado quase nula, receita entre as piores do dataset, e o m² de compra mais caro do próprio bairro. O que realmente explica receita é **capacidade do imóvel** (quartos, banheiros, hóspedes) e, dentro do condomínio, a presença de **elevador** — não localização central, não reputação do anfitrião.

A recomendação de compra é um **apartamento de 2 quartos no bairro Morretes, com elevador**, comprado à vista por cerca de **R$ 750 mil**. Dependendo de como o imóvel é operado e de qual receita se assume, o retorno líquido estimado fica entre **4,9% e 9,0% ao ano**, com payback de **13,7 a 20,3 anos**. Esse resultado é equivalente ao único case real e comparável (mesma cidade, imóvel pronto) que a própria Seazone divulga publicamente em Itapema — o que reforça que a recomendação é defensável mesmo diante do padrão da empresa contratante.

---

## 1. Qual o melhor perfil de imóvel para investir?

Receita escala com **capacidade**, não com estar compacto: cada quarto adicional soma, em mediana, mais de R$ 2 mil/mês de receita.

| Nº de quartos | Receita mensal mediana |
|---|---|
| 4+ | R$ 12.692 |
| 3 | R$ 7.972 |
| 2 | R$ 6.004 |
| 1 | R$ 4.194 |
| Studio (0) | R$ 3.705 |

**Apartamento** é o formato recomendado — domina o mercado (84% dos 4.441 anúncios), é o mais líquido tanto no Airbnb quanto no VivaReal, e supera "casa" e "outros" (hostels/kitnets) em receita mediana.

**Instalação de condomínio determinante: o elevador.** Controlando por tamanho do imóvel (para não confundir "prédio com lazer" com "unidade pequena"), o elevador é a única instalação com efeito positivo e consistente em qualquer tipologia (+15% a +31% de receita). Piscina, academia e espaço gourmet também ajudam a receita quando isolados do efeito de tamanho, mas **custam na compra um prêmio maior do que devolvem em receita** (ex.: elevador custa +20% no preço e entrega +15% na receita; academia custa +17% e entrega só +6% — a pior relação custo-benefício). Recomendação prática: priorizar elevador; evitar pagar prêmio só por piscina/academia/espaço gourmet, que diluem o retorno percentual.

---

## 2. Qual a melhor localização em termos de receita?

| Bairro | % da oferta da cidade | Receita mensal mediana (apartamentos) |
|---|---|---|
| **Meia Praia** | 64% | R$ 7.443 |
| Tabuleiro dos Oliveiras | 3% | R$ 5.841 |
| Centro | 15% | R$ 5.736 |
| Morretes | 10% | R$ 5.518 |
| Casa Branca | 2% | R$ 4.444 |

**Meia Praia lidera em receita bruta absoluta** — maior praia da cidade, maior densidade de bares/restaurantes, motor turístico principal. Mas essa é a resposta para "receita absoluta". Quando o critério muda para **retorno sobre o capital investido**, o ranking se inverte: bairros mais baratos como Morretes entregam o melhor retorno, porque o preço de entrada cai proporcionalmente mais do que a receita (ver Seção 5).

---

## 3. Quais características explicam as melhores receitas?

Correlação com receita mensal (amostra confiável, n=925): nº de banheiros (+0,19), nº de hóspedes (+0,16), nº de camas (+0,12) — todas ligadas a capacidade. Star rating (~0,00) e satisfação do hóspede (~0,00) praticamente não importam.

Amenidades com maior impacto (diferença de receita mediana): **estacionamento (+29%)** — cidade de praia, hóspede chega de carro — e **elevador (+18%)**. Sinais de qualidade de operação (superhost +11%, "guest favorite" +10%) ajudam na margem, mas não compensam um imóvel pequeno ou mal localizado.

**Conclusão:** priorize capacidade, estacionamento e elevador. Reputação do anfitrião é otimizável depois da compra; tamanho e localização, não.

---

## 4. Posição sobre a tese: "studios/1 quarto no Centro são a aposta mais eficiente"

**Os dados contrariam a tese**, em três dimensões testadas independentemente:

1. **Adesão de mercado:** apenas 3 anúncios do tipo studio em todo o Centro (0,5% dos 657 anúncios do bairro) — nenhum com dado de calendário suficiente para medir receita. O próprio mercado não validou esse produto.
2. **Receita:** studio/1 quarto no Centro (n=80) rende R$ 4.349/mês em mediana — um dos piores segmentos do dataset, menos da metade de um apartamento de 3 quartos no mesmo bairro (R$ 9.046/mês).
3. **Retorno sobre capital:** 1 quarto no Centro custa R$ 890 mil (R$ 19.905/m², o m² mais caro entre os cortes analisados no bairro — unidades pequenas pagam ágio por metro quadrado) e entrega yield líquido de 5,3% a.a., inferior a apartamentos maiores no mesmo bairro e muito inferior ao melhor segmento do dataset (Morretes 3 quartos: 13,7%).

**Veredito: rejeitar a tese.** O erro provável da hipótese interna foi assumir "Centro = localização premium" sem considerar que (i) Meia Praia concentra a demanda turística real e (ii) compacto = mais caro por m², o que não é compensado em receita, já que o mercado paga por capacidade, não por estar central.

---

## 5. Se a Seazone fosse investir hoje: o que comprar e por quê

### Recomendação: apartamento de 2 quartos em Morretes, com elevador

| | |
|---|---|
| Preço de compra | ≈ R$ 750.000 (R$ 11.100/m², ~69m²) |
| Distância da orla/Centro | ~3 km (dentro do raio de atrativos turísticos, Seção 7) |
| Amostra de suporte | 47 anúncios Airbnb com calendário confiável + 1.250 comparáveis de venda no VivaReal |

### Estimativa de retorno — vários cenários, do mais conservador ao mais otimista

Construí o modelo em camadas, testando premissas diferentes (todas com fonte documentada e, quando aplicável, verificadas por um segundo cálculo independente):

| Cenário | Receita bruta/ano | NOI/ano | Yield à vista | Payback |
|---|---|---|---|---|
| Custos operacionais reais completos (limpeza, taxa Airbnb, gestão, transação, mobília, IR), receita mediana | R$ 59.778 | R$ 39.993 | 4,9% | 20,3 anos |
| Idem, com receita revisada (ADR médio × ocupação média, removendo 1 outlier de dado) | R$ 71.857 | R$ 49.044 | 6,0% | 16,5 anos |
| Limpeza e taxa Airbnb tratadas como repasse ao hóspede (dado real: `cleaning_fee` mediano de R$250 confirmado na base) | R$ 59.778 | R$ 48.402 | 6,0% | 16,8 anos |
| Repasse + receita revisada combinados (cenário mais otimista) | R$ 71.857 | R$ 59.153 | **7,3%** | **13,7 anos** |
| Régua simplificada "estilo Seazone" (só desconta IR, sem custos operacionais — replicando a forma como a empresa divulga seus próprios números) | R$ 59.778–71.857 | — | 7,5%–9,0% | 11,1–14,4 anos |

**Faixa honesta de retorno: 4,9% a 9,0% ao ano, dependendo de quem opera o imóvel e de qual receita se assume.** O cenário mais realista para a Seazone operando o próprio imóvel (autogestão, sem repassar comissão a si mesma) fica entre 6,0% e 7,3% a.a., com payback de 13,7 a 16,8 anos. *(Round 2: a faixa caiu em relação à versão anterior — condomínio e IPTU passaram a ser medidos com valores reais do VivaReal em vez dos placeholders 0/1 da base; ver FONTES_E_PREMISSAS.md.)*

**Compra financiada não compensa nas taxas atuais.** Simulando SFH (30% de entrada, SAC, 20 anos, ~11,2% a.a.), o serviço da dívida no ano 1 (R$ 80.948) supera o NOI em todos os cenários — fluxo de caixa negativo. A taxa de financiamento é maior que o yield operacional do imóvel: alavancar destruiria retorno em vez de ampliá-lo. **Este investimento só se sustenta comprado à vista.**

### Validação externa: comparando com o próprio catálogo da Seazone

A Seazone vende um produto de investimento próprio (SPOTs — cotas fracionadas em empreendimentos pré-obra, anunciando 13-23% a.a.) e publica um case real em Itapema, o **Manhattan Flats** (Centro): retorno projetado de **8,1% a.a. depois de impostos**, e "mais de R$ 45 mil líquidos/ano por unidade" nas 76 unidades geridas pela empresa no prédio.

Os SPOTs não são um comparável justo — misturam yield operacional com valorização de obra, risco de construção, e margem de incorporação que a própria Seazone captura (não replicável comprando pronto no mercado secundário). **O comparável correto é o Manhattan Flats**, e nele:

- Em **percentual**: Morretes fica entre 4,9% e 9,0%, contra 8,1% do Manhattan Flats — equipara no cenário otimista, um pouco abaixo no conservador.
- Em **receita líquida absoluta**: Morretes entrega entre R$ 40,0 mil e R$ 67,5 mil/ano, superando na maioria dos cenários os "R$ 45 mil+" do Manhattan Flats.
- Em **tempo de retorno**: Morretes leva 13,7 a 20,3 anos, contra 12,3 anos implícitos no Manhattan Flats — equivalente no cenário otimista, um pouco atrás no conservador.

**Conclusão: a recomendação é competitiva com o padrão que a própria Seazone demonstra ser capaz de entregar em Itapema**, ainda que não alcance os números do produto de investimento pré-obra que a empresa vende a terceiros (SPOTs) — uma comparação estruturalmente diferente e não aplicável a uma compra de imóvel pronto no mercado secundário.

---

## 6. Aposta secundária / próximo passo natural

O segmento de **3 quartos em Morretes** tem o melhor yield do dataset inteiro (13,7% líquido), mas com amostra Airbnb pequena (n=9) — tratar como piloto antes de escalar. Uma estratégia ainda mais alinhada ao que a própria Seazone já validou em Itapema (o retrofit do Manhattan Flats, convertendo 1 quarto em 2 estúdios) seria testar a divisão de uma unidade maior em Morretes em duas unidades independentes — multiplicando receita sem trocar de bairro nem abrir mão do preço de entrada mais baixo da cidade.

---

## 7. Atrativos turísticos e de lazer num raio de 10 km

Todos os bairros analisados ficam a no máximo ~5 km da orla/Centro (Morretes, a mais distante, fica a ~3 km) — a cidade inteira está dentro do raio de 10 km de atrativos: Meia Praia (praia mais extensa, vida noturna), Canto da Praia e Praia da Ilhota, Costão de Itapema, Mirante do Encanto, Morro da Guarita, Gruta Nossa Senhora dos Navegantes, Parque das Capivaras, Praça da Paz, cachoeiras do Sertão. Balneário Camboriú (~13 km) e Porto Belo/Bombinhas (~15-23 km) ficam logo fora do raio, mas puxam demanda regional — Itapema historicamente atrai hóspedes que buscam preço mais baixo com acesso fácil a esses polos.

**Implicação para a decisão:** Meia Praia e Centro colhem diretamente o fluxo turístico da praia, o que explica ADR mais alto nesses bairros. Morretes está mais afastado da faixa de areia e não tem atrativo turístico próprio — coerente com seu ADR mais baixo, mas é exatamente o que barateia o preço de compra sem penalizar tanto a receita, sustentando o yield superior.

---

## 8. Metodologia (resumo) e limitações

- **ADR e ocupação são proxies**, não dados diretos de reserva: usamos o snapshot mais recente do calendário de preços (`Price_AV_Itapema.csv`), tratando "dia que sumiu do calendário" como provável reserva. Cobre 22,5% dos 4.441 anúncios (999); amostra restrita a janelas de calendário ≥60 dias (925) para confiabilidade.
- **Yield líquido** = (receita anual proxy − condomínio − IPTU anuais medianos) ÷ preço de venda mediano do segmento bairro×quartos (VivaReal, `business_types=="Venda"`, n≥5 em ambas as bases). *(Round 2: condomínio e IPTU são medidos apenas com valores reais — descartando os placeholders 0/1 e valores triviais da base; Morretes 2Q passa de R$3/mês para R$350/mês de condomínio, o que reduz o yield para ~7,3%.)*
- **Custos de aquisição e operação** (ITBI 1,5%, escritura/registro 2,0%, mobília ~R$35k, limpeza, taxa Airbnb, gestão, IR) vêm de pesquisa de mercado — fontes e ressalvas de incerteza documentadas nos arquivos de apoio em `analise/`.
- **Com mais uma semana**, eu: (i) buscaria dados reais de disponibilidade/reserva em vez da proxy de calendário; (ii) usaria geolocalização exata para medir distância real até a praia, não o centróide do bairro; (iii) testaria a estratégia de retrofit (dividir unidade em duas) com uma cotação real de reforma; (iv) validaria os custos de mobília e a taxa de gestão da Seazone com números internos, já que não são públicos.

**Fontes da pesquisa de atrativos e do comparativo com a Seazone:**
- [Pontos Turísticos de Itapema SC — Litoral de Santa Catarina](https://www.litoraldesantacatarina.com/itapema/pontos-turisticos-de-itapema.php)
- [O que fazer em Itapema SC — Blog de Viagem e Turismo](https://blogdeviagemeturismo.com.br/o-que-fazer-em-itapema-sc/)
- [Seazone Marketplace — SPOTs](https://seazone.com.br/marketplace)
- [Manhattan Flats: imóveis como investimento em Itapema](https://seazone.com.br/blog/manhattan-flats-itapema)
- [A Seazone é segura para investir?](https://institucional.seazone.com.br/faq/seazone-segura-para-investir/)
