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
import scipy.stats.mstats as mstats # Cálculo média geométrica
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
interS = [5000,10000,15000,20000]
# Problema de otimização: 0 max(1-IC) 1 min(Custo)
problemaOtim = 0

# Problema Knapsack a ser resolvido
'''
AlimPeq - ID 5 W 100 IC 0.5
AlimGra - ID 2 W 150 IC 0.6
'''
W = 100 # ACO com problema relaxado, de cara ja acha solucao boa, problema muito restrito, outros ganham (muito) rapidamente
ICLimite = 0.5 # Problema min(Custo)
M = []
V = []
segmentosGrupos = []
segmentos = []

if not cluster:
    query = ("SELECT DISTINCT EquipamentoMT.ID AS ID, Segmento.ID AS SEGMENTOID, EquipamentoMT.IC AS IC, EquipamentoMT.TIPO_EQUIPAMENTO_ID as TIPOEQP, "
        "IF(EquipamentoMT.TIPO_EQUIPAMENTO_ID != 1, EquipamentoNovo.CUSTO, (EquipamentoNovo.CUSTO/1000*CaboMT.COMPRIMENTO)) AS CUSTO "
        "/*EquipamentoNovo.CUSTO,*/  "
        "/*EquipamentoMT.TIPO_EQUIPAMENTO_ID */ "
        "FROM EquipamentoMT  "
        "JOIN Segmento ON EquipamentoMT.SEGMENTO_ID = Segmento.ID  "
        "JOIN Alimentador ON Segmento.ALIMENTADOR_ID = Alimentador.ID  "
        "JOIN EquipamentoNovo ON EquipamentoNovo.TIPO_EQUIPAMENTO_ID = EquipamentoMT.TIPO_EQUIPAMENTO_ID  "
        "LEFT JOIN CaboMT ON EquipamentoMT.ID = CaboMT.ID  "
        #" ") # SED inteira
        "WHERE Alimentador.ID = 5") # 5 pequeno # 2 grande
        
    cursor.execute(query)
    i = 0
    for(ID,SEGMENTOID,IC,TIPOEQP,CUSTO) in cursor:
        M.append(CUSTO)
        V.append((1-IC))
        if SEGMENTOID not in segmentosGrupos:
            segmentosGrupos.append(SEGMENTOID)
            segmentos.append([])
        posSeg = [k for k,x in enumerate(segmentosGrupos) if x == SEGMENTOID][0]
        segmentos[posSeg].append(i)
        i = i+1

    cursor.close()
    print V
    print M
    print segmentos
    raw_input('pause')
    
else: # Cluster
    M = []
    V = [] # Completar apenas no cluster
    segmentos = [] # lista de listas com os ids(posições) de V e M que formam os segmentos que formam o alimentador
    print 'sum(M): %f sum(V): %f len(segmentos): %d' % (sum(M),sum(V), len(segmentos))


#Configuracoes ILS

# AlimPeq
if problemaOtim == 0:
    iterMaxILS = 60000 #30000 original 60000 avaliacoes
    iterMaxBL = 1
    pPert = 2
    iterMaxBL_P = 1
else:
    iterMaxILS = 150000 #30000 original 150000 avaliacoes
    iterMaxBL = 1
    pPert = 2
    iterMaxBL_P = 1

"""
#AlimGra
if problemaOtim == 0:
    iterMaxILS = 50000
    iterMaxBL = 1
    pPert = 2
    iterMaxBL_P = 1
else:
    iterMaxILS = 70000
    iterMaxBL = 1
    pPert = 2
    iterMaxBL_P = 1
"""
# CONFIGURACOES AG

#AlimPeq
# Configuração max(1-IC)
if problemaOtim == 0:
    geracoes = 300
    tampop = 200
    crossover = 90
    mutacao = 5
    pressaoSel = 4
    cortes = 3
    buscaLocal = 2
else:
    # Configuração min(custo)
    geracoes = 500
    tampop = 300
    crossover = 90
    mutacao = 15
    pressaoSel = 2
    cortes = 3
    buscaLocal = 2
"""
#AlimGra
# Configuração max(1-IC)
if problemaOtim == 0:
    geracoes = 400
    tampop = 600 # Testei com g800 mas na g400/300 já estava bom
    crossover = 90
    mutacao = 5
    pressaoSel = 4
    cortes = 3
    buscaLocal = 2
else:
    # Configuração min(custo)
    geracoes = 300
    tampop = 700 
    crossover = 90
    mutacao = 5
    pressaoSel = 2
    cortes = 3
    buscaLocal = 2
"""
#  Configuracoes ACO

