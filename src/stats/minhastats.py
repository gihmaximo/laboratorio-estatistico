def media(lista):
    if not lista:
        return 0
    
    soma = 0

    for numero in lista:
        soma += numero

    return soma / len(lista)


def mediana(lista):
    lista_ordenada = sorted(lista)
    n = len(lista_ordenada)

    meio = n // 2

    if n % 2 != 0:
        return lista_ordenada[meio]
    else:
        return (lista_ordenada[meio - 1] + lista_ordenada[meio]) / 2

def moda(lista):
    if not lista:
        return None

    contagem = {}
    for numero in lista:
        if numero in contagem:
            contagem[numero] += 1
        else:
            contagem[numero] = 1

    max_frequencia = max(contagem.values())

    if max_frequencia == 1:
        return "Não existe moda"

    modas = []
    for numero, frequencia in contagem.items():
        if frequencia == max_frequencia:
            modas.append(numero)

    if len(modas) == 1:
        return modas[0]
    
    return modas

def amplitude(lista):
    if not lista:
        return 0
    
    return max(lista) - min(lista)

def variancia_populacional(lista):
    n = len(lista)
    if n == 0:
        return 0
    
    med = media(lista)
    
    soma_quadrados = sum((x - med) ** 2 for x in lista)
    
    return soma_quadrados / n

def variancia_amostral(lista):
    n = len(lista)

    if n <= 1:
        return 0

    med = media(lista)

    soma_quadrados = sum((x - med) ** 2 for x in lista)

    return soma_quadrados / (n - 1)


def desvio_padrao_populacional(lista):
    var_pop = variancia_populacional(lista)
    return var_pop ** 0.5

def desvio_padrao_amostral(lista):
    var_amostral = variancia_amostral(lista)
    return var_amostral ** 0.5

def percentil(lista, p):
    if not lista:
        return 0
    if p < 0 or p > 100:
        raise ValueError("O percentil deve estar entre 0 e 100")
        
    lista_ordenada = sorted(lista)
    n = len(lista_ordenada)
    
    idx = (p / 100) * (n - 1)
    idx_baixo = int(idx)
    idx_alto = idx_baixo + 1
    
    if idx_alto >= n:
        return lista_ordenada[idx_baixo]
        
    peso_alto = idx - idx_baixo
    peso_baixo = 1 - peso_alto
    
    return (lista_ordenada[idx_baixo] * peso_baixo) + (lista_ordenada[idx_alto] * peso_alto)

def quartis(lista):
    if not lista:
        return (0, 0, 0)
    
    q1 = percentil(lista, 25)
    q2 = percentil(lista, 50)
    q3 = percentil(lista, 75)
    
    return (q1, q2, q3)

def coeficiente_variacao(lista):
    med = media(lista)
    if med == 0:
        return 0  
    
    dp = desvio_padrao_amostral(lista)
    return (dp / med) * 100

def covariancia(lista_x, lista_y):
    n = len(lista_x)
    if n != len(lista_y):
        raise ValueError("As duas listas devem ter o mesmo tamanho")
    if n <= 1:
        return 0
        
    media_x = media(lista_x)
    media_y = media(lista_y)
    
    soma_produtos = sum((lista_x[i] - media_x) * (lista_y[i] - media_y) for i in range(n))
    
    return soma_produtos / (n - 1)

def correlacao_pearson(lista_x, lista_y):
    n = len(lista_x)
    if n != len(lista_y):
        raise ValueError("As duas listas devem ter o mesmo tamanho")
        
    cov = covariancia(lista_x, lista_y)
    dp_x = desvio_padrao_amostral(lista_x)
    dp_y = desvio_padrao_amostral(lista_y)
    
    if dp_x == 0 or dp_y == 0:
        return 0
        
    return cov / (dp_x * dp_y)

def regressao_linear(lista_x, lista_y):
    if len(lista_x) != len(lista_y):
        raise ValueError("As duas listas devem ter o mesmo tamanho")

    if len(lista_x) < 2:
        return 0, 0

    media_x = media(lista_x)
    media_y = media(lista_y)

    numerador = 0
    denominador = 0

    for i in range(len(lista_x)):
        numerador += (
            (lista_x[i] - media_x)
            * (lista_y[i] - media_y)
        )

        denominador += (
            (lista_x[i] - media_x) ** 2
        )

    if denominador == 0:
        return 0, media_y

    coeficiente_angular = numerador / denominador

    coeficiente_linear = (
        media_y
        - coeficiente_angular * media_x
    )

    return coeficiente_angular, coeficiente_linear


def coeficiente_determinacao(lista_x, lista_y):
    if len(lista_x) != len(lista_y):
        raise ValueError("As duas listas devem ter o mesmo tamanho")

    if len(lista_x) == 0:
        return 0

    coeficiente_angular, coeficiente_linear = regressao_linear(
        lista_x,
        lista_y
    )

    media_y = media(lista_y)

    soma_total = 0
    soma_residuos = 0

    for i in range(len(lista_y)):
        y_estimado = (
            coeficiente_angular * lista_x[i]
            + coeficiente_linear
        )

        soma_total += (
            lista_y[i] - media_y
        ) ** 2

        soma_residuos += (
            lista_y[i] - y_estimado
        ) ** 2

    if soma_total == 0:
        return 0

    return 1 - (
        soma_residuos / soma_total
    )