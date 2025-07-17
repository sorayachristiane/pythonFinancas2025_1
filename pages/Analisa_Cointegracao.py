import pandas as pd
import statsmodels.api as sm
import statsmodels.tsa.stattools as ts
import matplotlib.pyplot as plt
import streamlit as st

# 1. Carregar os dados CSV
def carregar_dados(caminho_csv='dados_acoes.csv'):
    data = pd.read_csv(caminho_csv, index_col=0, parse_dates=True)
    return data

# 2. Executa a regressão linear e o teste de cointegração entre 2 ativos
def analisar_relacao(ticker_y, ticker_x, data, titulo):
    y = data[ticker_y]
    x = data[ticker_x]
    x_ = sm.add_constant(x)
    model = sm.OLS(y, x_).fit()
    beta = model.params[1]
    alpha = model.params[0]
    spread = y - (beta * x + alpha)
    pvalor = ts.coint(y, x)[1]

    # Gráficos
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Gráfico 1: Séries com linha de regressão
    axes[0].plot(y, label=ticker_y)
    axes[0].plot(beta * x + alpha, label=f'{beta:.2f} * {ticker_x} + {alpha:.2f}', linestyle='--')
    axes[0].set_title(f'{titulo}\nRegressão: {ticker_y} ~ {ticker_x}')
    axes[0].legend()
    axes[0].grid(True)

    # Gráfico 2: Spread (resíduo)
    axes[1].plot(spread, label='Spread')
    axes[1].axhline(spread.mean(), color='black', linestyle='--', label='Média do spread')
    axes[1].set_title(f'Spread da Regressão\np-valor da cointegração: {pvalor:.4f}')
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    return fig, pvalor, alpha, beta

# 3. Interface Streamlit
def main():
    st.title("Análise de Cointegração entre Ações")
    dados = carregar_dados('dados_acoes.csv')
    colunas = list(dados.columns)

    st.write("Selecione dois ativos para analisar a relação de cointegração:")

    ticker_y = st.selectbox("Ativo Y (dependente)", colunas, index=0)
    ticker_x = st.selectbox("Ativo X (independente)", colunas, index=1 if len(colunas) > 1 else 0)
    titulo = st.text_input("Título para o gráfico", "Análise de Cointegração")

    if st.button("Analisar"):
        if ticker_y == ticker_x:
            st.warning("Selecione ativos diferentes para a análise.")
        else:
            fig, pvalor, alpha, beta = analisar_relacao(ticker_y, ticker_x, dados, titulo)
            st.pyplot(fig)
            st.write(f"**p-valor do teste de cointegração:** {pvalor:.4f}")
            st.write(f"**Regressão:** {ticker_y} = {beta:.4f} * {ticker_x} + {alpha:.4f}")

    st.write("Colunas disponíveis no arquivo CSV:")
    st.write(colunas)

if __name__ == "__main__":
    main()