import numpy as np
import pandas as pd
from arch import arch_model
from .config import CONFIG


class HestonModel:
    def __init__(self, config=CONFIG):
        self.config = config

    def estimate(self, returns, params):
        # Semente fixa
        np.random.seed(self.config["seed"])
        n_days = len(returns)
        dt = 1.0 / 252.0
        horizon = self.config["heston_horizon_days"]
        n_sims = self.config["heston_sims"]

        kappa = params["kappa"]
        theta = params["theta"]
        sigma = params["sigma"]

        # Variância histórica 21d
        rolling_vol = returns.rolling(window=21).std() * np.sqrt(252)
        rolling_var = (rolling_vol.fillna(np.sqrt(theta)) ** 2).values

        heston_vol = np.zeros(n_days)
        Z = np.random.normal(0.0, 1.0, size=(horizon, n_sims))

        # Simulação Monte Carlo
        for t in range(n_days):
            v_paths = np.full(n_sims, max(rolling_var[t], 1e-6))
            for step in range(horizon):
                drift = kappa * (theta - v_paths) * dt
                diffusion = sigma * np.sqrt(np.maximum(v_paths, 1e-6)) * np.sqrt(dt) * Z[step]
                v_paths = np.maximum(v_paths + drift + diffusion, 1e-6)
            heston_vol[t] = np.sqrt(np.mean(v_paths)) * 100.0

        return pd.Series(heston_vol, index=returns.index)


class GarchModel:
    def __init__(self, config=CONFIG):
        self.config = config

    def estimate(self, log_returns):
        window = self.config["garch_window"]
        n = len(log_returns)
        garch_vol = np.zeros(n)

        scaled_rets = log_returns.values * 100.0
        sample_std = float(np.std(scaled_rets[:window]) * np.sqrt(252))
        last_sigma = sample_std

        # Janela móvel 250d
        for t in range(n):
            if t < window:
                garch_vol[t] = sample_std
                continue

            window_rets = scaled_rets[t - window:t]
            try:
                am = arch_model(window_rets, vol="Garch", p=1, q=1, mean="Constant", dist="normal", rescale=False)
                res = am.fit(disp="off", show_warning=False)
                var_next = res.forecast(horizon=1).variance.values[-1, 0]
                vol_ann = np.sqrt(var_next * 252.0)
                if np.isnan(vol_ann) or vol_ann <= 0.0 or vol_ann > 250.0:
                    vol_ann = last_sigma
            except Exception:
                vol_ann = last_sigma

            last_sigma = vol_ann
            garch_vol[t] = vol_ann

        return pd.Series(garch_vol, index=log_returns.index)
