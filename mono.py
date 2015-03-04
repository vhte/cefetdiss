# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:49:59 2015

mono.py

Executa os algoritmos mono-objetivo n vezes conforme o teorema do limite central da normalidade
Cria o gráfico comparativo das médias de cada geração/iteração

@author: victor
@todo Adicionar busca local ao fim da execução de cada algoritmo
"""
import d519
import mono_ga
import mono_aco
import mono_ils
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import mysql.connector
import timeit

plt.ion()
cnx = mysql.connector.connect(user='root', password='root', database='cemig_d519')
cursor = cnx.cursor()

# Quantidade de vezes a ser executado
n = 30

# Loops principais (gerações, colônias, iterações, etc...)
loops = 200

# Problema Knapsack a ser resolvido
W = 250
M = []
V = []

query = ("SELECT DISTINCT EquipamentoMT.ID AS ID, EquipamentoMT.IC AS IC, "
    "IF(EquipamentoMT.TIPO_EQUIPAMENTO_ID != 1, EquipamentoNovo.CUSTO, (EquipamentoNovo.CUSTO/1000*CaboMT.COMPRIMENTO)) AS CUSTO "
    "/*EquipamentoNovo.CUSTO,*/  "
    "/*EquipamentoMT.TIPO_EQUIPAMENTO_ID */ "
    "FROM EquipamentoMT  "
    "JOIN Segmento ON EquipamentoMT.SEGMENTO_ID = Segmento.ID  "
    "JOIN Alimentador ON Segmento.ALIMENTADOR_ID = Alimentador.ID  "
    "JOIN EquipamentoNovo ON EquipamentoNovo.TIPO_EQUIPAMENTO_ID = EquipamentoMT.TIPO_EQUIPAMENTO_ID  "
    "LEFT JOIN CaboMT ON EquipamentoMT.ID = CaboMT.ID  "
    "WHERE Alimentador.ID = 3")
    
cursor.execute(query)
for(ID,IC,CUSTO) in cursor:
    M.append(CUSTO)
    V.append(1-IC)

#Configuracoes ILS

# Configuracoes AG
geracoes = loops
tampop = 150
crossover = 90
mutacao = 5
pressaoSel = 2

#  Configuracoes ACO
colonias = loops
numForm = 10
C = 1
Q = d519.randrange(11,100)
alpha = 1
beta = 1
rho = 0.7 

# lista dos métodos a serem chamados
algoritmos = ['mono_ils','mono_ga', 'mono_aco']
#algoritmos = ['mono_ga', 'mono_ga','mono_ga','mono_ga']
#algoritmos = ['mono_ils', 'mono_ils','mono_ils','mono_ils']
#algoritmos = ['mono_aco']

# nomes a serem plotados (caso False, o nome do algoritmo)
nomesAlg = ['mono_ils', 'mono_ga', 'mono_aco']
#nomesAlg = ['mono_ga_200', 'mono_ga_250', 'mono_ga_300', 'mono_ga_350']
#nomesAlg = ['mono_ils_0001P_20BL_3V', 'mono_ils_0001P_20BL_6V', 'mono_ils_0001P_20BL_9V', 'mono_ils_0001P_20BL_12V']
#nomesAlg = ['mono_aco']

# lista de marcadores do matplotlib
marcadores = ['r-','b-','g-', 'y-']

# Conjunto de parâmetros de cada algoritmo para execução
#todos
parametrizacao = [[False,loops,20,0.001,1,W,M,V],[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel],[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V]]
#ag
#parametrizacao= [[False,W,M,V,geracoes,200,crossover,mutacao,pressaoSel], [False,W,M,V,geracoes,250,crossover,mutacao,pressaoSel], [False,W,M,V,geracoes,300,crossover,mutacao,pressaoSel], [False,W,M,V,geracoes,350,crossover,mutacao,pressaoSel]]
#ils
#parametrizacao= [[False,4000,20,0.001,3,W,M,V],[False,4000,20,0.001,6,W,M,V],[False,4000,20,0.001,9,W,M,V],[False,4000,20,0.001,12,W,M,V]]
#aco
#parametrizacao = [[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V]]

# Médias das melhores execuções de cada iteração/geração
execucoes = []

for i in range(0,len(algoritmos)): # para cada algoritmo
    execucoes.append([])
    m = __import__ (algoritmos[i])
    toCall = getattr(m,algoritmos[i])
    start_time = timeit.default_timer()
    for j in range(0,n): # Obter uma lista de 30 execuções cada uma com parametro dentro do AG de gerações/iterações
        print 'Executando o algoritmo \'%s\' da posição %i na vez %i' % (nomesAlg[i],i,j)
        res = toCall(parametrizacao[i])
        execucoes[i].append(res)
    print 'Valor maximo da primeira execucao: %f' % (max(execucoes[i][0]))
    elapsed = timeit.default_timer() - start_time
    print 'Tempo de execucao das %i vezes: %f segundos' % (n,elapsed)

print '----------------------'

# Depois de todos os algoritmos rodados, crio uma média das iterações dos algoritmos para plotar
# e faço um único gráfico com os resultados

for i in range(0,len(algoritmos)):
    # Crio uma única lista com a soma de todas as execuções
    zipped_list = zip(*execucoes[i])
    medias = [sum(item)/float(n) for item in zipped_list]

    # @todo olhar se python tem operador ternário
    if not nomesAlg[i]:
        nomesAlg[i] = algoritmos[i]
    
    print 'Resultado final (medias) para o algoritmo %s:' % (nomesAlg[i])
    #print medias
    
    # plota no grafico    
    plt.plot( range(0,len(medias)), medias, marcadores[i], label=nomesAlg[i])    
    

plt.legend(loc='best')
plt.xlabel('Iteracoes')
plt.ylabel('Media$_{v}$')
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
    
    plt.title('Histograma %s' % (nomesAlg[i]))
    
    plt.show()                   #use may also need add this
    
    std = np.std(h) 
    mean = np.mean(h)    
    print 'std for algorithm %s: %f' % (nomesAlg[i],std)
    print 'mean for algorithm %s: %f'% (nomesAlg[i],mean)

print histoDados[1]