#AlimPeq

if problemaOtim == 0:
    colonias = 400 # 50 convergencia #400 avaliacao
    numForm = 150
    # Constante inicial de ferormonio
    C = 100
    Q = d519.randrange(11,100)
    alpha = 1 # deixar alpha mais forte, aumenta a força do ferormônio, porém retirar alelos aleatórios sem mudar o ferormônio é cagada
    beta = 5
    rho = 0.3

else:
    colonias = 500 # 250 convergencia # 500 avaliacao
    numForm = 300
    # Constante inicial de ferormonio
    C = 100
    Q = d519.randrange(11,100)
    alpha = 1 # deixar alpha mais forte, aumenta a força do ferormônio, porém retirar alelos aleatórios sem mudar o ferormônio é cagada
    beta = 5
    rho = 0.3
"""
#AlimGra
if problemaOtim == 0:
    colonias = 90 # a partir da 80 começa a convergir muito rapido
    numForm = 150
    # Constante inicial de ferormonio
    C = 100
    Q = d519.randrange(11,100)
    alpha = 1 # deixar alpha mais forte, aumenta a força do ferormônio, porém retirar alelos aleatórios sem mudar o ferormônio é cagada
    beta = 5
    rho = 0.3
else:
    colonias = 500
    numForm = 300
    # Constante inicial de ferormonio
    C = 100
    Q = d519.randrange(11,100)
    alpha = 1 # deixar alpha mais forte, aumenta a força do ferormônio, porém retirar alelos aleatórios sem mudar o ferormônio é cagada
    beta = 5
    rho = 0.3
"""

#M = [92,4,43,83,84,68,92,82,6,44,32,18,56,83,25,96,70,48,14,58]
#V = [44,46,90,72,91,40,75,35,8,54,78,40,77,15,61,17,75,29,75,63]
#W = 878

# lista dos métodos a serem chamados
#algoritmos = ['mono_ils','mono_ga', 'mono_aco']
#algoritmos = [ 'mono_ga']
#algoritmos = ['mono_ils', 'mono_ils','mono_ils','mono_ils']
#algoritmos = ['mono_aco','mono_aco','mono_aco','mono_aco','mono_aco']
#algoritmos = ['mono_aco']
#algoritmos = ['mono_ga', 'mono_ga', 'mono_ga', 'mono_ga', 'mono_ga']
#algoritmos = ['mono_ils','mono_ils','mono_ils','mono_ils','mono_ils']
#algoritmos = ['mono_ga','mono_ga','mono_ga', 'mono_ga','mono_ga']
#algoritmos = ['mono_aco','mono_aco','mono_aco','mono_aco','mono_aco']
algoritmos = ['mono_ils', 'mono_ga', 'mono_aco']
#algoritmos = ['mono_aco']

# nomes a serem plotados (caso False, o nome do algoritmo)
#nomesAlg = ['mono_ils', 'mono_ga', 'mono_aco']
#nomesAlg = [ 'mono_ga']
#nomesAlg = ['mono_ils_7000P', 'mono_ils_8000P', 'mono_ils_9000P', 'mono_ils_10000P']
#nomesAlg = ['mono_aco_a1b5', 'mono_aco_a3b5', 'mono_aco_a5b3', 'mono_aco_a5b1', 'mono_aco_a3b3']
#nomesAlg = ['mono_aco']
#nomesAlg = ['mono_ag_BL1', 'mono_ag_BL2', 'mono_ag_BL3', 'mono_ag_BL4', 'mono_ag_BL5']
#nomesAlg = ['mono_ils_BL1','mono_ils_BL2','mono_ils_BL3','mono_ils_BL4','mono_ils_BL5']
#nomesAlg = ['mono_ga_p50','mono_ga_p100','mono_ga_p200','mono_ga_p300', 'mono_ga_p400']
#nomesAlg = ['mono_aco_f10', 'mono_aco_f75', 'mono_aco_f150', 'mono_aco_f300', 'mono_aco_f700']
nomesAlg = ['mono_ils_BL1', 'mono_ga_200', 'mono_aco_150']
#nomesAlg = ['mono_aco_150']

