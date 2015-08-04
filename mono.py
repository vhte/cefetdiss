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
import timeit
import sys
from multiprocessing import Pool

cluster = False

if not cluster:
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy.stats as stats
    import mysql.connector
    plt.ion()

    cnx = mysql.connector.connect(user='root', password='root', database='cemig_d519')
    cursor = cnx.cursor()

pool = Pool(processes=None) # If processes is None then the number returned by cpu_count() is used.

# Quantidade de vezes a ser executado
n = 30
# Solucoes intermediarias a salvar
interS = [20,30,40,50]

# Problema Knapsack a ser resolvido
W = 100 # ACO com problema relaxado, de cara ja acha solucao boa, problema muito restrito, outros ganham (muito) rapidamente
M = []
V = []


if not cluster:
    query = ("SELECT DISTINCT EquipamentoMT.ID AS ID, EquipamentoMT.IC AS IC, "
        "IF(EquipamentoMT.TIPO_EQUIPAMENTO_ID != 1, EquipamentoNovo.CUSTO, (EquipamentoNovo.CUSTO/1000*CaboMT.COMPRIMENTO)) AS CUSTO "
        "/*EquipamentoNovo.CUSTO,*/  "
        "/*EquipamentoMT.TIPO_EQUIPAMENTO_ID */ "
        "FROM EquipamentoMT  "
        "JOIN Segmento ON EquipamentoMT.SEGMENTO_ID = Segmento.ID  "
        "JOIN Alimentador ON Segmento.ALIMENTADOR_ID = Alimentador.ID  "
        "JOIN EquipamentoNovo ON EquipamentoNovo.TIPO_EQUIPAMENTO_ID = EquipamentoMT.TIPO_EQUIPAMENTO_ID  "
        "LEFT JOIN CaboMT ON EquipamentoMT.ID = CaboMT.ID  "
        "WHERE Alimentador.ID = 5")
        
    cursor.execute(query)
    for(ID,IC,CUSTO) in cursor:
        M.append(CUSTO)
        V.append((1-IC))
    cursor.close()
else: # Cluster
    M = []
    V = [] # Completar apenas no cluster
print sum(V)
print sum(M)
raw_input('pause')
'''
print M
print V
raw_input('wait')
'''
#Configuracoes ILS
iterMaxILS = 14000
iterMaxBL = 10
pPert = 0.001
iterMaxBL_P = 1

# Configuracoes AG
geracoes = 3500
tampop = 300
crossover = 90
mutacao = 5
pressaoSel = 3

#  Configuracoes ACO
colonias = 3000
numForm = 10
# Constante inicial de ferormonio
C = 100
Q = d519.randrange(11,100)
alpha = 1 # deixar alpha mais forte, aumenta a força do ferormônio, porém retirar alelos aleatórios sem mudar o ferormônio é cagada
beta = 5
rho = 0.3
#M = [92,4,43,83,84,68,92,82,6,44,32,18,56,83,25,96,70,48,14,58]
#V = [44,46,90,72,91,40,75,35,8,54,78,40,77,15,61,17,75,29,75,63]
#W = 878

# lista dos métodos a serem chamados
#algoritmos = ['mono_ils','mono_ga', 'mono_aco']
#algoritmos = [ 'mono_ga','mono_ga','mono_ga','mono_ga', 'mono_ga']
#algoritmos = ['mono_ils', 'mono_ils','mono_ils','mono_ils']
#algoritmos = ['mono_aco','mono_aco','mono_aco','mono_aco']
#algoritmos = ['mono_aco']
#algoritmos = ['mono_ga', 'mono_ga', 'mono_ga', 'mono_ga']
#algoritmos = ['mono_ils']
algoritmos = ['mono_ga']

