"""Análise de preços de ações com o Índice de Força Relativa (RSI).

Baixa o histórico de preços de um ativo pelo yfinance, calcula o RSI,
classifica cada pregão em Comprar / Vender / Manter e gera dois gráficos:
preço com os sinais marcados e RSI com as faixas de sobrecompra e sobrevenda.

Uso:
    python rsi_analise.py                       # CXSE3.SA, últimos 2 anos
    python rsi_analise.py PETR4.SA --inicio 2023-01-01 --periodo 14
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd

SOBREVENDIDO = 30
SOBRECOMPRADO = 70


def baixar_precos(ativo: str, inicio: str | None = None, periodo_hist: str = "2y") -> pd.Series:
    """Retorna a série de preços de fechamento ajustados do ativo."""
    import yfinance as yf

    if inicio:
        dados = yf.download(ativo, start=inicio, auto_adjust=True, progress=False)
    else:
        dados = yf.download(ativo, period=periodo_hist, auto_adjust=True, progress=False)

    if dados.empty:
        raise ValueError(f"Nenhum dado encontrado para {ativo}.")

    fechamento = dados["Close"]
    # versões recentes do yfinance devolvem colunas multinível (uma por ticker)
    if isinstance(fechamento, pd.DataFrame):
        fechamento = fechamento.iloc[:, 0]
    return fechamento.rename("Preco").dropna()


def calcular_rsi(precos: pd.Series, periodo: int = 14) -> pd.Series:
    """RSI pela suavização de Wilder (média móvel exponencial com alpha = 1/periodo)."""
    variacao = precos.diff()
    ganhos = variacao.clip(lower=0)
    perdas = -variacao.clip(upper=0)

    media_ganhos = ganhos.ewm(alpha=1 / periodo, min_periods=periodo, adjust=False).mean()
    media_perdas = perdas.ewm(alpha=1 / periodo, min_periods=periodo, adjust=False).mean()

    rs = media_ganhos / media_perdas
    rsi = 100 - 100 / (1 + rs)
    # sem perdas no período o RSI é 100 por definição
    rsi = rsi.where(media_perdas != 0, 100)
    return rsi.where(media_ganhos.notna()).rename("RSI")


def classificar_sinal(rsi: float) -> str:
    if rsi < SOBREVENDIDO:
        return "Comprar"
    if rsi > SOBRECOMPRADO:
        return "Vender"
    return "Manter"


def montar_tabela(precos: pd.Series, periodo: int = 14) -> pd.DataFrame:
    tabela = pd.concat([precos, calcular_rsi(precos, periodo)], axis=1).dropna()
    tabela["Sinal"] = tabela["RSI"].apply(classificar_sinal)
    return tabela


def plotar(tabela: pd.DataFrame, ativo: str) -> None:
    fig, (ax_preco, ax_rsi) = plt.subplots(
        2, 1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [2, 1]}
    )

    ax_preco.plot(tabela.index, tabela["Preco"], color="#1f4e79", linewidth=1.2, label="Preço ajustado")
    compras = tabela[tabela["Sinal"] == "Comprar"]
    vendas = tabela[tabela["Sinal"] == "Vender"]
    ax_preco.scatter(compras.index, compras["Preco"], marker="^", color="#2e7d32", label="Sinal de compra", zorder=3)
    ax_preco.scatter(vendas.index, vendas["Preco"], marker="v", color="#c62828", label="Sinal de venda", zorder=3)
    ax_preco.set_title(f"{ativo}: preço e sinais pelo RSI")
    ax_preco.set_ylabel("Preço (R$)")
    ax_preco.legend(loc="upper left")
    ax_preco.grid(alpha=0.3)

    ax_rsi.plot(tabela.index, tabela["RSI"], color="#6a1b9a", linewidth=1)
    ax_rsi.axhline(SOBRECOMPRADO, linestyle="--", color="#c62828", alpha=0.6, label=f"Sobrecomprado ({SOBRECOMPRADO})")
    ax_rsi.axhline(SOBREVENDIDO, linestyle="--", color="#2e7d32", alpha=0.6, label=f"Sobrevendido ({SOBREVENDIDO})")
    ax_rsi.set_ylim(0, 100)
    ax_rsi.set_ylabel("RSI")
    ax_rsi.legend(loc="upper left")
    ax_rsi.grid(alpha=0.3)

    fig.tight_layout()
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Sinais de compra e venda pelo RSI.")
    parser.add_argument("ativo", nargs="?", default="CXSE3.SA", help="ticker no Yahoo Finance (padrão: CXSE3.SA)")
    parser.add_argument("--inicio", help="data inicial no formato AAAA-MM-DD (padrão: últimos 2 anos)")
    parser.add_argument("--periodo", type=int, default=14, help="janela do RSI em pregões (padrão: 14)")
    args = parser.parse_args()

    tabela = montar_tabela(baixar_precos(args.ativo, args.inicio), args.periodo)

    print(tabela.tail(10).round(2).to_string())
    print("\nContagem de sinais no período:")
    print(tabela["Sinal"].value_counts().to_string())

    ultimo = tabela.iloc[-1]
    print(f"\nÚltimo pregão ({tabela.index[-1]:%d/%m/%Y}): RSI {ultimo['RSI']:.1f} -> {ultimo['Sinal']}")

    plotar(tabela, args.ativo)


if __name__ == "__main__":
    main()