# lista de marcadores do matplotlib
marcadores = ['b*','gx','r+', 'c^', 'mv', 'yo', 'kH']

# Conjunto de parâmetros de cada algoritmo para execução
#todos
#parametrizacao = [[False,iterMaxILS,iterMaxBL,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,interS,segmentos,ICLimite,problemaOtim],[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim]]
#ag
#parametrizacao= [[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,cortes,buscaLocal,interS,segmentos,ICLimite,problemaOtim]]
#ils
#parametrizacao= [[False,15000,10,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim], [False,15000,20,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim], [False,15000,30,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim], [False,15000,40,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim]]
#acos
#parametrizacao=[[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,colonias,numForm,C,Q,3,5,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,colonias,numForm,C,Q,5,3,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,colonias,numForm,C,Q,5,1,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,colonias,numForm,C,Q,3,3,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim]]
#aco
#parametrizacao=[[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim]]
#ag
#parametrizacao = [[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,cortes,1,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,cortes,2,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,cortes,3,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,cortes,4,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,cortes,5,interS,segmentos,ICLimite,problemaOtim]]
#ils
#parametrizacao = [[False,iterMaxILS,1,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,iterMaxILS,2,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,iterMaxILS,3,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,iterMaxILS,4,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,iterMaxILS,5,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim]]
#ag
#parametrizacao = [[False,W,M,V,geracoes,50,crossover,mutacao,pressaoSel,cortes,buscaLocal,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,100,crossover,mutacao,pressaoSel,cortes,buscaLocal,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,200,crossover,mutacao,pressaoSel,cortes,buscaLocal,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,300,crossover,mutacao,pressaoSel,cortes,buscaLocal,interS,segmentos,ICLimite,problemaOtim],[False,W,M,V,geracoes,400,crossover,mutacao,pressaoSel,cortes,buscaLocal,interS,segmentos,ICLimite,problemaOtim]]
#aco
#parametrizacao = [[False,colonias,10,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,colonias,75,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,colonias,150,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,colonias,300,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim],[False,colonias,700,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim]]
#allAval
parametrizacao = [[False,iterMaxILS,1,pPert,iterMaxBL_P,W,M,V,interS,segmentos,ICLimite,problemaOtim], [False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel,cortes,buscaLocal,interS,segmentos,ICLimite,problemaOtim],[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim]]
#parametrizacao = [[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V,interS,segmentos,ICLimite,problemaOtim]]

# Médias das melhores execuções de cada iteração/geração
execucoes = []

for i in range(0,len(algoritmos)): # para cada algoritmo
    execucoes.append([])
    m = __import__ (algoritmos[i])
    toCall = getattr(m,algoritmos[i])
    
    res = []
    for j in range(0,n): # Obter uma lista de 30 execuções cada uma com parametro dentro do AG de gerações/iterações
        print 'Executando o algoritmo \'%s\' da posição %i na vez %i' % (nomesAlg[i],i,j)
        #res = toCall(parametrizacao[i])
        #execucoes[i].append(res)
        res.append(pool.apply_async(toCall,[parametrizacao[i]]))
    start_time = timeit.default_timer()    
    print 'Executando as %d vezes... ' % (len(res))    
    for j in range(0,len(res)):
        execucoes[i].append(res[j].get())
    if problemaOtim == 0:
        print 'Valor maximo da primeira execucao: %f' % (max(execucoes[i][0][0]))
    else:
        print 'Valor minimo da primeira execucao: %f' % (min(execucoes[i][0][0]))
    elapsed = timeit.default_timer() - start_time
    print 'Tempo de execucao médio para o algoritmo %s: %f segundos' % (nomesAlg[i],elapsed/float(n))

print '----------------------'

# Depois de todos os algoritmos rodados, crio uma média das iterações dos algoritmos para plotar
# e faço um único gráfico com os resultados

