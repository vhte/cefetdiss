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

W=500
M=[57, 72, 51, 96, 82, 61, 65, 66, 53, 82, 61, 70, 54, 83, 66, 89, 83, 66, 52, 52, 54, 85, 62, 72, 87, 89, 68, 50, 71, 57, 73, 85, 58, 77, 75, 99, 71, 55, 84, 59, 82, 97, 99, 53, 73, 62, 93, 63, 89, 59, 84, 54, 93, 71, 78, 55, 69, 67, 57, 91, 82, 60, 78, 64, 54, 86, 66, 73, 56, 71, 87, 58, 53, 95, 92, 94, 53, 78, 72, 82, 74, 68, 55, 74, 82, 59, 68, 66, 64, 93, 76, 92, 88, 76, 54, 97, 78, 82, 60, 63, 84, 95, 58, 89, 77, 96, 89, 76, 77, 54, 79, 70, 98, 53, 76, 94, 79, 83, 63, 71, 99, 77, 64, 98, 52, 87, 50, 80, 51, 67, 56, 62, 62, 52, 51, 84, 89, 79, 52, 53, 57, 74, 92, 79, 84, 95, 55, 87, 76, 69, 90, 71, 79, 50, 68, 57, 96, 73, 63, 96, 80, 93, 72, 80, 88, 71, 73, 77, 99, 56, 76, 87, 58, 56, 52, 94, 83, 63, 68, 89, 60, 90, 78, 51, 68, 57, 79, 73, 57, 56, 83, 57, 57, 75, 77, 60, 70, 87, 87, 99, 54, 88, 80, 86, 74, 96, 84, 87, 82, 80, 82, 52, 99, 62, 77, 50, 52, 58, 90, 80, 80, 64, 82, 61, 70, 54, 82, 66, 70, 82, 90, 62, 69, 75, 69, 78, 50, 71, 81, 71, 95, 58, 69, 96, 51, 78, 70, 75, 87, 95, 87, 81, 67, 66, 72, 98, 73, 60, 97, 97, 70, 97, 54, 56, 69, 73, 85, 90, 89, 80, 93, 79, 63, 67, 99, 73, 74, 93, 94, 53, 65, 79, 65, 56, 78, 94, 60, 86, 64, 65, 75, 67, 85, 56, 99, 87, 92, 78, 74, 58, 55, 94, 89, 98, 84, 71, 53, 80, 52, 52, 51, 70, 57, 56, 84, 98, 60, 57, 89, 63, 51, 54, 77, 96, 92, 62, 64, 62, 75, 90, 71, 88, 55, 66, 72, 66, 71, 60, 93, 80, 96, 63, 92, 86, 60, 77, 57, 65, 67, 86, 78, 59, 65, 98, 81, 66, 90, 61, 94, 84, 52, 55, 66, 60, 65, 79, 76, 88, 95, 66, 65, 92, 62, 75, 99, 63, 92, 97, 97, 72, 90, 87, 64, 87, 68, 86, 72, 66, 82, 90, 76, 68, 55, 56, 83, 50, 83, 90, 67, 83, 56, 83, 87, 55, 73, 90, 53, 94, 54, 50, 62, 75, 98, 77, 96, 81, 78, 95, 52, 69, 94, 51, 53, 72, 72, 78, 68, 60, 97, 67, 77, 60, 88, 85, 73, 85, 65, 88, 56, 51, 73, 66, 75, 83, 91, 60, 56, 99, 81, 53, 50, 72, 94, 61, 54, 67, 63, 65, 73, 50, 85, 73, 70, 86, 59, 61, 57, 52, 66, 70, 90, 96, 53, 95, 50, 94, 73, 58, 71, 74, 90, 90, 61, 98, 93, 84, 69, 83, 62, 83, 77, 99, 52, 74, 86, 50, 85, 51, 55, 58]
V=[164, 835, 881, 190, 440, 785, 685, 80, 630, 192, 649, 220, 538, 625, 722, 43, 587, 863, 183, 907, 616, 278, 485, 997, 208, 513, 951, 512, 699, 241, 772, 460, 79, 247, 527, 942, 993, 520, 566, 837, 749, 133, 835, 175, 751, 644, 331, 287, 903, 268, 758, 790, 345, 915, 287, 432, 38, 630, 347, 628, 915, 266, 652, 785, 240, 713, 946, 634, 253, 323, 949, 47, 685, 981, 493, 634, 418, 856, 866, 693, 159, 830, 501, 104, 59, 377, 732, 336, 666, 298, 673, 822, 36, 734, 68, 245, 629, 688, 723, 83, 363, 77, 103, 188, 700, 286, 33, 355, 716, 59, 427, 308, 735, 698, 266, 998, 259, 686, 865, 798, 16, 868, 551, 912, 97, 54, 614, 794, 714, 772, 316, 461, 387, 609, 41, 655, 936, 38, 998, 976, 41, 607, 930, 726, 593, 82, 654, 631, 36, 323, 120, 843, 823, 932, 240, 172, 15, 333, 559, 801, 753, 457, 408, 986, 46, 259, 620, 642, 782, 15, 955, 179, 230, 407, 660, 904, 532, 204, 485, 473, 219, 672, 888, 586, 492, 888, 500, 846, 489, 730, 539, 977, 559, 135, 46, 322, 417, 357, 237, 646, 95, 891, 17, 6, 785, 832, 850, 574, 512, 2, 854, 698, 79, 35, 395, 924, 108, 323, 666, 86, 168, 427, 847, 166, 218, 421, 655, 929, 885, 281, 535, 805, 839, 509, 899, 783, 237, 515, 634, 724, 201, 354, 891, 108, 526, 181, 957, 582, 397, 364, 558, 900, 679, 530, 53, 718, 906, 909, 963, 909, 957, 404, 996, 119, 968, 633, 21, 36, 52, 266, 466, 121, 82, 918, 538, 269, 625, 21, 858, 905, 41, 437, 358, 550, 294, 960, 417, 807, 24, 631, 80, 8, 170, 112, 801, 421, 856, 504, 203, 507, 361, 782, 378, 250, 617, 500, 663, 171, 267, 721, 288, 317, 344, 560, 693, 401, 188, 155, 423, 921, 341, 215, 439, 309, 320, 832, 770, 544, 138, 47, 480, 49, 464, 21, 133, 778, 133, 917, 105, 581, 234, 652, 942, 599, 355, 195, 206, 57, 186, 896, 543, 83, 259, 951, 84, 602, 696, 51, 788, 82, 256, 816, 210, 627, 618, 634, 49, 691, 305, 812, 952, 900, 635, 229, 835, 685, 828, 372, 666, 531, 958, 980, 744, 146, 446, 937, 918, 426, 359, 808, 237, 518, 376, 47, 971, 851, 447, 545, 211, 965, 230, 859, 83, 892, 247, 957, 779, 816, 144, 464, 182, 957, 964, 364, 919, 824, 352, 870, 410, 396, 547, 799, 737, 532, 506, 813, 57, 317, 871, 734, 947, 301, 738, 222, 587, 351, 534, 614, 922, 693, 885, 312, 344, 178, 294, 382, 322, 173, 577, 280, 127, 502, 359, 879, 543, 385, 276, 55, 494, 186, 100, 886, 497, 335, 521, 891, 622, 95, 617, 360, 413, 903, 72, 6, 331, 746, 684, 354, 325, 642, 191, 871, 327, 148, 503, 264, 424, 864, 946, 558, 657, 357, 727, 228, 339, 440, 819, 978, 129, 814]
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
        for i in range(0,int(n*0.01)): # até 10% da solução inicial
            self.alelos[d519.randrange(0,n)] = True

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
            print 'len(F[i]): %d' % (len(F[i])) # TA VINDO 0 AQUI!!!!!
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