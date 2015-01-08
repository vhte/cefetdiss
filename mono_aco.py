# -*- coding: utf-8 -*-
"""
Ant Colony Optimization

Problema: Otimização mono-objetivo para maximização de IC com limite de custo

Entrada: Equipamentos do Segmento
Saida: Melhor solução de troca

Este algoritmo segue a adaptação do AS (Ant System) de acordo com o trabalho de Hanxiao Shi, "Solution to 0/1 Knapsack Problem Based on Improved Ant Colony Algorithm," Information Acquisition, 2006 IEEE International Conference on , vol., no., pp.1062,1066, 20-23 Aug. 2006
doi: 10.1109/ICIA.2006.305887

@author Victor Torres - victorhugo@lsi.cefetmg.br

https://pythonhosted.org/ete2/tutorial/tutorial_trees.html
http://stackoverflow.com/questions/2349991/python-how-to-import-other-python-files
http://stackoverflow.com/questions/9542738/python-find-in-list
"""

import d519

########### PARAMETROS ###########
# Numero de iteracoes
g = 100
# Numero de formigas
m = 100 # Generally, it is defined that the number of ants (m) is equal to that of articles (n)

"""
# Limite knapsack
W = 269
# Peso
M = [95, 4, 60, 32, 23, 72, 80, 62, 65,46]
# Valor
V = [55, 10, 47, 5, 4, 50, 8, 61, 85, 87]

W=878
M=[92,4,43,83,84,68,92,82,6,44,32,18,56,83,25,96,70,48,14,58]
V=[44,46,90,72,91,40,75,35,8,54,78,40,77,15,61,17,75,29,75,63]
"""
W=1500 # Best ~ V = 1020
M=[8, 19, 38, 66, 15, 62, 19, 95, 74, 55, 7, 41, 65, 65, 61, 29, 82, 45, 27, 7, 97, 79, 91, 14, 93, 41, 61, 55, 80, 74, 27, 66, 72, 49, 33, 47, 55, 61, 40, 16, 60, 29, 68, 9, 21, 88, 74, 10, 32, 96, 45, 98, 39, 42, 9, 40, 48, 2, 56, 36, 7, 50, 52, 59, 98, 64, 52, 87, 54, 23, 64, 84, 18, 64, 92, 56, 40, 31, 47, 36, 80, 61, 27, 61, 35, 55, 34, 39, 46, 82, 42, 81, 35, 10, 54, 24, 84, 2, 11, 49]
V=[27, 48, 99, 54, 42, 43, 38, 96, 49, 81, 85, 63, 89, 46, 73, 3, 9, 3, 89, 89, 20, 32, 1, 92, 88, 71, 76, 47, 7, 32, 22, 66, 32, 26, 1, 94, 6, 58, 67, 37, 58, 94, 79, 1, 17, 1, 65, 61, 92, 57, 67, 60, 78, 23, 93, 58, 52, 82, 50, 24, 49, 42, 54, 21, 83, 70, 1, 53, 7, 5, 3, 26, 60, 98, 21, 71, 19, 36, 74, 50, 16, 97, 15, 24, 8, 78, 9, 67, 22, 41, 17, 11, 87, 25, 87, 89, 69, 4, 7, 27]

# Total itens
n = len(M)
# Constante inicial de ferormonio
C = 1
# Constante Q randômica para cálculo de G(Weight_k) 10 < Q < 100
Q = d519.randrange(11,100)
# Constantes alpha e beta para função de probabilidade 0 < alpha < 5 e 0 <= beta <= 5
alpha = 3
beta = 3
# Permanencia do ferormonio 
rho = 0.7
# Lista de ferormonio em cada item
ferormonio = [C] * n
ferormonioDelta = [0] * n

