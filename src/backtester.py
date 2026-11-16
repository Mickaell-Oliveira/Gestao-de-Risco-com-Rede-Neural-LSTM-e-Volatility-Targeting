import numpy as np
import pandas as pd
from .config import CONFIG
from .strategy import HestonGarchStrategy


class Backtester:
    def __init__(self, config=CONFIG):
        self.config = config
        self.strategy = HestonGarchStrategy(config)

    def run(self, df):
        raw_positions = self.strategy.generate_positions(df)

        # Corte após 2018
        mask = df.index >= self.config["start_backtest"]
        df_eval = df.loc[mask].copy()
        market_returns = df_eval["Returns"]

        results = {}
        for name, pos in raw_positions.items():
            pos_eval = pos.loc[mask]

            # Execução com atraso (1d)
            executed_pos = pos_eval.shift(1).fillna(0)
            trades = pos_eval.diff().ne(0)
            costs = self.config["op_cost"] * trades

            # Curva de capital
            strat_returns = (executed_pos * market_returns) - costs
            equity_curve = (1.0 + strat_returns).cumprod()

            results[name] = {
                "position": pos_eval,
                "executed_pos": executed_pos,
                "daily_returns": strat_returns,
                "equity_curve": equity_curve,
                "trades_count": int(trades.sum())
            }

        return df_eval, results

    def summarize(self, results, asset_name):
        rows = []
        for name, res in results.items():
            eq = res["equity_curve"]
            dr = res["daily_returns"]

            # Métricas de retorno
            total_ret = (eq.iloc[-1] - 1.0) * 100.0
            years = len(dr) / 252.0
            cagr = ((eq.iloc[-1]) ** (1.0 / years) - 1.0) * 100.0 if eq.iloc[-1] > 0 else -100.0

            # Métricas de risco
            vol_ann = dr.std() * np.sqrt(252) * 100.0
            sharpe = (dr.mean() / dr.std() * np.sqrt(252)) if dr.std() > 0 else 0.0
            max_dd = ((eq - eq.cummax()) / eq.cummax()).min() * 100.0

            rows.append({
                "Índice": asset_name,
                "Estratégia": name,
                "Retorno Total": f"{total_ret:.2f}%",
                "CAGR": f"{cagr:.2f}%",
                "Volatilidade": f"{vol_ann:.2f}%",
                "Sharpe": f"{sharpe:.2f}",
                "Max Drawdown": f"{max_dd:.2f}%",
                "Trades": res["trades_count"]
            })

        return pd.DataFrame(rows)
