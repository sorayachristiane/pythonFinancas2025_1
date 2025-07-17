# salvar_dados.py

import yfinance as yf
import pandas as pd

# Lista de tickers (ações da B3 no Yahoo Finance)
tickers = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA']

def baixar_dados(tickers, start='2020-01-01', end='2024-12-31'):
    print("⏳ Baixando os dados do Yahoo Finance...")
    data = yf.download(tickers, start=start, end=end, group_by='ticker', auto_adjust=True)
    
    # Extraindo somente os fechamentos ajustados (Close)
    dados_fechamento = pd.DataFrame({
        ticker: data[ticker]['Close'] for ticker in tickers if ticker in data.columns
    })

    # Remover linhas com valores nulos
    dados_fechamento = dados_fechamento.dropna()

    # Salvar como CSV
    dados_fechamento.to_csv('dados_acoes.csv')
    print("✅ Dados salvos em: dados_acoes.csv")

baixar_dados(tickers)