class Ant:
    """
    Nesta modelagem, cada formiga é um objeto com suas propriedades de solução.
    Os itens estão representados pelos vetores M e V e os ferormônios atualizados também de acordo com eles
    """
    tabu = [0]
    allowed = [1]
    FO = 0 # Função objetivo
    
    # Inicia a formiga colocando ela em um determinado item já (posição)
    def __init__(self,n):
        self.tabu = self.tabu * n
        self.allowed = self.allowed * n
        # Colocando a formiga em uma posição (item) aleatória para começar
        pos = d519.randrange(0,n)
        self.tabu[pos] = 1
        self.allowed[pos] = 0
        
    def calculaDeltaTau(self,item):
        weightFormiga = self.calculaPeso()
        GWeightFormiga = float(Q)/weightFormiga
        return M[item] * GWeightFormiga
        
    def calculaPeso(self):
        peso = 0
        for i in range(0,len(self.tabu)):
            if self.tabu[i] == 1:
                peso = peso + M[i]
        return peso
    def calculaValor(self):
        valor = 0
        for i in range(0,len(self.tabu)):
            if self.tabu[i] == 1:
                valor = valor + V[i]
        return valor
        
def quicksort(v, w):
    """
    Utilizando o quicksort, organizo somente as posições que devem ser escolhidas na roleta do dicionário de probabilidades
    Para não perder os índices, utilizo a estrutura de dicionário com o índice sendo a posição do vetor P selecionado e o valor, o valor de P daquela posição selecionada
    """
    # Transformo v e w num dicionário primeiro. É necessário que len(v) = len(w)
    dicio= {}
    for i in range(0,len(v)):
        dicio[v[i]] = w[i]
        
    if len(dicio) <= 1:
        return dicio.keys() # uma lista vazia ou com 1 elemento ja esta ordenada
    less, equal, greater = [], [], [] # cria as sublistas dos maiores, menores e iguais ao pivo
    less2,equal2,greater2= [],[],[]
    pivot = dicio.itervalues().next() # escolhe o pivo. neste caso, o primeiro elemento da lista
    for x in dicio:
        # adiciona o elemento x a lista correspondeste
        if dicio[x] < pivot:
            less.append(dicio[x])
            less2.append(x)
        elif dicio[x] == pivot:
            equal.append(dicio[x])
            equal2.append(x)
        else:
            greater.append(dicio[x])
            greater2.append(x)
    return quicksort(less2,less) + equal2 + quicksort(greater2, greater) # concatena e retorna recursivamente
    
def roleta(aux, P):
    # Gera um número aleatório [0,1]
    roleta = d519.randrange(0,100)/float(100)
    
    i = 0
    total = 0
    while True:
        total = total+P[aux[i]]
        if total < roleta:
            # Passa para proximo
            i = i+1
        else:
            return aux[i] # selecionado
            
