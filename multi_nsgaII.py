# -*- coding: utf-8 -*-
"""
Non-Dominated Sorting Genetic Algorithm II
Problema: Otimização mono-objetivo para maximização de IC com limite de custo
Entrada: Equipamentos do Segmento
Saida: Melhor solução de troca

@author Victor Torres

https://pythonhosted.org/ete2/tutorial/tutorial_trees.html
http://stackoverflow.com/questions/2349991/python-how-to-import-other-python-files
http://stackoverflow.com/questions/9542738/python-find-in-list

@todo sorted() para ordenar os vetores!
"""
import d519
import math # math.floor() para baixo round() para cima
import sys
#sys.setrecursionlimit(100000)

# PARAMETROS
#Numero de gerações
g = 100
#Tamanho da população
N = 100
# Probabilidade crossover
crossover = 90
# Probabilidade mutacao
mutacao = 5

W=1500 # Best ~ V = 1020
M=[8, 19, 38, 66, 15, 62, 19, 95, 74, 55, 7, 41, 65, 65, 61, 29, 82, 45, 27, 7, 97, 79, 91, 14, 93, 41, 61, 55, 80, 74, 27, 66, 72, 49, 33, 47, 55, 61, 40, 16, 60, 29, 68, 9, 21, 88, 74, 10, 32, 96, 45, 98, 39, 42, 9, 40, 48, 2, 56, 36, 7, 50, 52, 59, 98, 64, 52, 87, 54, 23, 64, 84, 18, 64, 92, 56, 40, 31, 47, 36, 80, 61, 27, 61, 35, 55, 34, 39, 46, 82, 42, 81, 35, 10, 54, 24, 84, 2, 11, 49]
V=[27, 48, 99, 54, 42, 43, 38, 96, 49, 81, 85, 63, 89, 46, 73, 3, 9, 3, 89, 89, 20, 32, 1, 92, 88, 71, 76, 47, 7, 32, 22, 66, 32, 26, 1, 94, 6, 58, 67, 37, 58, 94, 79, 1, 17, 1, 65, 61, 92, 57, 67, 60, 78, 23, 93, 58, 52, 82, 50, 24, 49, 42, 54, 21, 83, 70, 1, 53, 7, 5, 3, 26, 60, 98, 21, 71, 19, 36, 74, 50, 16, 97, 15, 24, 8, 78, 9, 67, 22, 41, 17, 11, 87, 25, 87, 89, 69, 4, 7, 27]
# Total itens
n = len(M)

# Fronteiras com o primeiro front
F = [[]]

"""
Form a complex number.

Keyword arguments:
real -- the real part (default 0.0)
imag -- the imaginary part (default 0.0)
"""
class Cromossomo:
    alelos = [0]
    penalidade = 0
    rank = 0
    distance = -1
    S = [] # Conjunto de soluções dominadas por este cromossomo (solução)
    n = 0
    
    # Inicia o cromossomo aleatório
    def __init__(self,n,novo=False):
        self.alelos = self.alelos * n
        
        if novo:
            return
            
        # Gerando posições de alelos aleatórias
        for i in range(0,n):
            pos = d519.randrange(0,100)
            if pos > 50:
                self.alelos[i] = 1
        # Verifica se respeita o knapsack
        while self.calculaPeso() > W:
            # Retira um item aleatorio
            r = d519.randrange(0,n)
            self.alelos[r] = 0

    def calculaRho(self):
        rho = 0
        for i in range(0,n):
            # calculo rho
            if V[i]/float(M[i]) > rho:
                rho = V[i]/float(M[i])
        return rho
                
    def calculaPeso(self):
        peso = 0
        for i in range(0,len(self.alelos)):
            if self.alelos[i] == 1:
                peso = peso + M[i]
        return peso
    
    def calculaValor(self):
        valor = 0
        for i in range(0,len(self.alelos)):
            if self.alelos[i] == 1:
                valor = valor + V[i]
        return valor

    def calculaFitness(self):
        fitness = 0
        fitness = self.calculaValor() - self.penalidade
        
        return fitness

    # @deprecated
    def calculaPenalidade(self):
        # Calcula a penalidade do problema e armazena (se houver)
        if self.calculaPeso() < W:
            self.penalidade = 0
            return

        totalPesoCrom = self.calculaPeso()
        rho = self.calculaRho()
        self.penalidade = rho * (totalPesoCrom - W)

