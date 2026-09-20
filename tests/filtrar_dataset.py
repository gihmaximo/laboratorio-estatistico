# Filtrando o dataset original para manter apenas os artistas que seriam utilizados no trabalho.

import duckdb

artistas = [
    "Taylor Swift",
    "Twenty One Pilots",
    "Linkin Park",
    "Michael Jackson",
    "Bad Bunny",
    "Sabrina Carpenter",
    "Bring Me The Horizon",
    "One Direction",
    "The Neighbourhood",
    "Tame Impala"
]

lista_artistas = "', '".join(artistas)

dados = duckdb.sql(f"""
    SELECT *
    FROM 'dados/spotify-huge-audio-features.parquet'
    WHERE artist_name IN ('{lista_artistas}')
""").df()

print("Antes da remoção de duplicatas:")
print(dados.shape)

# Removendo músicas repetidas por causa de colaborações
dados = dados.drop_duplicates(subset="track_id")

print("Depois da remoção de duplicatas:")
print(dados.shape)

# Salvando o dataset final do trabalho
dados.to_csv("dados/spotify_trabalho.csv", index=False)

print("Arquivo salvo com sucesso!")