####################### MAIN #######################
def mono_aco(params):
    debug = params[0]
    
    melhoresGeracao = [] # a resposta do algoritmo, para cada geração uma única resposta será enviada
    
    # inicializando dicionário de probabilidade de escolha do item
    P = {}
    for i in range(0,n):
        P[i] = 0
    if debug:
        print 'Inicializou o dicionário de probabilidades'
    
    ########### INICIO ###########
    # Gerando n formigas em ants e colocando cada n formiga em uma posição aleatória de um item
    ants = []
    for i in range(0,m):
        ants.append(Ant(n))
        #print ants[i].itensVisitados
    if debug:
        print 'Gerou as formigas'
    
    
    # Inicializando  conunto solucoes (colonias)
    for i in range(0,g):
        if debug:
            print 'Inicializando colônia %d' % (i)
        
        # Inicializando lista de ferormonio em cada item e ferormonio acumulado em cada item
        for i in range(0,n): # Cada item tem um delta tau
            for j in range(0,m): # Cada delta tau de item é somatorio de delta tau de todo delta tau de cada formiga
                ferormonioDelta[i] = ferormonioDelta[i] + ants[j].calculaDeltaTau(i)
        if debug:
            print '   Calculou ferormonioDelta para cada item'
        
        # para cada formiga
        for j in range(0,m):
            if debug:
                print '   Iniciando formiga %d da colônia %d' % (i,j)
            # selecionar o próximo item (j) baseado na equacao de probabilidade
            # Crio um vetor auxiliar com todas as posições de allowed ordenadas por P de forma ascendente
            aux = [] * len([x for x in ants[j].allowed if x == 1])
            somatorioAllowed = 0
            # Somatório do denominador com allowed da formiga j
            for l in range(0,n):
                if ants[j].allowed[l] == 1:
                    somatorioAllowed = somatorioAllowed + pow(float(V[l])/M[l], alpha) * pow(ferormonio[l], beta)
            # Calculo a probabilidade para todos os itens de allowed (pois tabu ja estao dentro do "caminho" da formiga)
            if debug:
                print '   Calculando a lista P[] com as probabilidades de escolha'
            for k in range(0,n):
                if ants[j].tabu[k] == 1: # Apenas em allowed
                    continue
                # adiciono o indice do item em aux
                aux.append(k)
                
                # Probabilidade do item k ser escolhido
                P[k] = float((pow(ferormonio[k],alpha) * pow(float(V[k])/M[k], beta))) / (somatorioAllowed)
            #print P
            # Ordeno aux do menor P[k] para maior
            # Aqui vai depender do tamanho de itens a serem ordenados. Usando quicksort O(n^2) pior caso
            aux = quicksort(aux, [P[x] for x in P if x in aux]) #  P[x] para value
            
            # Com as probabilidades montadas, gerar a estrutura para roleta
            selecionado = roleta(aux, P)
            if debug:
                print '   Selecionou o item da posição %d na roleta' % (selecionado)
            # Retirar de allowed e adicionar em tabu na formiga j
            ants[j].allowed[selecionado] = 0
            ants[j].tabu[selecionado] = 1
            # Verifico se a soma de tabu da formiga excede o peso da mochila
            # Caso exceda, utilizar a solução corrente até então; Caso não, adiciona o item da roleta
            if ants[j].calculaPeso() > W:
                ants[j].allowed[selecionado] = 1
                ants[j].tabu[selecionado] = 0
            
            # Atualiza ferormonio
            for k in range(0,n):
                ferormonio[k] = rho*ferormonio[k] + ferormonioDelta[k]
                
            if debug:
                print '   Parcial Colonia %d Formiga %d: %f' % (i, j,ants[j].calculaValor())
            
        # Reseto o ferormonio acumulado de todos os itens
        # DUVIDA: CHECAR NOVAMENTE USO DE ferormonioDelta
        for j in range(0,n):
            ferormonioDelta[j] = 0
        
        # Verifico quem é o melhor para adicionar em melhoresGeracao
        # Imprime melhor solução FACTÍVEL
        best = [-1, 0, 0]
        for j in range(0,m):
            if ants[j].calculaValor() > best[1] and ants[j].calculaPeso() <= W:
                best = [j, ants[j].calculaValor(), ants[j].calculaPeso()]
        if best[0] == -1:
            if debug:
                print 'Nao obteve solução factível ):'
            melhoresGeracao.append(0)
        else:
            melhoresGeracao.append(best[1])
    
    # exibir resultado de todas as formigas e achar a melhor
    melhor = [0 ,0]
    for i in range(0,m):
        if ants[i].calculaValor() > melhor[1]:
            melhor = [i, ants[i].calculaValor()]
        if debug:
            print 'Formiga %d: %f' % (i, ants[i].calculaValor())
    if debug:    
        print 'Melhor Formiga: %d com Valor: %f' % (melhor[0], melhor[1])
        print 'Lista de artigos da melhor formiga: '
        print ants[melhor[0]].tabu
    
    return melhoresGeracao
#mono_aco(True)