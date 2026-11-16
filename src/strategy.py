import pandas as pd
from .config import CONFIG


class HestonGarchStrategy:
    def __init__(self, config=CONFIG):
        self.config = config

    def generate_positions(self, df):
        # Filtro de tendência
        bullish = df["EMA_7"] > df["EMA_21"]
        z_uni = df["Z_Score_Unified"]

        pos_bh = pd.Series(1, index=df.index)
        pos_meta = pd.Series(0, index=df.index)

        # Regras de decisão
        for idx in df.index:
            if z_uni.loc[idx] > self.config["z_panic"]:
                pos_meta.loc[idx] = 0  # Saída por pânico
            elif bullish.loc[idx]:
                pos_meta.loc[idx] = 1  # Compra na tendência
            else:
                pos_meta.loc[idx] = 0  # Fora da bolsa

        return {
            "Buy & Hold": pos_bh,
            "Meta-Estratégia Heston-GARCH": pos_meta
        }