def geraFilhos(populacao):
    # Verifico se vai entrar no crossover
    r = d519.randrange(0,100)
    if r < crossover:
        print 'Entrou crossover'
        # Entrou no crossover, seleciono nova população a partir de torneio binário para seleção de pais
        # Devem ser 'm' tamanho da população de pais
        # O torneio selecionará dois cromossomos aleatórios e aquele que tiver maior fitness será o escolhido
        torneio = []
        vencedorAnterior = -1 # para não deixar que dois pais sejam o mesmo pai
        j = 0
        while j < N:
            pai1Pos = d519.randrange(0,N)
            pai2Pos = d519.randrange(0,N)
            # Nao deixo escolher o mesmo pai
            while pai1Pos == pai2Pos:
                pai2Pos = d519.randrange(0,N)
                
            # Verifico primeiro pelo rank. Se forem iguais, pela distância
            if populacao[pai1Pos].rank < populacao[pai2Pos].rank:
                if pai1Pos == vencedorAnterior:
                    continue
                torneio.append(pai1Pos)
                vencedorAnterior = pai1Pos
            elif populacao[pai2Pos].rank < populacao[pai1Pos].rank:
                if pai2Pos == vencedorAnterior:
                    continue
                torneio.append(pai2Pos)
                vencedorAnterior = pai2Pos
            else:
                if populacao[pai1Pos].distance > populacao[pai2Pos].distance:
                    if pai1Pos == vencedorAnterior:
                        continue
                    torneio.append(pai1Pos)
                    vencedorAnterior = pai1Pos
                else:
                    if pai2Pos == vencedorAnterior:
                        continue
                    torneio.append(pai2Pos)
                    vencedorAnterior = pai2Pos
            """
            if populacao[pai1Pos].calculaFitness() > populacao[pai2Pos].calculaFitness():
                if pai1Pos == vencedorAnterior: # Nao deixo o mesmo pai 2x seguidas
                    continue
                torneio.append(pai1Pos)
                vencedorAnterior = pai1Pos
            else:
                if pai2Pos == vencedorAnterior: # Nao deixo o mesmo pai 2x seguidas
                    continue
                torneio.append(pai2Pos)
                vencedorAnterior = pai2Pos
            """
            
            
            j = j+1
        print 'torneio: '
        print torneio
        # Crio vetor de nova populacao
        novaPop = []
        
        # Pais prontos em torneio, cruzamento de dois em dois
        j = 0
        while j < N:
            # Antes de trabalhar com o ponto de corte, verifico se existe um pai acima de j (caso em que tamPop é ímpar)
            if len(torneio) % 2 == 1 and j == N-1:
                novaPop.append(populacao[j])
                break # Sai do while, o pai sozinho pode sofrer no máximo mutação

            # Gero dois filhos
            filho1 = Cromossomo(n, True)
            filho2 = Cromossomo(n, True)
            
           
            # Seleciono um ponto de cruzamento entre [0-n] (total alelos/itens)
            pontoCorte = d519.randrange(0,(n)*2+1) # m+1 para englobar m
            
            ate = int(round(pontoCorte/float(2)))
            
            #Gerando primeira metade de filho1 e filho2
            for k in range(0,ate):
                filho1.alelos[k] = populacao[torneio[j]].alelos[k]
                filho2.alelos[k] = populacao[torneio[j+1]].alelos[k]
            #Gerando segunda metade de filho1 e filho2
            for k in range(ate,n):
                filho1.alelos[k] = populacao[torneio[j+1]].alelos[k]
                filho2.alelos[k] = populacao[torneio[j]].alelos[k]
            
            # Adiciono os filhos gerados na nova população
            novaPop.append(filho1)
            novaPop.append(filho2)
            j = j+2
            
        # Inicio mutação
        r = d519.randrange(0,100)
        if r < mutacao:
            print 'Entrou mutação'
            # Para cada indivíduo de novaPop, seleciono um bit aleatório e inverto o valor
            for j in range(0,N):
                bit = d519.randrange(0,n)
                if novaPop[j].alelos[bit] == 1:
                    novaPop[j].alelos[bit] = 0
                else:
                    novaPop[j].alelos[bit] = 1
        # Fim mutação
        # Calcula penalidade dos filhos
        #for j in range(0,N):
            #novaPop[j].calculaPenalidade()

        # Atualiza população
        populacao = novaPop
        
    # Retorna a população
    return populacao
    
