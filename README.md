# Python para Finanças 2025.1

Este repositório contém um conjunto de aplicações interativas desenvolvidas em Python utilizando Streamlit, voltadas para análise e visualização de dados financeiros. O projeto inclui painéis para acompanhamento de ativos da bolsa, análise de fundos de investimento e estudo de cointegração entre ações, facilitando a exploração de dados históricos e métricas relevantes do mercado financeiro brasileiro.

## Painel Financeiro (`pages/Painel_Financeiro.py`)

O Painel Financeiro permite ao usuário visualizar dados históricos dos principais ativos da bolsa brasileira, como Ibovespa, PETR4 e VALE3, nos últimos cinco anos. Através de gráficos interativos e tabelas, é possível acompanhar o desempenho dos ativos, facilitando a análise de tendências e movimentos do mercado.

## Ranking de Fundos de Investimento (`pages/Pagina_Fundos.py`)

Esta página apresenta um ranking dos melhores fundos de investimento com base em critérios como número de cotistas, classe do fundo e indicadores de desempenho ajustados ao CDI. O usuário pode filtrar o período de análise, a quantidade de fundos exibidos e outras características, além de visualizar métricas como Sharpe Ratio e drawdown para cada fundo selecionado.

## Analisa Cointegração (`pages/Analisa_Cointegracao.py`)

A página de Análise de Cointegração permite ao usuário investigar a relação estatística de longo prazo entre dois ativos distintos. Utilizando regressão linear e testes de cointegração, a aplicação gera gráficos e estatísticas que ajudam a identificar pares de ativos com comportamento correlacionado, útil para estratégias de pairs trading e diversificação.