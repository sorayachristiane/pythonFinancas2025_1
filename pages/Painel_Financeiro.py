import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Título do dashboard
st.title("📈 Painel Financeiro - Últimos 5 anos")

# Barra lateral para seleção do ativo
opcao = st.sidebar.radio(
    "Selecione o ativo:",
    ("Ibovespa", "PETR4", "VALE3")
)

# Dicionário de mapeamento
mapa_tickers = {
    "Ibovespa": "^BVSP",
    "PETR4": "PETR4.SA",
    "VALE3": "VALE3.SA"
}

# Determina o ticker com base na seleção
ticker_selecionado = mapa_tickers[opcao]

# Datas para consulta
data_fim = datetime.today()
data_inicio = data_fim - timedelta(days=5*365)

# Mensagem de carregamento
st.write(f"Carregando dados de **{opcao}**...")

# Baixando os dados
dados = yf.download(ticker_selecionado, start=data_inicio, end=data_fim)

# Verificação se os dados foram carregados
if dados.empty:
    st.error(f"Não foi possível carregar os dados de {opcao}.")
else:
    # Exibe os dados em tabela
    st.subheader(f"📊 Dados Históricos - {opcao}")
    st.dataframe(dados.tail())

    # Gráfico de preços de fechamento
    st.subheader(f"📉 Gráfico de Fechamento - {opcao}")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dados.index, dados['Close'], color='blue')
    ax.set_title(f"Preço de Fechamento - {opcao} (5 anos)", fontsize=14)
    ax.set_xlabel("Data")
    ax.set_ylabel("Preço (BRL)")
    ax.grid(True)
    st.pyplot(fig)
