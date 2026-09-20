import random
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from stats.minhastats import (
    media,
    mediana,
    moda,
    amplitude,
    variancia_populacional,
    variancia_amostral,
    desvio_padrao_populacional,
    desvio_padrao_amostral,
    percentil,
    quartis,
    coeficiente_variacao,
    covariancia,
    correlacao_pearson,
    regressao_linear,
    coeficiente_determinacao,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Laboratório Estatístico",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #121212;
            color: #ffffff;
        }

        [data-testid="stSidebar"] {
            background-color: #000000;
        }

        [data-testid="stMetric"] {
            background-color: #181818;
            border-radius: 10px;
            padding: 15px;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 10px;
        }

        h1, h2, h3 {
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DADOS
# ============================================================

@st.cache_data
def carregar_dados():
    caminho = "dados/spotify_trabalho.csv"
    return pd.read_csv(caminho)


df = carregar_dados()


# ============================================================
# VARIÁVEIS
# ============================================================

variaveis_numericas = [
    "track_popularity",
    "album_popularity",
    "artist_popularity",
    "artist_followers",
    "tempo",
    "duration_ms",
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "energy_danceability_score",
]

variaveis_categoricas = [
    "artist_name",
    "album_name",
    "explicit",
]


nomes_variaveis = {
    "track_popularity": "Popularidade da música",
    "album_popularity": "Popularidade do álbum",
    "artist_popularity": "Popularidade do artista",
    "artist_followers": "Seguidores do artista",
    "tempo": "Tempo (BPM)",
    "duration_ms": "Duração (ms)",
    "danceability": "Dançabilidade",
    "energy": "Energia",
    "loudness": "Volume (dB)",
    "speechiness": "Fala na música",
    "acousticness": "Acústica",
    "instrumentalness": "Instrumentalidade",
    "liveness": "Presença de público",
    "valence": "Valência",
    "energy_danceability_score": "Energia × Dançabilidade",
    "artist_name": "Artista",
    "album_name": "Álbum",
    "explicit": "Conteúdo explícito",
}


descricoes_variaveis = {
    "track_popularity": (
        "Popularidade da música em uma escala de 0 a 100."
    ),
    "album_popularity": (
        "Popularidade do álbum em uma escala de 0 a 100."
    ),
    "artist_popularity": (
        "Popularidade do artista em uma escala de 0 a 100."
    ),
    "artist_followers": (
        "Quantidade de seguidores do artista."
    ),
    "tempo": (
        "Tempo musical da faixa, medido em batidas por minuto (BPM)."
    ),
    "duration_ms": (
        "Duração da música em milissegundos."
    ),
    "danceability": (
        "Mede o quanto uma faixa é adequada para dançar, de 0 a 1."
    ),
    "energy": (
        "Mede a intensidade e atividade da música, de 0 a 1."
    ),
    "loudness": (
        "Volume médio da faixa, medido em decibéis."
    ),
    "speechiness": (
        "Detecta a presença de palavras faladas na música."
    ),
    "acousticness": (
        "Confiança de que a faixa é acústica, de 0 a 1."
    ),
    "instrumentalness": (
        "Probabilidade de a faixa não conter vocais, de 0 a 1."
    ),
    "liveness": (
        "Probabilidade de a faixa ter sido gravada ao vivo."
    ),
    "valence": (
        "Mede a positividade musical transmitida pela faixa."
    ),
    "energy_danceability_score": (
        "Índice combinado de energia e dançabilidade."
    ),
}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_numero(valor):
    if isinstance(valor, float):
        return f"{valor:,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return f"{valor:,}".replace(",", ".")


def obter_dados_numericos(nome_variavel):
    valores = pd.to_numeric(
        df[nome_variavel],
        errors="coerce"
    )

    valores = valores.dropna()

    return valores.tolist()


def interpretar_assimetria(media_valor, mediana_valor):
    diferenca = abs(media_valor - mediana_valor)

    if media_valor > mediana_valor:
        if diferenca > abs(media_valor) * 0.05:
            return (
                "A média é maior que a mediana, indicando "
                "uma possível assimetria positiva."
            )

        return (
            "A média é levemente maior que a mediana, "
            "indicando pouca assimetria."
        )

    if mediana_valor > media_valor:
        if diferenca > abs(media_valor) * 0.05:
            return (
                "A média é menor que a mediana, indicando "
                "uma possível assimetria negativa."
            )

        return (
            "A média é levemente menor que a mediana, "
            "indicando pouca assimetria."
        )

    return (
        "A média e a mediana são iguais ou muito próximas, "
        "indicando uma distribuição aproximadamente simétrica."
    )


def interpretar_cv(cv):
    if cv < 15:
        return "Baixa variabilidade em relação à média."

    if cv < 30:
        return "Variabilidade moderada em relação à média."

    return "Alta variabilidade em relação à média."


def normal_pdf(x, media_valor, desvio):
    if desvio == 0:
        return 0

    constante = 1 / (
        desvio * (2 * 3.141592653589793) ** 0.5
    )

    expoente = -(
        (x - media_valor) ** 2
    ) / (
        2 * desvio ** 2
    )

    return constante * (
        2.718281828459045 ** expoente
    )


def uniforme_pdf(x, minimo, maximo):
    if maximo == minimo:
        return 0

    if minimo <= x <= maximo:
        return 1 / (maximo - minimo)

    return 0


# ============================================================
# MENU
# ============================================================

st.sidebar.title("Laboratório Estatístico")

pagina = st.sidebar.radio(
    "Módulo",
    [
        "Início",
        "Estatística Descritiva",
        "Monte Carlo",
        "Distribuições",
        "Correlação e Regressão",
        "Descobertas",
    ]
)


# ============================================================
# INÍCIO — MÓDULO 0
# ============================================================

if pagina == "Início":

    st.title("Laboratório Estatístico Interativo")

    st.write(
        "Explore um conjunto de dados reais do Spotify "
        "por meio de estatística descritiva, probabilidade, "
        "distribuições, correlação e regressão."
    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Registros",
            f"{len(df):,}".replace(",", ".")
        )

    with col2:
        st.metric(
            "Variáveis",
            len(df.columns)
        )

    with col3:
        st.metric(
            "Artistas",
            df["artist_name"].nunique()
        )

    st.markdown("---")

    st.subheader("Sobre os dados")

    st.write(
        "O conjunto de dados contém informações sobre músicas, "
        "álbuns e artistas, incluindo popularidade, características "
        "musicais e informações de áudio."
    )

    st.subheader("Variáveis quantitativas")

    st.write(
        "São utilizadas nas análises estatísticas que envolvem "
        "média, mediana, variância, desvio padrão, correlação "
        "e regressão."
    )

    st.write(
        ", ".join(
            nomes_variaveis[v]
            for v in variaveis_numericas
        )
    )

    st.subheader("Variáveis categóricas")

    st.write(
        "São utilizadas para análises de frequência e distribuição "
        "de categorias."
    )

    st.write(
        ", ".join(
            nomes_variaveis[v]
            for v in variaveis_categoricas
        )
    )

    st.subheader("Artistas analisados")

    artistas = sorted(
        df["artist_name"].dropna().unique()
    )

    st.write(", ".join(artistas))


# ============================================================
# ESTATÍSTICA DESCRITIVA — MÓDULO 2
# ============================================================

elif pagina == "Estatística Descritiva":

    st.title("Estatística Descritiva")

    tipo_variavel = st.radio(
        "Escolha o tipo de variável:",
        [
            "Variável numérica",
            "Variável categórica"
        ],
        horizontal=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # VARIÁVEL NUMÉRICA
    # --------------------------------------------------------

    if tipo_variavel == "Variável numérica":

        variavel = st.selectbox(
            "Escolha uma variável:",
            variaveis_numericas,
            format_func=lambda x: nomes_variaveis[x]
        )

        valores = obter_dados_numericos(variavel)

        st.info(
            descricoes_variaveis.get(
                variavel,
                "Variável numérica."
            )
        )

        st.markdown("---")

        st.subheader("Medidas estatísticas")

        med = media(valores)
        mediana_valor = mediana(valores)
        moda_valor = moda(valores)
        amp = amplitude(valores)

        var_pop = variancia_populacional(valores)
        var_amostral = variancia_amostral(valores)

        dp_pop = desvio_padrao_populacional(valores)
        dp_amostral = desvio_padrao_amostral(valores)

        q1, q2, q3 = quartis(valores)

        cv = coeficiente_variacao(valores)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Média",
                formatar_numero(med)
            )

        with col2:
            st.metric(
                "Mediana",
                formatar_numero(mediana_valor)
            )

        with col3:
            if isinstance(moda_valor, list):
                texto_moda = ", ".join(
                    formatar_numero(x)
                    for x in moda_valor[:3]
                )

                if len(moda_valor) > 3:
                    texto_moda += "..."

            else:
                texto_moda = str(moda_valor)

            st.metric(
                "Moda",
                texto_moda
            )

        with col4:
            st.metric(
                "Amplitude",
                formatar_numero(amp)
            )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Variância populacional",
                formatar_numero(var_pop)
            )

        with col2:
            st.metric(
                "Variância amostral",
                formatar_numero(var_amostral)
            )

        with col3:
            st.metric(
                "Desvio padrão",
                formatar_numero(dp_amostral)
            )

        with col4:
            st.metric(
                "Coeficiente de variação",
                f"{cv:.2f}%"
            )

        st.markdown("---")

        st.subheader("Quartis e percentis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Q1",
                formatar_numero(q1)
            )

        with col2:
            st.metric(
                "Q2",
                formatar_numero(q2)
            )

        with col3:
            st.metric(
                "Q3",
                formatar_numero(q3)
            )

        percentil_escolhido = st.slider(
            "Escolha um percentil:",
            0,
            100,
            90
        )

        valor_percentil = percentil(
            valores,
            percentil_escolhido
        )

        st.write(
            f"O percentil {percentil_escolhido} "
            f"é **{formatar_numero(valor_percentil)}**."
        )

        st.markdown("---")

        # ----------------------------------------------------
        # FREQUÊNCIAS
        # ----------------------------------------------------

        st.subheader("Distribuição de frequências")

        classes = st.slider(
            "Número de classes:",
            5,
            20,
            10
        )

        intervalos = pd.cut(
            valores,
            bins=classes,
            include_lowest=True
        )

        frequencias = (
            pd.Series(intervalos)
            .value_counts()
            .sort_index()
            .reset_index()
        )

        frequencias.columns = [
            "Classe",
            "Frequência"
        ]

        frequencias["Classe"] = frequencias[
            "Classe"
        ].apply(
            lambda intervalo: (
                f"{intervalo.left:.1f} – "
                f"{intervalo.right:.1f}"
            )
        )

        frequencias[
            "Frequência relativa (%)"
        ] = (
            frequencias["Frequência"]
            / len(valores)
            * 100
        )

        frequencias[
            "Frequência relativa (%)"
        ] = (
            frequencias[
                "Frequência relativa (%)"
            ].round(2)
        )

        st.dataframe(
            frequencias,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # ----------------------------------------------------
        # HISTOGRAMA
        # ----------------------------------------------------

        st.subheader("Histograma")

        fig, ax = plt.subplots(figsize=(6, 3))

        ax.hist(
            valores,
            bins=classes
        )

        ax.set_xlabel(
            nomes_variaveis[variavel]
        )

        ax.set_ylabel(
            "Frequência"
        )

        ax.set_title(
            f"Distribuição de {nomes_variaveis[variavel]}"
        )

        st.pyplot(fig)

        plt.close(fig)

        st.markdown("---")

        # ----------------------------------------------------
        # BOXPLOT
        # ----------------------------------------------------

        st.subheader("Boxplot")

        fig, ax = plt.subplots(figsize=(6, 3))

        ax.boxplot(
            valores,
            vert=False
        )

        ax.set_xlabel(
            nomes_variaveis[variavel]
        )

        st.pyplot(fig)

        plt.close(fig)

        # ----------------------------------------------------
        # OUTLIERS
        # ----------------------------------------------------

        limite_inferior = q1 - 1.5 * (q3 - q1)
        limite_superior = q3 + 1.5 * (q3 - q1)

        outliers = [
            x
            for x in valores
            if x < limite_inferior
            or x > limite_superior
        ]

        st.markdown("---")

        st.subheader("Detecção de outliers")

        st.write(
            f"Foram identificados **{len(outliers)} "
            "outliers** pelo método do intervalo interquartil (IQR)."
        )

        st.write(
            f"Limite inferior: "
            f"**{formatar_numero(limite_inferior)}**"
        )

        st.write(
            f"Limite superior: "
            f"**{formatar_numero(limite_superior)}**"
        )

        st.markdown("---")

        # ----------------------------------------------------
        # INTERPRETAÇÃO
        # ----------------------------------------------------

        st.subheader("Interpretação automática")

        st.write(
            interpretar_assimetria(
                med,
                mediana_valor
            )
        )

        st.write(
            interpretar_cv(cv)
        )


    # --------------------------------------------------------
    # VARIÁVEL CATEGÓRICA
    # --------------------------------------------------------

    else:

        variavel = st.selectbox(
            "Escolha uma variável:",
            variaveis_categoricas,
            format_func=lambda x: nomes_variaveis[x]
        )

        valores = df[variavel].dropna()

        frequencias = (
            valores
            .value_counts()
            .reset_index()
        )

        frequencias.columns = [
            nomes_variaveis[variavel],
            "Frequência"
        ]

        frequencias["Frequência relativa (%)"] = (
            frequencias["Frequência"]
            / len(valores)
            * 100
        )

        frequencias[
            "Frequência relativa (%)"
        ] = (
            frequencias[
                "Frequência relativa (%)"
            ].round(2)
        )

        st.subheader(
            "Distribuição de frequências"
        )

        st.dataframe(
            frequencias,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        st.subheader(
            "Categorias mais frequentes"
        )

        top = frequencias.head(15)

        fig, ax = plt.subplots(figsize=(6, 3))

        ax.bar(
            top.iloc[:, 0].astype(str),
            top["Frequência"]
        )

        ax.set_xlabel(
            nomes_variaveis[variavel]
        )

        ax.set_ylabel(
            "Frequência"
        )

        ax.set_title(
            f"Categorias de {nomes_variaveis[variavel]}"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        st.pyplot(fig)

        plt.close(fig)

        categoria_principal = frequencias.iloc[0, 0]
        quantidade_principal = frequencias.iloc[0, 1]

        st.info(
            f"A categoria mais frequente é "
            f"**{categoria_principal}**, com "
            f"**{quantidade_principal} registros**."
        )


# ============================================================
# MONTE CARLO — MÓDULO 3
# ============================================================

elif pagina == "Monte Carlo":

    st.title("Probabilidade e Simulação")

    experimento = st.radio(
        "Escolha um experimento:",
        [
            "Lei dos Grandes Números",
            "Teorema Central do Limite"
        ],
        horizontal=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # LEI DOS GRANDES NÚMEROS
    # --------------------------------------------------------

    if experimento == "Lei dos Grandes Números":

        st.subheader(
            "Lei dos Grandes Números"
        )

        st.write(
            "Simulamos lançamentos de um dado e observamos "
            "como a frequência relativa de uma face se aproxima "
            "da probabilidade teórica de 1/6."
        )

        quantidade_lancamentos = st.slider(
            "Número de lançamentos:",
            100,
            10000,
            1000,
            step=100
        )

        face_escolhida = st.selectbox(
            "Face observada:",
            [1, 2, 3, 4, 5, 6]
        )

        if st.button(
            "Executar simulação",
            key="simulacao_dado"
        ):

            resultados = [
                random.randint(1, 6)
                for _ in range(
                    quantidade_lancamentos
                )
            ]

            frequencia_acumulada = []

            quantidade_face = 0

            for i, resultado in enumerate(
                resultados,
                start=1
            ):

                if resultado == face_escolhida:
                    quantidade_face += 1

                frequencia = (
                    quantidade_face / i
                )

                frequencia_acumulada.append(
                    frequencia
                )

            fig, ax = plt.subplots(figsize=(6, 3))

            ax.plot(
                frequencia_acumulada
            )

            ax.axhline(
                1 / 6,
                linestyle="--"
            )

            ax.set_xlabel(
                "Número de lançamentos"
            )

            ax.set_ylabel(
                "Frequência relativa"
            )

            ax.set_title(
                f"Convergência da face {face_escolhida}"
            )

            st.pyplot(fig)

            plt.close(fig)

            st.write(
                f"Frequência relativa final: "
                f"**{frequencia_acumulada[-1]:.4f}**"
            )

            st.write(
                "Probabilidade teórica: "
                "**0,1667 (1/6)**"
            )


    # --------------------------------------------------------
    # TEOREMA CENTRAL DO LIMITE
    # --------------------------------------------------------

    else:

        st.subheader(
            "Teorema Central do Limite"
        )

        st.write(
            "A simulação retira repetidas amostras de uma "
            "variável do conjunto de dados e calcula a média "
            "de cada amostra."
        )

        variavel_tcl = st.selectbox(
            "Variável:",
            [
                "track_popularity",
                "danceability",
                "energy",
                "valence",
                "tempo",
            ],
            format_func=lambda x: nomes_variaveis[x]
        )

        tamanho_amostra = st.slider(
            "Tamanho de cada amostra:",
            2,
            200,
            30
        )

        repeticoes = st.slider(
            "Número de repetições:",
            100,
            5000,
            1000,
            step=100
        )

        if st.button(
            "Executar simulação",
            key="simulacao_tcl"
        ):

            valores_tcl = obter_dados_numericos(
                variavel_tcl
            )

            medias_amostrais = []

            for _ in range(repeticoes):

                amostra = random.choices(
                    valores_tcl,
                    k=tamanho_amostra
                )

                medias_amostrais.append(
                    media(amostra)
                )

            fig, ax = plt.subplots(figsize=(6, 3))

            ax.hist(
                medias_amostrais,
                bins=30
            )

            ax.set_xlabel(
                "Médias amostrais"
            )

            ax.set_ylabel(
                "Frequência"
            )

            ax.set_title(
                "Distribuição das médias amostrais"
            )

            st.pyplot(fig)

            plt.close(fig)

            st.write(
                f"Média das médias amostrais: "
                f"**{media(medias_amostrais):.4f}**"
            )


# ============================================================
# DISTRIBUIÇÕES — MÓDULO 4
# ============================================================

elif pagina == "Distribuições":

    st.title("Distribuições Teóricas")

    st.write(
        "Nesta etapa, comparamos a distribuição observada "
        "nos dados com distribuições teóricas."
    )

    variavel = st.selectbox(
        "Escolha uma variável:",
        [
            "track_popularity",
            "danceability",
            "energy",
            "valence",
            "tempo",
        ],
        format_func=lambda x: nomes_variaveis[x]
    )

    valores = obter_dados_numericos(
        variavel
    )

    media_valor = media(valores)
    desvio = desvio_padrao_populacional(
        valores
    )

    minimo = min(valores)
    maximo = max(valores)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Média estimada",
            formatar_numero(media_valor)
        )

    with col2:
        st.metric(
            "Desvio padrão estimado",
            formatar_numero(desvio)
        )

    fig, ax = plt.subplots(figsize=(6, 3))

    frequencias_hist, limites, _ = ax.hist(
        valores,
        bins=30,
        density=True,
        alpha=0.6
    )

    pontos_x = []

    passo = (
        (maximo - minimo) / 200
        if maximo != minimo
        else 1
    )

    for i in range(201):
        pontos_x.append(
            minimo + i * passo
        )

    pontos_normal = [
        normal_pdf(
            x,
            media_valor,
            desvio
        )
        for x in pontos_x
    ]

    ax.plot(
        pontos_x,
        pontos_normal,
        label="Normal"
    )

    pontos_uniforme = [
        uniforme_pdf(
            x,
            minimo,
            maximo
        )
        for x in pontos_x
    ]

    ax.plot(
        pontos_x,
        pontos_uniforme,
        label="Uniforme"
    )

    ax.set_xlabel(
        nomes_variaveis[variavel]
    )

    ax.set_ylabel(
        "Densidade"
    )

    ax.set_title(
        "Dados observados × distribuições teóricas"
    )

    ax.legend()

    st.pyplot(fig)

    plt.close(fig)

    st.markdown("---")

    st.subheader("Discussão")

    st.write(
        "A distribuição Normal é construída a partir da média "
        "e do desvio padrão calculados nos próprios dados."
    )

    st.write(
        "A distribuição Uniforme considera todos os valores "
        "entre o mínimo e o máximo como igualmente prováveis."
    )

    st.write(
        "A comparação visual permite avaliar qual modelo "
        "teórico representa melhor o comportamento observado."
    )


# ============================================================
# CORRELAÇÃO E REGRESSÃO — MÓDULO 5
# ============================================================

elif pagina == "Correlação e Regressão":

    st.title("Correlação e Regressão Linear")

    variaveis_regressao = [
        v
        for v in variaveis_numericas
    ]

    col1, col2 = st.columns(2)

    with col1:

        variavel_x = st.selectbox(
            "Variável X:",
            variaveis_regressao,
            index=0,
            format_func=lambda x: nomes_variaveis[x]
        )

    with col2:

        variavel_y = st.selectbox(
            "Variável Y:",
            variaveis_regressao,
            index=1,
            format_func=lambda x: nomes_variaveis[x]
        )

    dados = df[
        [variavel_x, variavel_y]
    ].dropna()

    valores_x = dados[
        variavel_x
    ].tolist()

    valores_y = dados[
        variavel_y
    ].tolist()

    correlacao = correlacao_pearson(
        valores_x,
        valores_y
    )

    cov = covariancia(
        valores_x,
        valores_y
    )

    coef_angular, coef_linear = regressao_linear(
        valores_x,
        valores_y
    )

    r2 = coeficiente_determinacao(
        valores_x,
        valores_y
    )

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Correlação de Pearson",
            f"{correlacao:.4f}"
        )

    with col2:
        st.metric(
            "Covariância",
            formatar_numero(cov)
        )

    with col3:
        st.metric(
            "Coeficiente angular",
            formatar_numero(coef_angular)
        )

    with col4:
        st.metric(
            "R²",
            f"{r2:.4f}"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # GRÁFICO
    # --------------------------------------------------------

    st.subheader("Dispersão e reta de regressão")

    fig, ax = plt.subplots(figsize=(6, 3))

    ax.scatter(
        valores_x,
        valores_y,
        alpha=0.5
    )

    x_min = min(valores_x)
    x_max = max(valores_x)

    linha_x = [
        x_min,
        x_max
    ]

    linha_y = [
        coef_angular * x_min + coef_linear,
        coef_angular * x_max + coef_linear
    ]

    ax.plot(
        linha_x,
        linha_y,
        linewidth=2
    )

    ax.set_xlabel(
        nomes_variaveis[variavel_x]
    )

    ax.set_ylabel(
        nomes_variaveis[variavel_y]
    )

    ax.set_title(
        "Regressão linear"
    )

    st.pyplot(fig)

    plt.close(fig)

    st.markdown("---")

    st.subheader("Equação da reta")

    sinal = "+" if coef_linear >= 0 else "-"

    st.latex(
        rf"""
        \hat{{Y}} =
        {coef_angular:.4f}X
        {sinal}
        {abs(coef_linear):.4f}
        """
    )

    st.write(
        f"O coeficiente angular indica que, para cada "
        f"aumento de 1 unidade em "
        f"**{nomes_variaveis[variavel_x]}**, "
        f"a variável **{nomes_variaveis[variavel_y]}** "
        f"varia, em média, "
        f"**{coef_angular:.4f} unidades**."
    )

    st.write(
        f"O modelo explica aproximadamente "
        f"**{r2 * 100:.2f}%** da variabilidade observada "
        f"na variável Y."
    )

    st.warning(
        "Correlação e regressão não demonstram causalidade. "
        "Uma associação estatística entre duas variáveis "
        "não significa que uma seja responsável pela outra."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # PREVISÃO
    # --------------------------------------------------------

    st.subheader("Previsão")

    valor_x = st.number_input(
        f"Digite um valor de "
        f"{nomes_variaveis[variavel_x]}:",
        value=float(
            media(valores_x)
        )
    )

    previsao = (
        coef_angular * valor_x
        + coef_linear
    )

    st.success(
        f"Valor estimado de "
        f"**{nomes_variaveis[variavel_y]}**: "
        f"**{formatar_numero(previsao)}**"
    )


# ============================================================
# DESCOBERTAS — MÓDULO 6
# ============================================================

elif pagina == "Descobertas":

    st.title("Descobertas Estatísticas")

    st.write(
        "Nesta seção são apresentadas algumas relações "
        "interessantes encontradas no conjunto de dados."
    )

    # --------------------------------------------------------
    # DESCOBERTA 1
    # --------------------------------------------------------

    x = obter_dados_numericos(
        "artist_popularity"
    )

    y = obter_dados_numericos(
        "track_popularity"
    )

    correlacao_1 = correlacao_pearson(
        x,
        y
    )

    st.subheader(
        "1. Popularidade do artista x popularidade da música"
    )

    st.write(
        f"A correlação de Pearson calculada pela biblioteca "
        f"própria foi **{correlacao_1:.4f}**."
    )

    st.write(
        "Esse resultado permite avaliar se artistas mais "
        "populares tendem a apresentar músicas com maior "
        "popularidade no conjunto analisado."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # DESCOBERTA 2
    # --------------------------------------------------------

    x = obter_dados_numericos(
        "danceability"
    )

    y = obter_dados_numericos(
        "energy"
    )

    correlacao_2 = correlacao_pearson(
        x,
        y
    )

    st.subheader(
        "2. Dançabilidade x energia"
    )

    st.write(
        f"A correlação encontrada foi "
        f"**{correlacao_2:.4f}**."
    )

    st.write(
        "Essa relação mostra se músicas com maior "
        "dançabilidade também tendem a apresentar "
        "maior energia."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # DESCOBERTA 3
    # --------------------------------------------------------

    x = obter_dados_numericos(
        "danceability"
    )

    y = obter_dados_numericos(
        "valence"
    )

    correlacao_3 = correlacao_pearson(
        x,
        y
    )

    st.subheader(
        "3. Dançabilidade x valência"
    )

    st.write(
        f"A correlação encontrada foi "
        f"**{correlacao_3:.4f}**."
    )

    st.write(
        "Essa análise permite observar se músicas mais "
        "dançantes tendem também a apresentar valores "
        "maiores de positividade musical."
    )

    st.markdown("---")

    st.info(
        "As descobertas apresentadas são calculadas "
        "diretamente a partir dos dados selecionados e "
        "das funções estatísticas implementadas no projeto."
    )