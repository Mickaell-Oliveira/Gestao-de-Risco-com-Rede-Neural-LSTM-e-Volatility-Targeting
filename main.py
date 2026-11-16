import pandas as pd
from src import (
    ASSET_PARAMS,
    MarketDataLoader,
    RiskIndicators,
    Backtester,
    ResultPlotter
)


def run_asset_pipeline(ticker, loader, indicators, backtester):
    params = ASSET_PARAMS[ticker]
    print(f"Processando {params['name']} ({ticker})...")

    # Carga e indicadores
    df = loader.load(ticker)
    df = indicators.compute(df, params)

    # Simulação e métricas
    df_eval, results = backtester.run(df)
    summary = backtester.summarize(results, params["name"])
    return df_eval, results, summary


def main():
    loader = MarketDataLoader()
    indicators = RiskIndicators()
    backtester = Backtester()
    plotter = ResultPlotter()

    # Execução por índice
    sp_df, sp_res, sp_table = run_asset_pipeline("^GSPC", loader, indicators, backtester)
    ib_df, ib_res, ib_table = run_asset_pipeline("^BVSP", loader, indicators, backtester)

    # Tabela consolidada
    comparison = pd.concat([sp_table, ib_table], ignore_index=True)
    print("\n" + "=" * 88)
    print("COMPARATIVO FASE 1: S&P 500 vs. IBOVESPA (2018 - 2025)")
    print("=" * 88)
    print(comparison.to_string(index=False))
    print("=" * 88)

    # Gráficos
    plotter.plot_comparison(sp_res, ib_res)
    plotter.plot_panic_override(ib_df, ib_res)
    print("\nGráficos atualizados na pasta 'resultados/'.")


if __name__ == "__main__":
    main()
