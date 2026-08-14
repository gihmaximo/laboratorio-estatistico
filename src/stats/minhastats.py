def media(lista):
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
    pass

def variancia_populacional(lista):
    pass

def variancia_amostral(lista):
    pass

def desvio_padrao_populacional(lista):
    pass

def desvio_padrao_amostral(lista):
    pass

def quartis(lista):
    pass

def percentil(lista):
    pass

def coeficiente_variacao(lista):
    pass

def covariancia(lista):
    pass

def correlacao_pearson(lista):
    pass