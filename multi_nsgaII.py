# -*- coding: utf-8 -*-
"""
INESC
Non-Dominated Sorting Genetic Algorithm II
Problema: Otimização mono-objetivo para maximização de IC com limite de custo
Entrada: Equipamentos do Segmento
Saida: Melhor solução de troca

@author Victor Torres

https://pythonhosted.org/ete2/tutorial/tutorial_trees.html
http://stackoverflow.com/questions/2349991/python-how-to-import-other-python-files
http://stackoverflow.com/questions/9542738/python-find-in-list

@todo Ao gerar pais e filhos, calcular o valor e peso e já deixar armazenado
@todo Elitismo (pressão seletiva e o Sempre Deixar o Melhor da passada se > Melhor desta)
"""
import copy
from random import randrange
import mysql.connector

cnx = mysql.connector.connect(user='root', password='root', database='cemig_d519')
cursor = cnx.cursor()
#sys.setrecursionlimit(100000)

# PARAMETROS
#Numero de gerações
g = 500
#Tamanho da população
N = 500
# Probabilidade crossover
crossover = 90
# Probabilidade mutacao
mutacao = 5
# Pressão seletiva (número de pais a entrar no torneio)
pS = 2
# Tamanho do arquivo
tamArq = N

# Problema Knapsack a ser resolvido
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
for i in range(0,len(M)):
    if M[i] > 0.1:
        del(M[i])
        del(V[i])
        break
for i in range(0,len(V)):
    if V[i] > 0.1:
        del(M[i])
        del(V[i])
        break
    
# Total itens
n = len(M)

# Fronteiras com o primeiro front
F = [[]]

R = [] #populacao pais + filhos

# Arquivo de nao dominados
A = []

# Total SAIFI
totalSAIFI = sum(M)
# Total SAIDET_X
totalSAIDET = sum(V)

"""
Form a complex number.

Keyword arguments:
real -- the real part (default 0.0)
imag -- the imaginary part (default 0.0)
"""
class Cromossomo:
    alelos = [False]
    valor = 0
    peso = 0
    preco = 0
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
        for i in range(0,int(n*0.5)): # até 50% da solução inicial
            self.alelos[randrange(0,n)] = True
            
        # Calcula os valores iniciais
        self.calculaValor()
        self.calculaPeso()
        self.calculaPreco()
                
    def calculaPeso(self):
        peso = 0
        for i in range(0,len(self.alelos)):
            if self.alelos[i]:
                peso = peso + M[i]
        self.peso = peso #- self.calculaFitness()
    
    def calculaValor(self):
        valor = 0
        for i in range(0,len(self.alelos)):
            if self.alelos[i]:
                valor = valor + V[i]

        self.valor =  valor #- self.calculaFitness()
        
    def calculaPreco(self):
        self.preco = sum(self.alelos)
        """
        preco = 0
        for i in range(0,len(self.alelos)):
            if self.alelos[i]:
                preco = preco + C[i]

        self.preco =  preco #- self.calculaFitness()
        """
    def calculaRho(self):
        rho = 0
        for i in range(0,len(self.alelos)):
            # calculo rho
            if M[i] == 0:
                continue
            if V[i]/float(M[i]) > rho:
                rho = V[i]/float(M[i])
        return rho

