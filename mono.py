# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:49:59 2015

mono.py

Executa os algoritmos mono-objetivo n vezes conforme o teorema do limite central da normalidade
Cria o gráfico comparativo das médias de cada geração/iteração

@author: victor
@todo Adicionar busca local ao fim da execução de cada algoritmo
"""
import mono_ga
import mono_aco
import mono_ils
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

#plt.ion()

# Quantidade de vezes a ser executado
n = 30

# lista dos métodos a serem chamados
algoritmos = ['mono_ils','mono_ga', 'mono_aco']
#algoritmos = ['mono_ils','mono_ga']
# lista de marcadores do matplotlib
marcadores = ['ro','bo','go']
# Conjunto de parâmetros de cada algoritmo para execução
parametrizacao= [[False], [False], [False]]

# Médias das melhores execuções de cada iteração/geração
execucoes = []

for i in range(0,len(algoritmos)): # para cada algoritmo
    execucoes.append([])
    m = __import__ (algoritmos[i])
    toCall = getattr(m,algoritmos[i])
    for j in range(0,n): # Obter uma lista de 30 execuções cada uma com parametro dentro do AG de gerações/iterações
        print 'Executando o algoritmo \'%s\' da posição %i na vez %i' % (algoritmos[i],i,j)
        res = toCall(parametrizacao[i])
        execucoes[i].append(res)

print '----------------------'

# Depois de todos os algoritmos rodados, crio uma média das iterações dos algoritmos para plotar
# e faço um único gráfico com os resultados

for i in range(0,len(algoritmos)):
    # Crio uma única lista com a soma de todas as execuções
    zipped_list = zip(*execucoes[i])
    medias = [sum(item)/float(n) for item in zipped_list]

    plt.plot( range(0,len(medias)), medias, marcadores[i], label=algoritmos[i])
    
    # plota no grafico

plt.legend(loc='best')
plt.xlabel('Iteracoes')
plt.ylabel('$Media_{Valor}$')
plt.grid()
plt.show()


# Salvo os histogramas

# Recupero o melhor resultado das 30 execuções e ploto o histograma pra cada algoritmo, ou seja, o último vetor de cada execução que contém a resposta final
histoDados = []
for i in range(0,len(algoritmos)):
    plt.figure()
    histoDados.append([])
    for j in range(0,len(execucoes[i])):
        histoDados[i].append(max(execucoes[i][j])) # tera cada melhor das 30 execucoes
    
    h = sorted(histoDados[i])  #sorted

    # norm: A normal continuous random variable.
    #The probability density function for norm is:
    #norm.pdf(x) = exp(-x**2/2)/sqrt(2*pi)
    fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
    
    plt.plot(h,fit,'-o')
    
    plt.hist(h,normed=True)      #use this to draw histogram of your data
    
    plt.title('Histograma %s' % (algoritmos[i]))
    
    plt.show()                   #use may also need add this
    
    std = np.std(h) 
    mean = np.mean(h)    
    print 'std for algorithm %s: %f' % (algoritmos[i],std)
    print 'mean for algorithm %s: %f'% (algoritmos[i],mean)