for i in range(0,len(algoritmos)):
    # Recrio uma lista apenas com as melhores (problemas com zip())
    best = []
    for j in range(0,len(execucoes[i])):
        teste = execucoes[i][j][0]
        best.append(teste) # teste[1::300] ils teste[1::5] ga
    
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
    print 'plt.legend(loc=\'best\')'
    print 'plt.grid()'
    print 'plt.show()'
    print "\n\nHISTOGRAMAS\n\n"
    # O histograma é feito fora porque o cluster nao tem numpy
    histoDados = []
    for i in range(0,len(algoritmos)):
        histoDados.append([])
        for j in range(0,len(execucoes[i])):
            if problemaOtim == 0:
                histoDados[i].append(max(execucoes[i][j][0])) # tera cada melhor das 30 execucoes
            else:
                histoDados[i].append(min(execucoes[i][j][0])) # tera cada melhor das 30 execucoes
        
        h = sorted(histoDados[i])  #sorted
        print 'fit = stats.norm.pdf(',h,', np.mean(',h,'), np.std(',h,'))'
        print 'plt.figure()'
        print 'plt.plot(',h,',fit,\'-o\')'
        print 'plt.hist(',h,',normed=True)'
        
        print 'plt.title(\'Histograma ',nomesAlg[i],'\') '

        print 'plt.show()'
        print 'std = np.std(',h,')'
        print 'mean = np.mean(',h,')'
        print 'z,pval = stats.mstats.normaltest(',h,')'
        print 'print \'std for algorithm %s: %f\' % (\'',nomesAlg[i],'\',std)'
        print 'print \'mean for algorithm %s: %f\' % (\'',nomesAlg[i],'\',mean)'
        print 'print \'p-value %s: %f\' % (\'',nomesAlg[i],'\',pval)'
        
    print '---\nExecuções intermediárias'
    for i in range(0,len(algoritmos)):
        # Recrio uma lista apenas com as soluções intermediárias (problemas com zip())
        parciais = []
        avaliacao = 0
        for j in range(0,len(execucoes[i])):
            parciais.append(execucoes[i][j][1])
            avaliacao = avaliacao + execucoes[i][j][2]
        # Crio uma única lista com a soma de todas as execuções
        zipped_list = zip(*parciais)
        medias = [sum(item)/float(n) for item in zipped_list]
        
        print 'Médias parciais do alg %s' % (nomesAlg[i])
        print medias
        print 'Avaliacoes Media do alg %s: %d' % (nomesAlg[i], avaliacao/float(n))
    sys.exit(0) #Exits with zero, which is generally interpreted as success. Non-zero codes are usually treated as errors. The default is to exit with zero.

plt.legend(loc='best')

if problemaOtim == 0:
    plt.xlabel(u'Gerações (x5)')
    plt.ylabel(u'Média$_{v}$')
    plt.title(u'max(1-$\overline{IC}$)')
else:
    plt.xlabel(u'Gerações (x5)')
    plt.ylabel(u'Média$_{p}$')
    plt.title(u'min(Custo)')
plt.grid()
plt.show()

# Salvo os histogramas

# Recupero o melhor resultado das 30 execuções e ploto o histograma pra cada algoritmo, ou seja, o último vetor de cada execução que contém a resposta final
histoDados = []
for i in range(0,len(algoritmos)):
    histoDados.append([])
    for j in range(0,len(execucoes[i])):
        if problemaOtim == 0:
            histoDados[i].append(max(execucoes[i][j][0])) # tera cada melhor das 30 execucoes
        else:
            histoDados[i].append(min(execucoes[i][j][0])) # tera cada melhor das 30 execucoes
    
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
    z,pval = stats.mstats.normaltest(h)
    print 'std for algorithm %s: %f' % (nomesAlg[i],std)
    print 'mean for algorithm %s: %f'% (nomesAlg[i],mean)
    print 'p-value %s: %f'% (nomesAlg[i],pval)

for i in range(0,len(histoDados)):
    print 'histoDados do algoritmo %s:' % (nomesAlg[i])
    print histoDados[i]
    
print '---\nExecuções intermediárias e Avaliacoes'
for i in range(0,len(algoritmos)):
    # Recrio uma lista apenas com as soluções intermediárias (problemas com zip())
    parciais = []
    avaliacao = 0
    for j in range(0,len(execucoes[i])):
        parciais.append(execucoes[i][j][1])
        avaliacao = avaliacao + execucoes[i][j][2]
    # Crio uma única lista com a soma de todas as execuções
    zipped_list = zip(*parciais)
    medias = [sum(item)/float(n) for item in zipped_list]
    
    print 'Médias parciais do alg %s' % (nomesAlg[i])
    print medias
    print 'Avaliacoes Media do alg %s: %d' % (nomesAlg[i], avaliacao/float(n))
    
pool.terminate()