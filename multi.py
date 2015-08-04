# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:49:59 2015

multi.py

Executa os algoritmos multi-objetivo
Plota no mesmo gráfico as soluções

@author: victor
@todo Hipervolume
"""
import d519
import multi_nsgaII
import multi_spea2
import mono_aco
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import mysql.connector
import timeit

plt.ion()
cnx = mysql.connector.connect(user='root', password='root', database='cemig_d519')
cursor = cnx.cursor()

# Loops principais (gerações, colônias, iterações, etc...)
loops = 500
tampop = 50

# Problema Knapsack a ser resolvido
W = 200
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
    "WHERE Alimentador.ID = 13")
    
cursor.execute(query)
for(ID,IC,CUSTO) in cursor:
    M.append(CUSTO)
    V.append((1-IC))

#Configuracoes NSGAII
geracoesN = 1000
tampopN = 50
crossoverN = 90
mutacaoN = 5
pressaoSelN = 3

# Configuracoes SPEA2
geracoesS = 1000
tampopS = 50
crossoverS = 90
mutacaoS = 5
pressaoSelS = 3

#  Configuracoes MACO
colonias = 70
numForm = 20
# Constante inicial de ferormonio
C = 1
Q = d519.randrange(11,100)
alpha = 1 #27
beta = 1
rho = 0.7 
#M = [92,4,43,83,84,68,92,82,6,44,32,18,56,83,25,96,70,48,14,58]
#V = [44,46,90,72,91,40,75,35,8,54,78,40,77,15,61,17,75,29,75,63]
#W = 878

# lista dos métodos a serem chamados
algoritmos = [ 'multi_nsgaII','multi_spea2','multi_maco']

# nomes a serem plotados (caso False, o nome do algoritmo)
#nomesAlg = ['mono_ils', 'mono_ga', 'mono_aco']
nomesAlg = ['multi_nsgaII','multi_spea2','multi_maco']

# lista de marcadores do matplotlib
marcadores = ['b-','g-','r-', 'c-', 'm-', 'y-', 'k-']

# Conjunto de parâmetros de cada algoritmo para execução
#todos
parametrizacao = [[False,iterMaxILS,iterMaxBL,pPert,iterMaxBL_P,W,M,V],[False,W,M,V,geracoes,tampop,crossover,mutacao,pressaoSel],[False,colonias,numForm,C,Q,alpha,beta,rho,W,M,V]]

# Médias das melhores execuções de cada iteração/geração
execucoes = []

for i in range(0,len(algoritmos)): # para cada algoritmo
    execucoes.append([])
    m = __import__ (algoritmos[i])
    toCall = getattr(m,algoritmos[i])
    start_time = timeit.default_timer()

    print 'Executando o algoritmo \'%s\' da posição %i' % (nomesAlg[i],i)
    res = toCall(parametrizacao[i])
    execucoes[i] = res
    print 'Valor maximo da primeira execucao: %f' % (max(execucoes[i][0]))
    elapsed = timeit.default_timer() - start_time
    print 'Tempo de execucao do algoritmo: %f segundos' % (elapsed)

print '----------------------'

# Depois de todos os algoritmos rodados, crio uma média das iterações dos algoritmos para plotar
# e faço um único gráfico com os resultados

for i in range(0,len(algoritmos)):
    # @todo olhar se python tem operador ternário
    if not nomesAlg[i]:
        nomesAlg[i] = algoritmos[i]
    
    print 'Resultado final para o algoritmo %s:' % (nomesAlg[i])
    #print medias
    
    # plota no grafico    
    plt.plot( range(0,len(execucoes[i])),execucoes[i], marcadores[i], label=nomesAlg[i])
    

plt.legend(loc='best')
plt.xlabel('Iteracoes')
plt.ylabel('Media$_{v}$')
plt.grid()
plt.show()