# nomes a serem plotados (caso False, o nome do algoritmo)
#nomesAlg = ['mono_ils', 'mono_ga', 'mono_aco']
#nomesAlg = [ 'mono_ga_pop100', 'mono_ga_pop150', 'mono_ga_pop200', 'mono_ga_pop250', 'mono_ga_pop300']
#nomesAlg = ['mono_ils_7000P', 'mono_ils_8000P', 'mono_ils_9000P', 'mono_ils_10000P']
#nomesAlg = ['mono_aco_1_5', 'mono_aco_5_1', 'mono_aco_3_3', 'mono_aco_2_4']
#nomesAlg = ['mono_aco']
#nomesAlg = ['mono_ga_p100', 'mono_ga_p150', 'mono_ga_p200', 'mono_ga_p300']
#nomesAlg = ['mono_ils']
nomesAlg = ['mono_ga']

# lista de marcadores do matplotlib
marcadores = ['b-','g-','r-', 'c-', 'm-', 'y-', 'k-']

# Conjunto de parâmetros de cada algoritmo para execução
#todos
#parametrizacao = [[False,iterMaxILS,iterMaxBL,pPert,iterMaxBL_P,W,M,V,interS],[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,interS],[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V,interS]]
#ag
#parametrizacao= [[False,W,M,V,geracoes,100,crossover,mutacao,pressaoSel], [False,W,M,V,geracoes,150,crossover,mutacao,pressaoSel], [False,W,M,V,geracoes,200,crossover,mutacao,pressaoSel], [False,W,M,V,geracoes,250,crossover,mutacao,pressaoSel], [False,W,M,V,geracoes,300,crossover,mutacao,pressaoSel]]
#ils
#parametrizacao= [[False,15000,10,pPert,iterMaxBL_P,W,M,V,interS], [False,15000,20,pPert,iterMaxBL_P,W,M,V,interS], [False,15000,30,pPert,iterMaxBL_P,W,M,V,interS], [False,15000,40,pPert,iterMaxBL_P,W,M,V,interS]]
#acos
#parametrizacao=[[False,colonias,10,C,Q,alpha,beta,rho,W,M,V,interS],[False,colonias,20,C,Q,alpha,beta,rho,W,M,V,interS],[False,colonias,30,C,Q,alpha,beta,rho,W,M,V,interS],[False,colonias,40,C,Q,alpha,beta,rho,W,M,V,interS]]
#aco
#parametrizacao=[[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V,interS]]
#ag
#parametrizacao = [[False,W,M,V,geracoes,350,crossover,mutacao,pressaoSel,interS],[False,W,M,V,geracoes,400,crossover,mutacao,pressaoSel,interS],[False,W,M,V,geracoes,450,crossover,mutacao,pressaoSel,interS],[False,W,M,V,geracoes,500,crossover,mutacao,pressaoSel,interS]]
#ils
#parametrizacao = [[False,iterMaxILS,iterMaxBL,pPert,iterMaxBL_P,W,M,V,interS]]
#ag
parametrizacao = [[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,interS]]

# Médias das melhores execuções de cada iteração/geração
execucoes = []

for i in range(0,len(algoritmos)): # para cada algoritmo
    execucoes.append([])
    m = __import__ (algoritmos[i])
    toCall = getattr(m,algoritmos[i])
    start_time = timeit.default_timer()
    
    res = []
    for j in range(0,n): # Obter uma lista de 30 execuções cada uma com parametro dentro do AG de gerações/iterações
        print 'Executando o algoritmo \'%s\' da posição %i na vez %i' % (nomesAlg[i],i,j)
        #res = toCall(parametrizacao[i])
        #execucoes[i].append(res)
        res.append(pool.apply_async(toCall,[parametrizacao[i]]))
    print 'Executando %d vezes' % (len(res))
    for j in range(0,len(res)):
        execucoes[i].append(res[j].get())
    print 'Valor maximo da primeira execucao: %f' % (max(execucoes[i][0][0]))
    elapsed = timeit.default_timer() - start_time
    print 'Tempo de execucao das %i vezes: %f segundos' % (n,elapsed)

print '----------------------'

# Depois de todos os algoritmos rodados, crio uma média das iterações dos algoritmos para plotar
# e faço um único gráfico com os resultados

