# Análise de preços de ações com RSI

Projeto de análise de dados financeiros (2024): baixa o histórico de preços de uma ação da B3, calcula o **Índice de Força Relativa (RSI)** e classifica cada pregão como sinal de compra, venda ou manutenção, com gráficos do preço e do indicador.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Stramasso/Projeto-Day-Trading-com-Python-Machine-Learning-2024-/blob/main/analise_rsi.ipynb)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

## Como funciona

1. **Coleta**: preços de fechamento ajustados por proventos via [yfinance](https://github.com/ranaroussi/yfinance) (padrão: `CXSE3.SA`, últimos 2 anos)
2. **RSI**: média dos ganhos dividida pela média das perdas numa janela de 14 pregões, com a suavização de Wilder
3. **Sinais**: RSI abaixo de 30 indica ativo sobrevendido (**comprar**), acima de 70 sobrecomprado (**vender**), e entre os dois **manter**
4. **Visualização**: preço com os sinais marcados e RSI com as faixas de 30 e 70

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| [`analise_rsi.ipynb`](analise_rsi.ipynb) | Passo a passo comentado, pronto para rodar no Colab |
| [`rsi_analise.py`](rsi_analise.py) | Mesma análise em script, com parâmetros pela linha de comando |

## Como executar

```bash
pip install -r requirements.txt

python rsi_analise.py                                   # CXSE3.SA, últimos 2 anos
python rsi_analise.py PETR4.SA --inicio 2023-01-01      # outro ativo e outra data inicial
python rsi_analise.py VALE3.SA --periodo 9              # janela do RSI diferente
```

## Limitações e próximos passos

- O RSI sozinho não é uma estratégia de investimento: em tendências fortes o ativo pode passar muito tempo sobrecomprado ou sobrevendido.
- Ainda não há backtest. O próximo passo é medir o retorno de seguir os sinais, com custos de operação, contra simplesmente manter o ativo.

Projeto de estudo, sem recomendação de investimento.
