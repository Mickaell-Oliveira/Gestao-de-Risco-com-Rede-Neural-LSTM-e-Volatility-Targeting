import os
import numpy as np
import pandas as pd
import yfinance as yf
from .config import DATA_DIR, CONFIG


class MarketDataLoader:
    def __init__(self, data_dir=DATA_DIR, config=CONFIG):
        self.data_dir = data_dir
        self.config = config

    def load(self, ticker):
        safe_ticker = ticker.replace("^", "")
        cache_path = os.path.join(self.data_dir, f"dados_{safe_ticker}.csv")
        df = self._read_cache(cache_path)

        # Download se necessário
        if df is None or df.empty:
            df = self._download(ticker, cache_path)

        close = self._extract_close(df, ticker)
        close = pd.to_numeric(close, errors="coerce").ffill().dropna()

        # Cálculo de retornos
        returns = close.pct_change().dropna()
        log_returns = np.log(close / close.shift(1)).dropna()

        return pd.DataFrame({
            "Close": close.loc[returns.index],
            "Returns": returns,
            "Log_Returns": log_returns
        })

    def _read_cache(self, path):
        if not (os.path.exists(path) and os.path.getsize(path) > 1000):
            return None
        try:
            return pd.read_csv(path, header=[0, 1], index_col=0, parse_dates=True)
        except Exception:
            try:
                return pd.read_csv(path, index_col=0, parse_dates=True)
            except Exception:
                return None

    def _download(self, ticker, cache_path):
        os.makedirs(self.data_dir, exist_ok=True)
        df = yf.download(
            ticker,
            start=self.config["start_burnin"],
            end=self.config["end_date"],
            auto_adjust=False,
            progress=False
        )
        if not df.empty:
            df.to_csv(cache_path)
        return df

    def _extract_close(self, df, ticker):
        if isinstance(df.columns, pd.MultiIndex):
            if ("Adj Close", ticker) in df.columns:
                return df[("Adj Close", ticker)]
            if ("Close", ticker) in df.columns:
                return df[("Close", ticker)]
            if "Close" in df.columns.levels[0]:
                return df["Close"].iloc[:, 0]
            return df.iloc[:, 0]

        if "Adj Close" in df.columns:
            return df["Adj Close"]
        if "Close" in df.columns:
            return df["Close"]
        return df.iloc[:, 0]