def domina(um,dois):
    """
    Verifica se 'um' domina 'dois' e retorna em bool
    """
    # Calcula f1 e f2
    solucoesUm = [um.calculaValor(),um.calculaPeso()]
    solucoesDois = [dois.calculaValor(),dois.calculaPeso()]
    
    # Verifico se dois é dominado por um
    if solucoesUm[0] > solucoesDois[0] and solucoesUm[1] < solucoesDois[1]:
        return True
    return False
    
    
def fastNonDominatedSort(R):
    global F
    
    # Para cada solução de R, avalio se todas as outras soluções a dominam ou não
    for i in range(0,len(R)):
        R[i].S = []
        R[i].n = 0
        for j in range(0,len(R)):
            # Se é a mesma solução, nada a fazer
            if i == j:
                continue
            # Se solução i domina j
            if domina(R[i], R[j]):
                R[i].S.append(R[j])
            elif domina(R[j], R[i]):
                R[i].n = R[i].n + 1
                
        if R[i].n == 0:
            R[i].rank = 0 # 1
            F[0].append(R[i])
            
    i = 0 # i =1
    while len(F[i]) != 0: #while True F[i]
        Q = []
        for j in range(0,len(F[i])):
            for k in range(0,len(F[i][j].S)):
                F[i][j].S[k].n = F[i][j].S[k].n - 1
                if F[i][j].S[k].n == 0:
                    F[i][j].S[k].rank = i+1
                    Q.append( F[i][j].S[k])
        i = i+1
        
        # Verifica se existe F[i]. Se não, cria
        if len(F) == i:
            F.append([])
        
        F[i] = Q
    #print F
       
"""
def quicksort(v, objetivo):
    if len(v) <= 1:
        return v # uma lista vazia ou com 1 elemento ja esta ordenada
    less, equal, greater = [], [], [] # cria as sublistas dos maiores, menores e iguais ao pivo
    pivot = v[0] # escolhe o pivo. neste caso, o primeiro elemento da lista
    for x in v:
        # adiciona o elemento x a lista correspondeste
        if objetivo == 0: # Valor
            if x.calculaValor() < pivot.calculaValor():
                less.append(x)
            elif x.calculaValor() == pivot.calculaValor():
                equal.append(x)
            else:
                greater.append(x)
        elif objetivo == 1: # Peso
            if x.calculaPeso() < pivot.calculaPeso():
                less.append(x)
            elif x.calculaPeso() == pivot.calculaPeso():
                equal.append(x)
            else:
                greater.append(x)
    return quicksort(less, objetivo) + equal + quicksort(greater, objetivo)
    # concatena e retorna recursivamente
"""
    
def sortObj(v, objetivo):
    for j in range(1, len(v)):
        chave = v[j]
        i = j - 1
        
        if objetivo == 'valor':            
            while i >= 0 and v[i].calculaValor() > chave.calculaValor():
                v[i + 1] = v[i]
                i -= 1
            v[i + 1] = chave
        elif objetivo == 'peso':
            while i >= 0 and v[i].calculaPeso() > chave.calculaPeso():
                v[i + 1] = v[i]
                i -= 1
            v[i + 1] = chave
            
    return v

