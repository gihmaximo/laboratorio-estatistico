# Explorando o dataset original para definir quais dados seriam utilizados.

import pandas as pd

dados = pd.read_csv("dados/spotify_trabalho.csv")

print(dados.head())
print()

print("Quantidade de linhas e colunas:")
print(dados.shape)
print()

print("Colunas:")
print(dados.columns)
print()

print("Tipos dos dados:")
print(dados.dtypes)

print(dados["artist_name"].value_counts())

print(dados.describe())