for i in range(0,len(algoritmos)):
    # Recrio uma lista apenas com as melhores (problemas com zip())
    best = []
    for j in range(0,len(execucoes[i])):
        best.append(execucoes[i][j][0])
    
    # Crio uma única lista com a soma de todas as execuções
    #zipped_list = zip(*execucoes[i])
    zipped_list = zip(*best)
    medias = [sum(item)/float(n) for item in zipped_list]

    # @todo olhar se python tem operador ternário
    if not nomesAlg[i]:
        nomesAlg[i] = algoritmos[i]
    
    print 'Resultado final (medias) para o algoritmo %s:' % (nomesAlg[i])
    #print medias
    
    if not cluster:
        # plota no grafico    
        plt.plot( range(0,len(medias)), medias, marcadores[i], label=nomesAlg[i])
    else:
        print  'plt.plot(',range(0,len(medias)),', ',medias,', \'',marcadores[i],'\', label=\'',nomesAlg[i],'\')'
    
if cluster:
    print "\n\nHISTOGRAMAS\n\n"
    # O histograma é feito fora porque o cluster nao tem numpy
    histoDados = []
    for i in range(0,len(algoritmos)):
        histoDados.append([])
        for j in range(0,len(execucoes[i])):
            histoDados[i].append(max(execucoes[i][j][0])) # tera cada melhor das 30 execucoes
        
        h = sorted(histoDados[i])  #sorted
        print 'fit = stats.norm.pdf(',h,', np.mean(',h,'), np.std(',h,'))'
        print 'plt.figure()'
        print 'plt.plot(',h,',fit,\'-o\')'
        print 'plt.hist(',h,',normed=True)'
        
        print 'plt.title(\'Histograma ',nomesAlg[i],'\') '
        
        print 'plt.show()'
    sys.exit(0) #Exits with zero, which is generally interpreted as success. Non-zero codes are usually treated as errors. The default is to exit with zero.

plt.legend(loc='best')
plt.xlabel(u'Gerações')
plt.ylabel(u'Média$_{v}$')
plt.title(u'max(1-$\overline{IC}$)')
plt.grid()
plt.show()


# Salvo os histogramas

# Recupero o melhor resultado das 30 execuções e ploto o histograma pra cada algoritmo, ou seja, o último vetor de cada execução que contém a resposta final
histoDados = []
for i in range(0,len(algoritmos)):
    histoDados.append([])
    for j in range(0,len(execucoes[i])):
        histoDados[i].append(max(execucoes[i][j][0])) # tera cada melhor das 30 execucoes
    
    h = sorted(histoDados[i])  #sorted

    # norm: A normal continuous random variable.
    #The probability density function for norm is:
    #norm.pdf(x) = exp(-x**2/2)/sqrt(2*pi)
    fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
    
    plt.figure()
    
    plt.plot(h,fit,'-o')
    
    plt.hist(h,normed=True)      #use this to draw histogram of your data
    
    plt.title('Histograma %s' % (nomesAlg[i]))
    
    plt.show()                   #use may also need add this
    
    std = np.std(h) 
    mean = np.mean(h)    
    print 'std for algorithm %s: %f' % (nomesAlg[i],std)
    print 'mean for algorithm %s: %f'% (nomesAlg[i],mean)

for i in range(0,len(histoDados)):
    print 'histoDados do algoritmo %s:' % (nomesAlg[i])
    print histoDados[i]
    
print '---\nExecuções intermediárias'
for i in range(0,len(algoritmos)):
    # Recrio uma lista apenas com as soluções intermediárias (problemas com zip())
    parciais = []
    for j in range(0,len(execucoes[i])):
        parciais.append(execucoes[i][j][1])
    # Crio uma única lista com a soma de todas as execuções
    zipped_list = zip(*parciais)
    medias = [sum(item)/float(n) for item in zipped_list]
    
    print '\nMédia do alg %s' % (nomesAlg[i])
    print medias
    
pool.terminate()