def crowdingDistanceAssignment(pop):
    l = len(pop)
    
    # Para cada i, setar distancia igual a 0
    for i in range(0,l):
        pop[i].distance = 0
    
    # para cada objetivo realizar os procedimentos
    # Estou fazendo os dois na mão mesmo
    
    # Valor
    pop = sortObj(pop, 'valor')
    pop[0].distance = float('inf')
    pop[l-1].distance = float('inf')
    fmin = pop[0].calculaValor()
    fmax = pop[l-1].calculaValor()
    for i in range(1,l-1):
        pop[i].distance = pop[i].distance + (pop[i+1].calculaValor() - pop[i-1].calculaValor()) / (fmax - fmin)
        
    # Peso
    pop = sortObj(pop, 'peso')
    pop[0].distance = float('inf')
    pop[l-1].distance = float('inf')
    fmin = pop[0].calculaPeso()
    fmax = pop[l-1].calculaPeso()
    for i in range(1,l-1):
        pop[i].distance = pop[i].distance + (pop[i+1].calculaPeso() - pop[i-1].calculaPeso()) / (fmax - fmin)
    
    return pop

def crowdedComparison(v):
    for j in range(1, len(v)):
        chave = v[j]
        i = j - 1
        # v[i].rank >= chave.rank or (v[i].rank != chave.rank or v[i].distance <= chave.distance):
        while i>= 0 and (v[i].rank > chave.rank or (v[i].rank == chave.rank or v[i].distance < chave.distance)):
        #while i>= 0 and (v[i].rank < chave.rank or (v[i].rank == chave.rank or v[i].distance > chave.distance)):
            v[i + 1] = v[i]
            i -= 1
        v[i + 1] = chave
        return v
        

def nsgaII():
    global F
    # Gera a população inicial randômica Pt
    print 'Iniciou o algoritmo'
    # Crio os cromossomos e gero populacao 0
    pais = [0]*N
    print 'Instaciou população'
    for i in range(0,N):
        pais[i] = Cromossomo(n)
        
    
    print 'Criou populacao'

    #  Gera os filhos Qt (problema irrestrito)
    filhos = geraFilhos(pais)
    
    # LOOP GERAÇÕES
    for t in range(0,g):
        print '##### GERACAO %d #####' % (t)
        # Combina os pais com filhos e se torna Rt
        R = pais + filhos
        print 'Combinou pais e filhos. Tamanho: %d' % (len(R))
        
        # Fast non-dominated sort em Rt (atualiza F)
        F =[[]]
        fastNonDominatedSort(R)
        print 'Executou fastNonDominatedSort e atualizou F'
        
        # Inicia próximos pais Pt+1
        pais = []
        i = 0 # i = 1 mas por causa do indice começa do 0
        
        # Enquanto Pt+1 + Fi for menorigual ao tamanho da população
        
        while (len(pais)+len(F[i])) <= N:
            # crowding-distance assignment(Fi)
            F[i] = crowdingDistanceAssignment(F[i])
            print 'Executou crowdingDistance'

            # Pt+1 = Pt+1 U Fi
            pais = pais + F[i]
            
            i = i+1
        
            
        # Ordenar Fi com Crowded comparison operator

        #print(len(F[i]))
        #print F[i]
        F[i] = crowdedComparison(F[i])
        
        # Adiciono poucos do seguinte front para preencher os faltantes de até N
        j = 0
        while len(pais) < N:
            pais.append(F[i][j])
            j = j+1
        # Pt+1 = Pt+1 U Fi[1:(N-|Pt+1|)]
        print 'Pais'
        # Qt+1 = nova população a partir de Pt+1
        filhos = geraFilhos(pais)
        
        t = t+1
        
    # Apresento os pais
    print pais
    for i in range(0,len(pais)):
        print 'Pai %d: Valor: %f Peso: %f' % (i, pais[i].calculaValor(), pais[i].calculaPeso())
        
    for i in range(0,len(F)):
        print 'F%d size: %d' % (i,len(F[i]))
        print 'F%dV = [ ' % (i),
        for j in range(0,len(F[i])):
            print '%d, ' % (F[i][j].calculaValor()),
        print ' ]'
        
        print 'F%dW = [ ' % (i),
        for j in range(0,len(F[i])):
            print '%d, ' % (F[i][j].calculaPeso()),
        print ' ]',
        print ' '
nsgaII()