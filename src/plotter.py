import os
import tempfile
import matplotlib.pyplot as plt
from .config import CONFIG, RESULTS_DIR


class ResultPlotter:
    def __init__(self, output_dir=RESULTS_DIR, config=CONFIG):
        self.output_dir = output_dir
        self.config = config
        plt.style.use("seaborn-v0_8-darkgrid" if "seaborn-v0_8-darkgrid" in plt.style.available else "default")

    def plot_comparison(self, sp500_res, ibov_res, show=False):
        fig, ax = plt.subplots(figsize=(12, 5))

        # Curvas de retorno
        sp_ret = (sp500_res["Meta-Estratégia Heston-GARCH"]["equity_curve"] - 1.0) * 100.0
        ib_ret = (ibov_res["Meta-Estratégia Heston-GARCH"]["equity_curve"] - 1.0) * 100.0
        sp_bh = (sp500_res["Buy & Hold"]["equity_curve"] - 1.0) * 100.0
        ib_bh = (ibov_res["Buy & Hold"]["equity_curve"] - 1.0) * 100.0

        ax.plot(sp_ret.index, sp_ret, label=f"Meta-Estratégia S&P 500 ({sp_ret.iloc[-1]:.1f}%)", color="#1f77b4", linewidth=2.2)
        ax.plot(ib_ret.index, ib_ret, label=f"Meta-Estratégia Ibovespa ({ib_ret.iloc[-1]:.1f}%)", color="#2ca02c", linewidth=2.2)
        ax.plot(sp_bh.index, sp_bh, label=f"Buy & Hold S&P 500 ({sp_bh.iloc[-1]:.1f}%)", color="#1f77b4", linestyle="--", alpha=0.5)
        ax.plot(ib_bh.index, ib_bh, label=f"Buy & Hold Ibovespa ({ib_bh.iloc[-1]:.1f}%)", color="#2ca02c", linestyle="--", alpha=0.5)

        ax.set_title("Comparativo de Rentabilidade: S&P 500 vs. Ibovespa (2018 - 2025)", fontsize=12, weight="bold")
        ax.set_xlabel("Ano")
        ax.set_ylabel("Retorno Acumulado (%)")
        ax.axhline(0, color="black", linewidth=0.8, linestyle=":")
        ax.legend(loc="upper left")
        plt.tight_layout()

        self._save(fig, "grafico_comparativo_sp500_ibov.png")
        if show:
            plt.show()
        plt.close(fig)

    def plot_panic_override(self, ibov_df, ibov_res, show=False):
        # Recorte COVID-19
        mask = (ibov_df.index >= "2019-10-01") & (ibov_df.index <= "2020-07-01")
        df_c = ibov_df.loc[mask].copy()
        pos_c = ibov_res["Meta-Estratégia Heston-GARCH"]["position"].loc[mask]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]})

        # Painel de preços
        ax1.plot(df_c.index, df_c["Close"], label="Ibovespa", color="black", linewidth=1.4)
        ax1.plot(df_c.index, df_c["EMA_7"], label="EMA 7", color="blue", linestyle="--")
        ax1.plot(df_c.index, df_c["EMA_21"], label="EMA 21", color="orange", linestyle="--")
        ax1.fill_between(df_c.index, df_c["Close"].min() * 0.95, df_c["Close"].max() * 1.05,
                         where=(pos_c == 1), color="green", alpha=0.15, label="Comprado (Long)")
        ax1.fill_between(df_c.index, df_c["Close"].min() * 0.95, df_c["Close"].max() * 1.05,
                         where=(pos_c == 0), color="red", alpha=0.15, label="Panic Override (Proteção)")
        ax1.set_title("Proteção na Crise de 2020: Ibovespa e Panic Override", fontsize=12, weight="bold")
        ax1.set_ylabel("Pontos")
        ax1.legend(loc="lower left", fontsize=9)

        # Painel do Z-score
        ax2.plot(df_c.index, df_c["Z_Score_Unified"], label="Z-Score Unificado", color="purple", linewidth=1.4)
        ax2.axhline(self.config["z_panic"], color="red", linestyle="--", label=f"Pânico (Z = {self.config['z_panic']})")
        ax2.axhline(self.config["z_calm"], color="green", linestyle=":", label=f"Calma (Z = {self.config['z_calm']})")
        ax2.axhline(0, color="grey", linewidth=0.8)
        ax2.set_ylabel("Z-Score")
        ax2.set_xlabel("Data")
        ax2.legend(loc="upper left", fontsize=9)

        plt.tight_layout()
        self._save(fig, "grafico_panic_override_2020.png")
        if show:
            plt.show()
        plt.close(fig)

    def _save(self, fig, filename):
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, filename)
        try:
            fig.savefig(path, dpi=300)
        except PermissionError:
            fallback = os.path.join(tempfile.gettempdir(), filename)
            fig.savefig(fallback, dpi=300)
