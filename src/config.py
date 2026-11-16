import os

# Diretórios do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "dados")
RESULTS_DIR = os.path.join(BASE_DIR, "resultados")

# Parâmetros gerais
CONFIG = {
    "start_burnin": "2017-01-01",   # Aquecimento de janelas
    "start_backtest": "2018-01-01", # Início do backtest
    "end_date": "2025-10-15",       # Data final
    "op_cost": 0.001,               # Custo por trade (0,1%)
    "z_calm": 0.5,                  # Limiar de calma
    "z_panic": 1.8,                 # Gatilho de pânico
    "heston_sims": 300,             # Trajetórias Monte Carlo
    "heston_horizon_days": 30,      # Horizonte Heston (dias)
    "garch_window": 250,            # Janela GARCH (1 ano)
    "zscore_window": 21,            # Janela Z-score (1 mês)
    "seed": 42                      # Semente fixa
}

# Parâmetros por ativo
ASSET_PARAMS = {
    "^GSPC": {
        "name": "S&P 500",
        "kappa": 2.5,     # Reversão à média
        "theta": 0.025,   # Variância longa (~15.8% vol)
        "sigma": 0.55,    # Vol da variância
        "rho": -0.50,     # Correlação
        "r": 0.02         # Juros EUA
    },
    "^BVSP": {
        "name": "Ibovespa",
        "kappa": 2.5,     # Reversão à média
        "theta": 0.060,   # Variância longa (~24.5% vol)
        "sigma": 0.55,    # Vol da variância
        "rho": -0.50,     # Correlação
        "r": 0.10         # Juros Brasil
    }
}
