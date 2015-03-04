# -*- coding: utf-8 -*-
"""
Ant Colony Optimization

Problema: Otimização mono-objetivo para maximização de IC com limite de custo

Entrada: Equipamentos do Segmento
Saida: Melhor solução de troca

Este algoritmo segue a adaptação do AS (Ant System) de acordo com o trabalho de Hanxiao Shi, "Solution to 0/1 Knapsack Problem Based on Improved Ant Colony Algorithm," Information Acquisition, 2006 IEEE International Conference on , vol., no., pp.1062,1066, 20-23 Aug. 2006
doi: 10.1109/ICIA.2006.305887

@author Victor Torres - victorhugo@lsi.cefetmg.br
@todo Não deixar entrar solucao infactivel no resultdo, igual no AG

https://pythonhosted.org/ete2/tutorial/tutorial_trees.html
http://stackoverflow.com/questions/2349991/python-how-to-import-other-python-files
http://stackoverflow.com/questions/9542738/python-find-in-list
"""

import d519

class Ant:
    """
    Nesta modelagem, cada formiga é um objeto com suas propriedades de solução.
    Os itens estão representados pelos vetores M e V e os ferormônios atualizados também de acordo com eles
    """
    tabu = [0]
    allowed = [1]
    valor = 0
    peso = 0
    
    # Lista de itens que tentaram ser adicionados a esta formiga mas extrapolaram o peso permitido W
    inuteis = []
    
    # Inicia a formiga colocando ela em um determinado item já (posição)
    def __init__(self,n):
        self.tabu = self.tabu * n
        self.allowed = self.allowed * n
        # Colocando a formiga em uma posição (item) aleatória para começar
        pos = d519.randrange(0,n)
        self.tabu[pos] = 1
        self.allowed[pos] = 0
        self.valor = self.valor + V[pos]
        self.peso = self.peso + M[pos]
        
    def calculaDeltaTau(self,item):
        weightFormiga = self.peso
        GWeightFormiga = float(Q)/weightFormiga
        return M[item] * GWeightFormiga
        
    def calculaPeso(self):
        peso = 0
        for i in range(0,len(self.tabu)):
            if self.tabu[i] == 1:
                peso = peso + M[i]
        self.peso = peso
    def calculaValor(self):
        valor = 0
        for i in range(0,len(self.tabu)):
            if self.tabu[i] == 1:
                valor = valor + V[i]
        self.valor = valor
        
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
    global W,V,M,Q,n
    debug = params[0]
    
    ########### PARAMETROS ###########
    # Numero de iteracoes
    g = params[1]
    # Numero de formigas
    m = params[2] # Generally, it is defined that the number of ants (m) is equal to that of articles (n)
    
    W = params[8]
    M = params[9]
    V = params[10]
    # Total itens
    n = len(M)
    # Constante inicial de ferormonio
    C = params[3]
    # Constante Q randômica para cálculo de G(Weight_k) 10 < Q < 100
    Q = params[4]
    # Constantes alpha e beta para função de probabilidade 0 < alpha < 5 e 0 <= beta <= 5
    alpha = params[5]
    beta = params[6]
    # Permanencia do ferormonio 
    rho = params[7]
    # Lista de ferormonio em cada item
    ferormonio = [C] * n
    ferormonioDelta = [0] * n
    
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
        for j in range(0,n): # Cada item tem um delta tau
            for k in range(0,m): # Cada delta tau de item é somatorio de delta tau de todo delta tau de cada formiga
                ferormonioDelta[j] = ferormonioDelta[j] + ants[k].calculaDeltaTau(j)
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
            
            tentativas = 0
            while ants[j].peso + M[selecionado] > W and tentativas < int(n*0.05):
                # Adição inválida, rodo a roleta de novo até encontrar alguem ou 5% sem encontrar ninguém (convergência)
                selecionado = roleta(aux, P)
                tentativas = tentativas +1
            
            if ants[j].peso + M[selecionado] <= W:
                # Retirar de allowed e adicionar em tabu na formiga j
                ants[j].allowed[selecionado] = 0
                ants[j].tabu[selecionado] = 1
                ants[j].valor = ants[j].valor + V[selecionado]
                ants[j].peso = ants[j].peso + M[selecionado]
            
            # Atualiza ferormonio
            for k in range(0,n):
                ferormonio[k] = rho*ferormonio[k] + ferormonioDelta[k]
                
            if debug:
                print '   Parcial Colonia %d Formiga %d: %f' % (i, j,ants[j].valor)
            
        # Reseto o ferormonio acumulado de todos os itens
        # Como vai começar uma nova colônia, o peso das formigas já mudou e por isto um novo ferormonioDelta deve ser calculado
        for j in range(0,n):
            ferormonioDelta[j] = 0
        
        # Verifico quem é o melhor para adicionar em melhoresGeracao
        # Imprime melhor solução FACTÍVEL
        best = [-1, 0, 0]
        for j in range(0,m):
            if ants[j].valor > best[1] and ants[j].peso <= W:
                best = [j, ants[j].valor, ants[j].peso]
        if best[0] == -1:
            if debug:
                print 'Nao obteve solução factível ):'
            melhoresGeracao.append(0)
        else:
            melhoresGeracao.append(best[1])
    
    # exibir resultado de todas as formigas e achar a melhor
    melhor = [0 ,0]
    for i in range(0,m):
        if ants[i].valor > melhor[1]:
            melhor = [i, ants[i].valor]
        if debug:
            print 'Formiga %d: %f' % (i, ants[i].valor)
    if debug:    
        print 'Melhor Formiga: %d com Valor: %f' % (melhor[0], melhor[1])
        print 'Lista de artigos da melhor formiga: '
        print ants[melhor[0]].tabu
    
    return melhoresGeracao
#print mono_aco([False])