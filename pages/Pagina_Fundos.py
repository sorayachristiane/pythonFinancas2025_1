import streamlit as st
import pyfolio as pf
import empyrical as ep
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from pandas.tseries.offsets import BDay

import sgs  # Importa o módulo sgs para acessar séries temporais do Banco Central
CDI_CODE = 12  # Código do CDI na SGS

import warnings
warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)

def busca_cadastro_cvm():
    try:
        url = 'cad_fi.csv'
        dados = pd.read_csv(url, sep=';', encoding='ISO-8859-1')
        return dados
    except:
        st.error(f"Arquivo {url} não encontrado!")
        return pd.DataFrame()

def busca_informes_diarios_cvm_por_periodo(data_inicio, data_fim):
    datas = pd.date_range(data_inicio, data_fim, freq='MS') 
    informe_completo = pd.DataFrame()
    for data in datas:
        try:
            url = 'inf_diario_fi_202501.zip'
            informe_mensal = pd.read_csv(url, compression='zip', sep=';')    
        except: 
            st.warning(f"Arquivo {url} não encontrado!")    
            continue
        informe_completo = pd.concat([informe_completo, informe_mensal], ignore_index=True)
    return informe_completo

def melhores_fundos(informes, cadastro, top=5, minimo_de_cotistas=100, classe='', CDI_periodo=0):
    cadastro = cadastro[cadastro['SIT'] == 'EM FUNCIONAMENTO NORMAL']
    fundos = informes[informes['NR_COTST'] >= minimo_de_cotistas]
    cnpj_informes = fundos['CNPJ_FUNDO_CLASSE'].drop_duplicates()
    fundos = fundos.drop_duplicates(subset=['DT_COMPTC', 'CNPJ_FUNDO_CLASSE'])
    fundos = fundos.pivot(index='DT_COMPTC', columns='CNPJ_FUNDO_CLASSE')
    cotas_normalizadas = fundos['VL_QUOTA'] / fundos['VL_QUOTA'].iloc[0]
    retornos_diarios = cotas_normalizadas.pct_change().dropna(axis=0, how='all')
    if classe == 'multimercado':
        cnpj_cadastro = cadastro[cadastro['CLASSE'] == 'Multimercado']['CNPJ_FUNDO']   
        cotas_normalizadas = cotas_normalizadas[cnpj_cadastro[cnpj_cadastro.isin(cnpj_informes)]]
    if classe == 'acoes':
        cnpj_cadastro = cadastro[cadastro['CLASSE'] == 'Ações']['CNPJ_FUNDO']   
        cotas_normalizadas = cotas_normalizadas[cnpj_cadastro[cnpj_cadastro.isin(cnpj_informes)]]
    if classe == 'rendafixa':
        cnpj_cadastro = cadastro[cadastro['CLASSE'] == 'Renda Fixa']['CNPJ_FUNDO']   
        cotas_normalizadas = cotas_normalizadas[cnpj_cadastro[cnpj_cadastro.isin(cnpj_informes)]]
    if classe == 'cambial':
        cnpj_cadastro = cadastro[cadastro['CLASSE'] == 'Cambial']['CNPJ_FUNDO']   
        cotas_normalizadas = cotas_normalizadas[cnpj_cadastro[cnpj_cadastro.isin(cnpj_informes)]]
    cotas_normalizadas = cotas_normalizadas.dropna(axis=0, how='all')
    melhores = pd.DataFrame()
    melhores['retorno(%)'] = (cotas_normalizadas.iloc[-1].sort_values(ascending=False)[:top] - 1) * 100
    for cnpj in melhores.index:
        fundo = cadastro[cadastro['CNPJ_FUNDO'] == cnpj]
        melhores.at[cnpj, 'Fundo de Investimento'] = fundo['DENOM_SOCIAL'].values[0]
        melhores.at[cnpj, 'Classe'] = fundo['CLASSE'].values[0]
        melhores.at[cnpj, 'PL'] = fundo['VL_PATRIM_LIQ'].values[0]
        melhores.at[cnpj, 'Drawdown(%)'] = pf.timeseries.gen_drawdown_table(retornos_diarios[cnpj], top=4)
        # Gráfico de drawdown
        fig, ax = plt.subplots()
        pf.plot_drawdown_underwater(retornos_diarios[cnpj], ax=ax, title="Drawdown:" + cnpj + " " + fundo['DENOM_SOCIAL'].values[0][:40] + "...")
        st.pyplot(fig)
        num_dias = len(retornos_diarios[cnpj])
        CDI_diario_periodo = (1 + CDI_periodo) ** (1/num_dias) - 1
        melhores.at[cnpj, 'Sharpe(CDI)'] = ep.sharpe_ratio(retornos_diarios[cnpj], risk_free=CDI_diario_periodo)
    return melhores

# ------------------- STREAMLIT APP -------------------
st.title("Ranking de Fundos de Investimento")

st.sidebar.header("Parâmetros")
periodo_inicio = st.sidebar.date_input("Data início", date(2025, 1, 1))
periodo_fim = st.sidebar.date_input("Data fim", date(2025, 1, 31))
NUM_FUNDOS = st.sidebar.slider("Quantidade de fundos", 1, 20, 5)
min_cotistas = st.sidebar.number_input("Mínimo de cotistas", 1, 1000, 100)
classe = st.sidebar.selectbox("Classe", ['', 'multimercado', 'acoes', 'rendafixa', 'cambial'])

if st.sidebar.button("Buscar e Analisar"):
    cadastro_fundos = busca_cadastro_cvm()
    if cadastro_fundos.empty:
        st.stop()
    diario_cvm = busca_informes_diarios_cvm_por_periodo(periodo_inicio.strftime("%Y-%m-%d"), periodo_fim.strftime("%Y-%m-%d"))
    if diario_cvm.empty:
        st.stop()
    st.info("Obtendo dados do CDI...")
    CDI_diario = sgs.time_serie(CDI_CODE, start=periodo_inicio.strftime("%d/%m/%Y"), end=periodo_fim.strftime("%d/%m/%Y"))
    CDI_diario = (CDI_diario/100)+1
    CDI_acumulado = CDI_diario.cumprod().iloc[-1]-1
    melhores = melhores_fundos(diario_cvm, cadastro_fundos, top=NUM_FUNDOS, minimo_de_cotistas=min_cotistas, classe=classe, CDI_periodo=CDI_acumulado)
    st.subheader("Melhores fundos de investimento")
    st.dataframe(melhores[['Fundo de Investimento', 'Classe', 'retorno(%)', 'PL', 'Sharpe(CDI)']])
    for index, row in melhores.iterrows():
        st.markdown(f"**{row['Fundo de Investimento']}** ({row['Classe']})")
        st.write(f"Retorno: {row['retorno(%)']:.2f}% | PL: {row['PL']:.2f} | Sharpe: {row['Sharpe(CDI)']:.2f}")
        if isinstance(row['Drawdown(%)'], pd.DataFrame):
            st.write("Drawdown:")
            st.dataframe(row['Drawdown(%)'])
        else:
            st.write("Nenhum drawdown no período.")