#tem erro aqui (28/01). Gerando filhos com mesmo id de pais
def geraFilhos(populacao):
    # Verifico se vai entrar no crossover
    r = randrange(0,100)
    if r < crossover:
        print 'Entrou crossover'
        # Entrou no crossover, seleciono nova população a partir de torneio binário para seleção de pais
        # Devem ser 'm' tamanho da população de pais
        # O torneio selecionará dois cromossomos aleatórios e aquele que tiver maior fitness será o escolhido
        torneio = []
        vencedorAnterior = -1 # para não deixar que dois pais sejam o mesmo pai
        j = 0
        while j < N:
            pai1Pos = randrange(0,N)
            pai2Pos = randrange(0,N)
            # Nao deixo escolher o mesmo pai
            while pai1Pos == pai2Pos:
                pai2Pos = randrange(0,N)
                
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
        
        
        # Crio vetor de nova populacao
        novaPop = []
        
        # Pais prontos em torneio, cruzamento de dois em dois
        j = 0
        """
        for z in range(0,len(populacao)):
            print populacao[z].alelos
        print  '---'
        """
        while j < N:
            # Antes de trabalhar com o ponto de corte, verifico se existe um pai acima de j (caso em que tamPop é ímpar)
            if len(torneio) % 2 == 1 and j == N-1:
                novaPop.append(copy.deepcopy(populacao[j]))
                break # Sai do while, o pai sozinho pode sofrer no máximo mutação

            # Gero dois filhos
            filho1 = Cromossomo(n, True)
            filho2 = Cromossomo(n, True)
            
           
            # Seleciono um ponto de cruzamento entre [0-n] (total alelos/itens)
            pontoCorte = randrange(0,(n)*2+1) # m+1 para englobar m
            
            ate = int(round(pontoCorte/float(2)))
            #Gerando primeira metade de filho1 e filho2
            for k in range(0,ate):
                filho1.alelos[k] = populacao[torneio[j]].alelos[k]
                filho2.alelos[k] = populacao[torneio[j+1]].alelos[k]
            #Gerando segunda metade de filho1 e filho2
            for k in range(ate,n):
                filho1.alelos[k] = populacao[torneio[j+1]].alelos[k]
                filho2.alelos[k] = populacao[torneio[j]].alelos[k]
                
            # Calcula valor e peso para filho1 e filho2
            filho1.calculaValor()
            filho1.calculaPeso()
            filho1.calculaPreco()
            filho2.calculaValor()
            filho2.calculaPeso()
            filho2.calculaPreco()
            
            # Adiciono os filhos gerados na nova população
            novaPop.append(filho1)
            novaPop.append(filho2)
            
            
            """
            print torneio
            print populacao[torneio[j]].alelos
            print populacao[torneio[j+1]].alelos
            print ate
            print n
            print filho1.alelos
            print filho2.alelos
            raw_input('continue...')
            """
            j = j+2
            
        # Inicio mutação
        r = randrange(0,100)
        if r < mutacao:
            print 'Entrou mutação'
            # Para cada indivíduo de novaPop, seleciono um bit aleatório e inverto o valor
            for j in range(0,N):
                bit = randrange(0,n)
                if novaPop[j].alelos[bit]:
                    novaPop[j].alelos[bit] = False
                else:
                    novaPop[j].alelos[bit] = True
                novaPop[j].calculaValor()
                novaPop[j].calculaPeso()
                novaPop[j].calculaPreco()
        # Fim mutação
        # Calcula penalidade dos filhos
        #for j in range(0,N):
            #novaPop[j].calculaPenalidade()

        # Atualiza população
        populacao = novaPop
        
    # Retorna a população
    return copy.deepcopy(populacao)
    
def domina(um,dois):
    """
    Verifica se 'um' domina 'dois' e retorna em bool
    """
    # Calcula f1 e f2
    solucoesUm = [um.valor,um.peso,um.preco]
    solucoesDois = [dois.valor,dois.peso,dois.preco]
    
    # Verifico se dois é dominado por um
    if solucoesUm[0] > solucoesDois[0] and solucoesUm[1] > solucoesDois[1] and solucoesUm[2] < solucoesDois[2]:
        return True
    return False
    
    
