import sys
from pathlib import Path

import numpy as np
import scipy.stats as stats

# Adiciona a pasta src ao caminho de importação.
PASTA_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PASTA_SRC))

import stats.minhastats as ms

# DADOS DE TESTE

dados_x = [
    12, 15, 18, 22, 25,
    30, 35, 40, 18
]

dados_y = [
    5, 8, 12, 14, 20,
    22, 28, 32, 15
]

# Tolerância utilizada para comparar resultados de ponto flutuante.
TOLERANCIA = 1e-5


# MEDIDAS DE TENDÊNCIA CENTRAL

def test_media():
    resultado = ms.media(dados_x)
    esperado = np.mean(dados_x)

    assert abs(resultado - esperado) < TOLERANCIA


def test_mediana():
    resultado = ms.mediana(dados_x)
    esperado = np.median(dados_x)

    assert abs(resultado - esperado) < TOLERANCIA


def test_moda():
    resultado = ms.moda(dados_x)
    esperado = int(
        stats.mode(
            dados_x,
            keepdims=True
        ).mode[0]
    )

    assert resultado == esperado


# MEDIDAS DE DISPERSÃO

def test_amplitude():
    resultado = ms.amplitude(dados_x)
    esperado = np.max(dados_x) - np.min(dados_x)

    assert abs(resultado - esperado) < TOLERANCIA


def test_variancia_populacional():
    resultado = ms.variancia_populacional(
        dados_x
    )

    esperado = np.var(
        dados_x,
        ddof=0
    )

    assert abs(resultado - esperado) < TOLERANCIA


def test_variancia_amostral():
    resultado = ms.variancia_amostral(
        dados_x
    )

    esperado = np.var(
        dados_x,
        ddof=1
    )

    assert abs(resultado - esperado) < TOLERANCIA


def test_desvio_padrao_populacional():
    resultado = ms.desvio_padrao_populacional(
        dados_x
    )

    esperado = np.std(
        dados_x,
        ddof=0
    )

    assert abs(resultado - esperado) < TOLERANCIA


def test_desvio_padrao_amostral():
    resultado = ms.desvio_padrao_amostral(
        dados_x
    )

    esperado = np.std(
        dados_x,
        ddof=1
    )

    assert abs(resultado - esperado) < TOLERANCIA


# PERCENTIS E QUARTIS

def test_percentil():
    resultado = ms.percentil(
        dados_x,
        25
    )

    esperado = np.percentile(
        dados_x,
        25,
        method="linear"
    )

    assert abs(resultado - esperado) < TOLERANCIA


def test_quartis():
    q1, q2, q3 = ms.quartis(
        dados_x
    )

    esperado_q1 = np.percentile(
        dados_x,
        25,
        method="linear"
    )

    esperado_q2 = np.percentile(
        dados_x,
        50,
        method="linear"
    )

    esperado_q3 = np.percentile(
        dados_x,
        75,
        method="linear"
    )

    assert abs(
        q1 - esperado_q1
    ) < TOLERANCIA

    assert abs(
        q2 - esperado_q2
    ) < TOLERANCIA

    assert abs(
        q3 - esperado_q3
    ) < TOLERANCIA


# COEFICIENTE DE VARIAÇÃO

def test_coeficiente_variacao():
    resultado = ms.coeficiente_variacao(
        dados_x
    )

    esperado = (
        np.std(
            dados_x,
            ddof=1
        )
        / np.mean(dados_x)
    ) * 100

    assert abs(
        resultado - esperado
    ) < TOLERANCIA


# COVARIÂNCIA E CORRELAÇÃO

def test_covariancia():
    resultado = ms.covariancia(
        dados_x,
        dados_y
    )

    esperado = np.cov(
        dados_x,
        dados_y
    )[0][1]

    assert abs(
        resultado - esperado
    ) < TOLERANCIA


def test_correlacao_pearson():
    resultado = ms.correlacao_pearson(
        dados_x,
        dados_y
    )

    esperado = np.corrcoef(
        dados_x,
        dados_y
    )[0][1]

    assert abs(
        resultado - esperado
    ) < TOLERANCIA


# REGRESSÃO LINEAR

def test_regressao_linear():
    coeficiente_angular, coeficiente_linear = (
        ms.regressao_linear(
            dados_x,
            dados_y
        )
    )

    esperado_angular, esperado_linear = (
        np.polyfit(
            dados_x,
            dados_y,
            1
        )
    )

    assert abs(
        coeficiente_angular - esperado_angular
    ) < TOLERANCIA

    assert abs(
        coeficiente_linear - esperado_linear
    ) < TOLERANCIA


# COEFICIENTE DE DETERMINAÇÃO - R²

def test_coeficiente_determinacao():
    resultado = ms.coeficiente_determinacao(
        dados_x,
        dados_y
    )

    correlacao = np.corrcoef(
        dados_x,
        dados_y
    )[0][1]

    esperado = correlacao ** 2

    assert abs(
        resultado - esperado
    ) < TOLERANCIA


# CASOS EXTREMOS

def test_lista_vazia():
    lista_vazia = []

    assert ms.media(
        lista_vazia
    ) == 0

    assert ms.variancia_populacional(
        lista_vazia
    ) == 0

    assert ms.variancia_amostral(
        lista_vazia
    ) == 0


def test_elemento_unico():
    lista = [42]

    assert ms.media(
        lista
    ) == 42

    assert ms.variancia_amostral(
        lista
    ) == 0


def test_listas_com_tamanhos_diferentes():
    lista_x = [1, 2, 3]
    lista_y = [1, 2]

    try:
        ms.covariancia(
            lista_x,
            lista_y
        )

        assert False

    except ValueError:
        assert True


def test_percentil_invalido():
    try:
        ms.percentil(
            dados_x,
            101
        )

        assert False

    except ValueError:
        assert True