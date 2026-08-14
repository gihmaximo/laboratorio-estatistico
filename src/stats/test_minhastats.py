import minhastats

dados_impar = [7, 1, 3, 9, 5]
dados_par = [10, 20, 30, 40, 50, 60]

resultado_impar = minhastats.mediana(dados_impar)
resultado_par = minhastats.mediana(dados_par)
media = minhastats.media(dados_impar)

print(resultado_impar)
print(resultado_par)
print(media)

print (minhastats.moda([1, 2, 3, 4]))