def fastNonDominatedSort():
    global F
    global R

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
                R[i].S.append(j)
            elif domina(R[j], R[i]):
                R[i].n = R[i].n + 1
                
        if R[i].n == 0:
            R[i].rank = 0 # 1
            F[0].append(i)

    """
    i = 0 # i =1s
    print 'F: ', 
    print F
    for i in range(0,len(R)):
        print 'R[%d].S = ' % (i),
        print R[i].S
        print 'R[%d].n = %d' % (i,R[i].n)
    """
    i=0
    while len(F[i]) != 0: #while True F[i]
        Q = []
        for j in range(0,len(F[i])):
            for k in range(0,len(R[F[i][j]].S)):
                R[R[F[i][j]].S[k]].n = R[R[F[i][j]].S[k]].n - 1
                if R[R[F[i][j]].S[k]].n == 0:
                    R[R[F[i][j]].S[k]].rank = i+1
                    Q.append(R[F[i][j]].S[k])
        i = i+1
        
        # Verifica se existe F[i]. Se não, cria
        if len(F) == i:
            F.append([])
        
        F[i] = Q
    #print F
    
    
    
def sortObj(v, objetivo):
    if objetivo == 'valor':
        return sorted(v, key=lambda pos: R[pos].valor)
    elif objetivo == 'peso':
        return sorted(v, key=lambda pos: R[pos].peso)

def crowdingDistanceAssignment(pop):
    global R
    l = len(pop)
    
    # Se houver apenas um elemento, nada a fazer, é ele
    if l == 1:
        return pop
    
    # Para cada i, setar distancia igual a 0
    for i in range(0,l):
        R[pop[i]].distance = 0
    
    # para cada objetivo realizar os procedimentos
    # Estou fazendo os dois na mão mesmo
    
    # Valor
    pop = sortObj(pop, 'valor')
    R[pop[0]].distance = float('inf')
    R[pop[l-1]].distance = float('inf')
    fmin = R[pop[0]].valor
    fmax = R[pop[l-1]].valor
    print fmin,fmax,(fmax - fmin),l
    
    if fmin != fmax:
        for i in range(1,l-1):
            R[pop[i]].distance = R[pop[i]].distance + (R[pop[i+1]].valor - R[pop[i-1]].valor) / (fmax - fmin)
        
    # Peso
    pop = sortObj(pop, 'peso')
    R[pop[0]].distance = float('inf')
    R[pop[l-1]].distance = float('inf')
    fmin = R[pop[0]].peso
    fmax = R[pop[l-1]].peso
    if fmin != fmax:
        for i in range(1,l-1):
            R[pop[i]].distance = R[pop[i]].distance + (R[pop[i+1]].peso - R[pop[i-1]].peso) / float(fmax - fmin)
    
    return pop

def crowdedComparison(v):
    global R
    for i in range(0,len(v)):
        for j in range(0,len(v)):
            if i == j:
                continue
            
            if (R[v[i]].rank < R[v[j]].rank) or (R[v[i]].rank == R[v[j]].rank and R[v[i]].distance > R[v[j]].distance):
            #if (R[v[i]].rank > R[v[j]].rank) or (R[v[i]].rank == R[v[j]].rank and R[v[i]].distance <= R[v[j]].distance):
                # trocam
                tmp = v[i]
                v[i] = v[j]
                v[j] = tmp
    return v
        

