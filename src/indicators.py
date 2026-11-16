from .config import CONFIG
from .volatility import HestonModel, GarchModel


class RiskIndicators:
    def __init__(self, config=CONFIG):
        self.config = config
        self.heston = HestonModel(config)
        self.garch = GarchModel(config)

    def compute(self, df, params):
        df = df.copy()

        # Previsões de volatilidade
        df["Heston_Vol"] = self.heston.estimate(df["Returns"], params)
        df["GARCH_Vol"] = self.garch.estimate(df["Log_Returns"])

        # Consenso dos modelos
        df["Vol_Consensus"] = (df["Heston_Vol"] + df["GARCH_Vol"]) / 2.0

        # Z-Score móvel 21d
        w = self.config["zscore_window"]
        mean_c = df["Vol_Consensus"].rolling(w).mean()
        std_c = df["Vol_Consensus"].rolling(w).std()
        df["Z_Score_Unified"] = (df["Vol_Consensus"] - mean_c) / std_c

        # Médias exponenciais
        df["EMA_7"] = df["Close"].ewm(span=7, adjust=False).mean()
        df["EMA_21"] = df["Close"].ewm(span=21, adjust=False).mean()

        return df
