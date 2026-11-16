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
