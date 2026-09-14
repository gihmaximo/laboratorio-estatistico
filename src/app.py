import streamlit as st
import pandas as pd

from stats.minhastats import (
    media,
    mediana,
    moda,
    amplitude,
    variancia_populacional,
    variancia_amostral,
    desvio_padrao_populacional,
    desvio_padrao_amostral
)


st.title("Laboratório Estatístico")

dados = pd.read_csv("dados/spotify_trabalho.csv")

st.write("Quantidade de registros:", len(dados))
st.write("Quantidade de variáveis:", len(dados.columns))

variaveis_numericas = dados.select_dtypes(include="number").columns.tolist()

variavel = st.selectbox(
    "Escolha uma variável:",
    variaveis_numericas
)

valores = dados[variavel].dropna().tolist()

st.subheader("Estatística Descritiva")

st.write("Média:", media(valores))
st.write("Mediana:", mediana(valores))
st.write("Moda:", moda(valores))
st.write("Amplitude:", amplitude(valores))
st.write("Variância populacional:", variancia_populacional(valores))
st.write("Variância amostral:", variancia_amostral(valores))
st.write("Desvio padrão populacional:", desvio_padrao_populacional(valores))
st.write("Desvio padrão amostral:", desvio_padrao_amostral(valores))