📹 Vídeo (3 min): https://drive.google.com/file/d/1efeZAqKdoWjFnKazHfzRhWldgg0L0G-k/view?usp=sharing

# jt2026-vinicius-azevedo

Recomendação de investimento imobiliário para a Seazone, com base em dados reais de Airbnb e VivaReal para Itapema (SC). Desafio: [Jovens Talentos AI Builder 2026](https://seazone-tech.github.io/jovens-talentos-2026-hackathon-data/).

## Onde está a resposta

A recomendação final está em dois documentos que devem ser lidos em conjunto:

1. **[`relatorio.md`](./relatorio.md)** — responde às 4 perguntas do desafio (perfil ideal, localização, drivers de receita, o que comprar) e a posição sobre a tese dos compactos no Centro.
2. **[`REVISAO_E_RECOMENDACAO_REVISADA.md`](./REVISAO_E_RECOMENDACAO_REVISADA.md)** — revisão crítica que testa a conclusão e valida, para uma **decisão de aquisição de imóvel pronto**, a compra de **2 quartos em Morretes** (melhor retorno sobre o capital) — com o compacto de Meia Praia como alternativa mais líquida. Inclui os anúncios reais de mercado que ancoram a solução.

As fontes e premissas de cada número estão em **[`FONTES_E_PREMISSAS.md`](./FONTES_E_PREMISSAS.md)**.

## Estrutura do repositório

```
.
├── README.md              <- este arquivo
├── relatorio.md            <- as 4 perguntas do desafio (comece por aqui)
├── REVISAO_E_RECOMENDACAO_REVISADA.md   <- revisão crítica da recomendação de compra (2Q Morretes)
├── FONTES_E_PREMISSAS.md   <- de onde vem cada número da solução
├── PITCH_3MIN_FINAL_v5.md  <- roteiro final do vídeo (aquisição de 2Q em Morretes)
├── Pitch_Seazone_3min.pptx <- apresentação de slides de apoio para o vídeo (13 slides)
├── COMO_CHEGAMOS_AS_ESTIMATIVAS.md <- resumo curto de onde veio cada número
├── analise/                <- código da análise (execute em ordem)
│   ├── 01_build_dataset.py            junta as 5 bases, calcula ADR/ocupação proxy por anúncio
│   ├── 02_analysis.py                 perfil ideal, localização, drivers de receita
│   ├── 03_thesis_and_vivareal.py      testa a tese studio/Centro, cruza com preços do VivaReal, calcula yield
│   ├── 04_roi_model.py                modelo financeiro detalhado (capex, DRE, financiamento)
│   ├── 05_roi_model_v2.py             ROI revisado (limpeza/taxa Airbnb como repasse ao hóspede)
│   ├── 06_amenities_condominio.py     quais instalações de condomínio maximizam receita/yield
│   ├── 07_receita_revisada_e_roi_final.py   consolidação: receita revisada + resumo dos cenários de ROI
│   ├── 08_revisao_critica.py          testes que tentam derrubar a recomendação (bootstrap, sensibilidade)
│   ├── 09_spot_receita_por_m2.py      receita por m² construído -> produto ótimo p/ um SPOT
│   ├── 10_spot_proforma.py            pro-forma: construir SPOT vs comprar pronto (3 cenários + break-even, round 2)
│   ├── 11_gerar_charts.py             regenera os 2 gráficos do relatório
│   ├── data/               5 CSVs originais do desafio (renomeados) — entrada dos scripts
│   └── outputs/             tabelas (.csv) e gráficos (.png) gerados pelos scripts acima
└── ai-log/
    └── conversa-completa.md   log completo da conversa com a IA usada no processo (texto integral)
```

## Como rodar

Requer Python 3 com `pandas`, `numpy` e `matplotlib`:

```bash
pip install pandas numpy matplotlib
```

Coloque os 5 CSVs originais do desafio na pasta `analise/data/`, renomeados para `details.csv`, `hosts.csv`, `mesh.csv`, `price.csv` e `vivareal.csv` (já vêm inclusos nesta entrega). Depois rode em ordem:

```bash
cd analise
python3 01_build_dataset.py
python3 02_analysis.py
python3 03_thesis_and_vivareal.py
python3 04_roi_model.py
python3 05_roi_model_v2.py
python3 06_amenities_condominio.py
python3 07_receita_revisada_e_roi_final.py
python3 08_revisao_critica.py
python3 09_spot_receita_por_m2.py
python3 10_spot_proforma.py
python3 11_gerar_charts.py
```

Cada script imprime seus resultados no terminal e salva tabelas de apoio em `outputs/`. Os números citados em `relatorio.md` vêm diretamente dessas execuções.

## Principais premissas (documentadas com fonte em `relatorio.md`, Seção 8)

- ADR e ocupação são estimados a partir do calendário de preços futuros (`Price_AV_Itapema.csv`), não de dados diretos de reserva.
- Custos de aquisição, mobília, gestão e financiamento vêm de pesquisa de mercado (taxas de mercado brasileiras 2025/2026), com incerteza sinalizada onde não há dado local confirmado.
- A comparação com a Seazone usa apenas dados públicos do site institucional da empresa (`seazone.com.br`) — não há acesso a dados internos.

## IA no processo

Todo o processo — cruzamento das bases, construção dos modelos financeiros, pesquisa de premissas de mercado, verificação independente dos cálculos e pesquisa do catálogo da Seazone para comparação — foi feito com apoio de IA. O histórico completo da conversa está em [`ai-log/conversa-completa.md`](./ai-log/conversa-completa.md).
