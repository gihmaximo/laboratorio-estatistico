import numpy as np
import scipy.stats as stats
import minhastats as ms

def executar_testes_automatizados():
    # Conjunto de dados de teste (garantindo variabilidade estatística)
    dados_x = [12, 15, 18, 22, 25, 30, 35, 40, 18]
    dados_y = [5, 8, 12, 14, 20, 22, 28, 32, 15]
    
    # Tolerância estrita documentada para arredondamento de float
    tol = 1e-5
    print("🧪 INICIANDO TESTES AUTOMATIZADOS (minhastats vs NumPy/SciPy):\n")

    assert abs(ms.media(dados_x) - np.mean(dados_x)) < tol, "Falha na Média"
    print("✅ Média: Validada com NumPy")

    assert abs(ms.mediana(dados_x) - np.median(dados_x)) < tol, "Falha na Mediana"
    print("✅ Mediana: Validada com NumPy")

    moda_res = ms.moda(dados_x)
    moda_numpy = int(stats.mode(dados_x, keepdims=True).mode[0])
    assert moda_res == moda_numpy, f"Falha na Moda: esperado {moda_numpy}, obteve {moda_res}"
    print("✅ Moda: Validada com SciPy")

    amp_numpy = int(np.max(dados_x) - np.min(dados_x))
    assert abs(ms.amplitude(dados_x) - amp_numpy) < tol, "Falha na Amplitude"
    print("✅ Amplitude: Validada com NumPy")

    assert abs(ms.variancia_populacional(dados_x) - np.var(dados_x, ddof=0)) < tol, "Falha na Variância Populacional"
    assert abs(ms.variancia_amostral(dados_x) - np.var(dados_x, ddof=1)) < tol, "Falha na Variância Amostral"
    print("✅ Variâncias (Populacional e Amostral): Validadas com NumPy")

    assert abs(ms.desvio_padrao_populacional(dados_x) - np.std(dados_x, ddof=0)) < tol, "Falha no Desvio Padrão Populacional"
    assert abs(ms.desvio_padrao_amostral(dados_x) - np.std(dados_x, ddof=1)) < tol, "Falha no Desvio Padrão Amostral"
    print("✅ Desvios Padrão (Populacional e Amostral): Validados com NumPy")

    assert abs(ms.percentil(dados_x, 25) - np.percentile(dados_x, 25, method='linear')) < tol, "Falha no Percentil 25"
    q1, q2, q3 = ms.quartis(dados_x)
    assert abs(q1 - np.percentile(dados_x, 25, method='linear')) < tol, "Falha no Q1"
    assert abs(q2 - np.percentile(dados_x, 50, method='linear')) < tol, "Falha no Q2"
    assert abs(q3 - np.percentile(dados_x, 75, method='linear')) < tol, "Falha no Q3"
    print("✅ Quartis e Percentis: Validados com NumPy (Interpolação Linear)")

    cv_numpy = (np.std(dados_x, ddof=1) / np.mean(dados_x)) * 100
    assert abs(ms.coeficiente_variacao(dados_x) - cv_numpy) < tol, "Falha no Coeficiente de Variação"
    print("✅ Coeficiente de Variação: Validado com NumPy")

    cov_numpy = np.cov(dados_x, dados_y)[0][1]
    assert abs(ms.covariancia(dados_x, dados_y) - cov_numpy) < tol, "Falha na Covariância"
    print("✅ Covariância: Validada com NumPy")

    corr_numpy = np.corrcoef(dados_x, dados_y)[0][1]
    assert abs(ms.correlacao_pearson(dados_x, dados_y) - corr_numpy) < tol, "Falha na Correlação de Pearson"
    print("✅ Correlação de Pearson: Validada com NumPy")

    print("\n🚀 Testes concluídos e validados com sucesso!")

    print("\n⚠️ VALIDANDO CASOS EXTREMOS (Proteção contra falhas):")
    
    vazia = []
    assert ms.media(vazia) == 0, "Falha: Média com lista vazia"
    assert ms.variancia_populacional(vazia) == 0, "Falha: Variância Pop com lista vazia"
    assert ms.variancia_amostral(vazia) == 0, "Falha: Variância Amostral com lista vazia"
    print("✅ Tratamento de Lista Vazia: OK")

    unico = [42]
    assert ms.media(unico) == 42, "Falha: Média com 1 elemento"
    assert ms.variancia_amostral(unico) == 0, "Falha: Variância Amostral com 1 elemento (Evitou divisão por zero!)"
    print("✅ Tratamento de Elemento Único: OK")

if __name__ == "__main__":
    executar_testes_automatizados()