def nsgaII():
    global F
    global R
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
        
        for i in range(0,len(R)):
            print 'R[%d].valor = %f R[%d].peso = %f' % (i, R[i].valor, i, R[i].peso)
        """
        # verificando se tem um individuo duplicado
        for i in range(0,len(R)):
            for j in range(0,len(R)):
                if i == j:
                    continue
                if id(R[i]) == id(R[j]):
                    print 'id %d duplicado' % (id(R[i]))
                    raw_input('continue...')
        """
        """
        for i in range(0,len(R)):
            print R[i]
            print 'Individuo %d' % (i)
            print 'ID: %s SAIDI: %f SAIDET_X: %f' % (id(R[i]), R[i].calculaValor(), R[i].calculaPeso())
        """
        print 'Combinou pais e filhos. Tamanho: %d' % (len(R))
        # Fast non-dominated sort em Rt (atualiza F)
        F =[[]]
        fastNonDominatedSort()
        
        print 'Executou fastNonDominatedSort e atualizou F'
        c = 0
        for i in range(0,len(F)):
            c = c + len(F[i])
        print 'Tamanho de todas as fronteiras de F: %d' % (c)
        if c < len(R):
            for i in range(0,len(R)):
                print R[i]
                print 'Individuo %d' % (i)
                print 'ID: %s SAIDI: %f SAIDET_X: %f' % (id(R[i]), R[i].valor, R[i].peso)
            raw_input('|F| < |R|')
        # Inicia próximos pais Pt+1
        pais = []
        i = 0 # i = 1 mas por causa do indice começa do 0
        
        # Enquanto Pt+1 + Fi for menorigual ao tamanho da população
        while (len(pais)+len(F[i])) <= N:
            # crowding-distance assignment(Fi)
            print 'Executando crowdingDistanceAssignment. N: %d e len(pais) + len(F[%d]) = %d' % (N,i,len(pais)+len(F[i]))
            F[i] = crowdingDistanceAssignment(F[i])
            # Pt+1 = Pt+1 U Fi
            for j in range(0,len(F[i])):
                pais.append(R[F[i][j]])
            #pais = pais + F[i]
            
            i = i+1
            
        # Ordenar Fi com Crowded comparison operator

        #print(len(F[i]))
        #print F[i]
        F[i] = crowdedComparison(F[i])
        
        # Adiciono poucos do seguinte front para preencher os faltantes de até N
        j = 0
        while len(pais) < N:
            pais.append(R[F[i][j]]) # os novos pais estao convergindo....
            j = j+1
        # Pt+1 = Pt+1 U Fi[1:(N-|Pt+1|)]
        
        # Qt+1 = nova população a partir de Pt+1
        filhos = geraFilhos(pais)
        
        t = t+1
        
        """
        # Fim iteracao, atualizacao de arquivo
        for i in range(0,len(F[0])):
            existe = False
            # Adiciono o que dominou somente se nao existir alguem com mesmo valor e peso igual a ele
            for j in range(0,len(A)):
                if R[F[0][i]].alelos == A[j].alelos:
                    existe = True
                    break
            if existe:
                continue
            A.append(R[F[0][i]])
        """

        
    # Apresento o arquivo final
    print F[0] # F[0] converge :(
    """
    print 'Iniciando os cálculos dos não dominados. Isto pode demorar um pouco...'
    retirar = []
    for i in range(0,len(A)):
        for j in range(0,len(A)):
            if domina(A[i], A[j]) or A[j].valor <= 0:
                retirar.append(j)
    print set(retirar)
    # retiro os dominados
    for index in sorted(set(retirar), reverse=True):
        del A[index]
        
    for i in range(0,len(A)):
        print 'Arquivo %d (%i): Valor: %f Peso: %f' % (i, id(A[i]), A[i].valor, A[i].peso)
    """
    
    # Preenchendo A com os tamArq primeiros invididuos
    A = []
    i = 0
    j = 0
    while len(A) < tamArq:
            A.append(R[F[i][j]])
            
            if len(F[i]) == j+1:
                i = i+1
                j = 0
            else:
                j = j+1
    
    print 'saidet_x = [ ',
    """
    for j in range(0,len(F[0])):
        print '%.20f, ' % (R[F[0][j]].calculaValor()),
    """
    for j in range(0,len(A)):
        print '%.20f, ' % (A[j].valor/float(totalSAIDET)),
    
    print ' ]'
    
    print 'saifi = [ ',
    """
    for j in range(0,len(F[0])):
        print '%.20f, ' % (R[F[0][j]].calculaPeso()),
    """
    for j in range(0,len(A)):
        print '%.20f, ' % (A[j].peso/float(totalSAIFI)),
    
    print ' ]'
    
    print 'custo = [ ',
    """
    for j in range(0,len(F[0])):
        print '%.20f, ' % (R[F[0][j]].calculaPeso()),
    """
    for j in range(0,len(A)):
        print '%.20f, ' % (A[j].preco),
    
    print ' ]'
    
    
nsgaII()