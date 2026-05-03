# quant-system-research-log
## EN

Versioned log of research in quantitative trading systems, statistical modeling, and algorithmic execution design. Each entry documents hypotheses, system changes, empirical tests, and statistical evaluation of market behavior.

### Scope

Research focuses on intraday and multi-regime market systems using rule-based and data-driven models. Emphasis is placed on:

market structure modeling using Fibonacci-based levels
regime detection via volatility and distributional features
execution logic in algorithmic trading systems
statistical validation of system behavior over time

This repository is not a trade journal. It is a structured record of system development and quantitative experimentation.

### Tools

* MetaTrader 5 for execution and data collection
* Python for statistical analysis and modeling
* Jupyter Notebook for reproducible experiments

### Structure

* `/posts/` research notes in Markdown
* `/notebooks/` experimental and statistical analysis
* `/data/` raw and processed datasets
* `/results/` aggregated outputs and metrics

### Research format

Each entry follows a structured experimental format:

* System state: description of current model version
* Hypothesis: statistical or behavioral assumption being tested
* Experiment: dataset, period, and configuration
* Metrics: expected value, variance, drawdown, distributional 
### properties

* Result: observed behavior under test conditions
* Model update: changes applied to system logic
* Limitations: known constraints and failure cases

### Naming convention

`Diario_de_bordo_YYYY-MM-DD.md`

Example:
Diario_de_Bordo_20260503.md

### Core metrics
* expected value per trade and per day
* standard deviation of returns
* maximum drawdown of equity curve
* trade frequency per regime
* distribution of outcomes under volatility filters
* proportion of truncated or constrained sessions

### Reproducibility

All conclusions must be backed by executable code in /notebooks/ or equivalent scripts. Parameters and assumptions must be explicitly defined.

---

## PT-BR

Registro versionado de pesquisa em sistemas quantitativos, modelagem estatística e desenvolvimento de lógica para trading algorítmico. Cada entrada documenta hipóteses, mudanças no sistema, testes empíricos e avaliação estatística do comportamento do mercado.

### Escopo

A pesquisa foca em sistemas intraday e multirregime com base em regras e modelos estatísticos. Ênfase em:

modelagem de estrutura de mercado com níveis de Fibonacci
detecção de regimes via volatilidade e distribuição
lógica de execução em sistemas algorítmicos
validação estatística de comportamento do sistema

Este repositório não é um diário operacional de trades. É um registro estruturado de desenvolvimento de sistemas quantitativos.

### Ferramentas

MetaTrader 5 para execução e coleta de dados
Python para análise estatística e modelagem
Jupyter Notebook para experimentos reproduzíveis

### Estrutura

* `/posts/` notas de pesquisa
* `/notebooks/` análises e experimentos
* `/data/ dados` brutos e tratados
* `/results/` resultados agregados e métricas

### Formato das entradas

* Estado do sistema
* Hipótese testada
* Experimento realizado
* Métricas estatísticas
* Resultado observado
* Atualização do modelo
* Limitações

### Convenção de nomes

`Diario_de_bordo_YYYY-MM-DD.md`

Examplo:
Diario_de_Bordo_20260503.md

### Métricas padrão
* valor esperado por trade e por dia
* desvio padrão dos retornos
* drawdown máximo
* frequência de trades por regime
* distribuição dos resultados sob filtros de volatilidade
* proporção de sessões truncadas

### Reprodutibilidade

Toda conclusão deve ser suportada por código executável em /notebooks/ ou scripts equivalentes. Parâmetros e suposições devem estar explícitos.
