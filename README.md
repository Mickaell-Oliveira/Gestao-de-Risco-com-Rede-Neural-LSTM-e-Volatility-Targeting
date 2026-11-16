# Gestão de Risco com Rede Neural LSTM e Volatility Targeting

Projeto desenvolvido para a disciplina **Trabalhos Multidisciplinares (MAC035 — DCC/UFJF)**.

**Discentes:** Caio Augusto de Paiva, Felipe Sachetto, Mickaell de Oliveira  
**Docentes:** Profa. Flavia Bastos, Prof. Rodrigo Weber  

---

## Estrutura do Repositório

```text
├── dados/           # Cotações históricas cacheadas (S&P 500 e Ibovespa)
├── notebooks/       # Notebooks enxutos que consomem o código modular
├── resultados/      # Gráficos gerados em alta resolução (300 DPI)
├── src/             # Código-fonte modularizado em classes Python
│   ├── config.py        # Parâmetros gerais e calibração por índice
│   ├── data_loader.py   # Leitura em cache local e download Yahoo Finance
│   ├── volatility.py    # Modelos Heston (Monte Carlo) e GARCH(1,1)
│   ├── indicators.py    # Consenso de volatilidade, Z-Score e EMAs
│   ├── strategy.py      # Regras de decisão e Panic Override
│   ├── backtester.py    # Motor de simulação sem look-ahead e métricas
│   └── plotter.py       # Geração de gráficos comparativos
└── main.py          # Script principal de execução da Fase 1
```

---

## Resultados da Fase 1 (2018 – 2025)

Comparativo direto da **Meta-Estratégia Heston-GARCH** (melhor abordagem do estudo de 2025) contra o benchmark **Buy & Hold**:

| Índice | Estratégia | Retorno Total | CAGR | Volatilidade | Sharpe | Max Drawdown | Trades |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **S&P 500** (`^GSPC`) | Buy & Hold | 146.22% | 12.30% | 19.77% | 0.69 | -33.92% | 1 |
| **S&P 500** (`^GSPC`) | **Meta-Estratégia Heston-GARCH** | **81.37%** | **7.97%** | **11.04%** | **0.75** | **-14.92%** | 106 |
| **Ibovespa** (`^BVSP`) | Buy & Hold | 81.72% | 8.09% | 23.55% | 0.45 | -46.82% | 1 |
| **Ibovespa** (`^BVSP`) | **Meta-Estratégia Heston-GARCH** | **29.12%** | **3.38%** | **13.54%** | **0.31** | **-25.77%** | 130 |

---

## Como Executar

1. Instale as dependências:
   ```bash
   pip install numpy pandas matplotlib yfinance arch
   ```
2. Execute o pipeline principal:
   ```bash
   python main.py
   ```
   Ou utilize o notebook modular em `notebooks/Fase1_Baseline.ipynb`.
