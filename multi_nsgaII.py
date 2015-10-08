# -*- coding: utf-8 -*-
"""
INESC
Non-Dominated Sorting Genetic Algorithm II
Problema: Otimização mono-objetivo para maximização de IC com limite de custo
Entrada: Equipamentos do Segmento
Saida: Melhor solução de troca

Assinatura
python nsgaII.py GERACOES POPULACAO CROSSOVER MUTACAO CORTES POPINICIAL

@author Victor Torres

https://pythonhosted.org/ete2/tutorial/tutorial_trees.html
http://stackoverflow.com/questions/2349991/python-how-to-import-other-python-files
http://stackoverflow.com/questions/9542738/python-find-in-list

@todo Ao gerar pais e filhos, calcular o valor e peso e já deixar armazenado
@todo Elitismo (pressão seletiva e o Sempre Deixar o Melhor da passada se > Melhor desta)
"""
import copy
import sys
from random import randrange
#sys.setrecursionlimit(100000)

# PARAMETROS
# Cluster
cluster= False

if cluster:
    #Numero de gerações
    g = int(sys.argv[1])
    #Tamanho da população
    N = int(sys.argv[2])
    # Probabilidade crossover
    crossover = int(sys.argv[3])
    # Probabilidade mutacao
    mutacao = int(sys.argv[4])
    # Quantidade de cortes crossver
    cortes = int(sys.argv[5])
    # Pop inicial (até x%)
    initAte = int(sys.argv[6])
    # Busca Local após mutação
    buscaLocal = int(sys.argv[7])
else:
    #Numero de gerações
    g = 1000
    #Tamanho da população
    N = 300
    # Probabilidade crossover
    crossover = 90
    # Probabilidade mutacao
    mutacao = 5
    # Quantidade de cortes crossver
    cortes = 2
    # Pop inicial (até x%)
    initAte = 10
    # Busca Local após nova população. Até x trocas p/ avaliação
    buscaLocal = 1

# ICs
V = [0.0, 0.0, 0.04400000000000004, 0.10450000000000004, 0.15949999999999998, 0.35750000000000004, 0.43999999999999995, 0.46199999999999997, 0.10450000000000004, 0.13749999999999996, 0.0, 0.5389999999999999, 0.616, 0.6985, 0.00990000000000002, 0.02849999999999997, 0.726, 0.8415, 0.9185, 0.0, 0.08250000000000002, 0.1925, 0.20350000000000001, 0.31899999999999995, 0.0595, 0.37949999999999995, 0.4125, 0.484, 0.07540000000000002, 0.08799999999999997, 0.5665, 0.627, 0.6599999999999999, 0.8305, 0.913, 0.0, 0.04949999999999999, 0.07699999999999996, 0.13749999999999996, 0.35750000000000004, 0.4235, 0.46199999999999997, 0.5555, 0.10999999999999999, 0.13439999999999996, 0.9223, 0.9289000000000001, 0.935, 0.9436, 0.9403, 0.909, 0.9099, 0.781, 0.8415, 0.21860000000000002, 0.22499999999999998, 0.9678, 0.9, 0.9017, 0.9057, 0.908, 0.9111, 0.9158, 0.9138, 0.9156, 0.9177, 0.9, 0.9181, 0.9297, 0.9359, 0.938, 0.9417, 0.9526, 0.9544, 0.9696, 0.9, 0.9, 0.906, 0.9446, 0.9498, 0.9001, 0.9015, 0.9024, 0.9038, 0.22550000000000003, 0.08440000000000003, 0.28049999999999997, 0.12119999999999997, 0.374, 0.4345, 0.5885, 0.649, 0.825, 0.14790000000000003, 0.7755, 0.8745, 0.0, 0.03300000000000003, 0.08250000000000002, 0.15400000000000003, 0.913, 0.16149999999999998, 0.1795, 0.3245, 0.39049999999999996, 0.4565, 0.0, 0.6214999999999999, 0.737, 0.792, 0.8745, 0.01100000000000001, 0.24080000000000001, 0.24, 0.0, 0.04949999999999999, 0.09899999999999998, 0.13749999999999996, 0.253, 0.29700000000000004, 0.363, 0.5665, 0.121, 0.13749999999999996, 0.2643, 0.2824, 0.32509999999999994, 0.0, 0.6930000000000001, 0.759, 0.8140000000000001, 0.0, 0.0605, 0.23099999999999998, 0.011600000000000055, 0.07699999999999996, 0.13749999999999996, 0.22550000000000003, 0.29700000000000004, 0.37949999999999995, 0.40700000000000003, 0.48950000000000005, 0.31899999999999995, 0.10440000000000005, 0.04039999999999999, 0.07720000000000005, 0.9376, 0.9460999999999999, 0.9509, 0.9715, 0.9209, 0.9106, 0.0, 0.05500000000000005, 0.10450000000000004, 0.14849999999999997, 0.253, 0.28600000000000003, 0.3355, 0.396, 0.5775, 0.627, 0.4125, 0.125, 0.12870000000000004, 0.15569999999999995, 0.44420000000000004, 0.6875, 0.7424999999999999, 0.836, 0.8634999999999999, 0.0, 0.09350000000000003, 0.16500000000000004, 0.21450000000000002, 0.31899999999999995, 0.374, 0.506, 0.5720000000000001, 0.6214999999999999, 0.20189999999999997, 0.23350000000000004, 0.5335, 0.6435, 0.2733, 0.27559999999999996, 0.6819999999999999, 0.7645, 0.0, 0.04400000000000004, 0.12649999999999995, 0.13749999999999996, 0.21450000000000002, 0.2915, 0.374, 0.40149999999999997, 0.495, 0.7095, 0.748, 0.45709999999999995, 0.0, 0.0, 0.02849999999999997, 0.04039999999999999, 0.5335, 0.605, 0.07540000000000002, 0.08979999999999999, 0.6655, 0.792, 0.913, 0.0, 0.02200000000000002, 0.10999999999999999, 0.16500000000000004, 0.22550000000000003, 0.31899999999999995, 0.8525, 0.9185, 0.12119999999999997, 0.1421, 0.16749999999999998, 0.9226, 0.9274, 0.9359, 0.9097999999999999, 0.911, 0.6545000000000001, 0.671, 0.8525, 0.913, 0.04949999999999999, 0.0, 0.01649999999999996, 0.2378, 0.25539999999999996, 0.09899999999999998, 0.14300000000000002, 0.27559999999999996, 0.31299999999999994, 0.24750000000000005, 0.31899999999999995, 0.363, 0.4125, 0.0, 0.016599999999999948, 0.02510000000000001, 0.9267, 0.9372, 0.9441, 0.967, 0.9045, 0.0, 0.01100000000000001, 0.10450000000000004, 0.14300000000000002, 0.25849999999999995, 0.31899999999999995, 0.385, 0.04390000000000005, 0.06299999999999994, 0.09160000000000001, 0.11560000000000004, 0.12680000000000002]
# Custo
M = [6.649294590463687, 0.6600000262260437, 0.9100000262260437, 16.70063082477171, 13.176766277561896, 1.4567244917036588, 35.92700160294864, 9.780029213543866, 0.9100000262260437, 0.6600000262260437, 5.039999961853027, 5.124980290103762, 2.903134252763179, 4.5826210065809425, 5.039999961853027, 5.039999961853027, 3.375060234277073, 3.7031472551284823, 10.810925833996153, 21.48596417965391, 19.345787513770162, 5.563273627089104, 0.9100000262260437, 0.6600000262260437, 5.039999961853027, 5.534409868911316, 13.207794939044863, 3.40753216463016, 5.039999961853027, 5.039999961853027, 4.282265636033321, 7.8510539508563815, 4.562911264871829, 3.7220220166797517, 9.097963230566355, 9.522319901323062, 3.2665514052772195, 4.829350896454708, 13.018736432406818, 0.6600000262260437, 0.6600000262260437, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 8.10961281625653, 28.6129575572412, 12.236691965552048, 4.254123512290593, 0.6600000262260437, 5.039999961853027, 5.039999961853027, 4.2658669387833505, 32.262974814426855, 5.039999961853027, 5.039999961853027, 9.687679436551523, 15.221070813182394, 10.225780159346876, 7.832646065734676, 10.554715923765325, 5.565297118111572, 10.399967707155621, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 16.65846729537903, 3.8437458774731788, 11.813269047654467, 17.074448256963514, 4.282265636033321, 0.7074500274658203, 4.829350896454708, 3.9844009028084986, 3.830700324522244, 22.068053837720306, 3.8437458774731788, 0.9100000262260437, 0.6600000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 15.240595423544292, 5.039999961853027, 2.546820098876953, 5.039999961853027, 32.77431946974667, 4.406677949422884, 2.8614513632092566, 2.8439208279560555, 0.9100000262260437, 5.039999961853027, 6.2616970170889985, 5.14253916178766, 9.548070970056578, 7.6877319399303525, 15.977900714391494, 5.722916759698477, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 2.6669309420868523, 2.4750706371298876, 10.691155027954606, 0.9100000262260437, 4.703354171783081, 4.529887178926321, 19.044978760331404, 4.709720962954336, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 3.7220220166797517, 5.189047070812201, 7.38194407081214, 4.358712738248258, 4.529887178926321, 7.5513354753224995, 18.489206899612444, 16.34605733734253, 0.9100000262260437, 0.6600000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 1.334815229692249, 4.496623177867587, 3.9134154452071526, 4.303248628028378, 5.113250627020199, 0.6600000262260437, 5.039999961853027, 5.356104093174741, 4.163753777126986, 5.388491284106509, 14.487585812934558, 9.546840359352064, 9.270000448091421, 10.978209008062725, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.494524048805062, 4.328759511777898, 5.663491216467286, 4.328759511777898, 0.9100000262260437, 5.039999961853027, 13.04914223215601, 0.721460368414264, 4.051665382253297, 5.55059617786645, 6.327631303515693, 6.632853523503058, 31.282167288097554, 4.496623177867587, 10.406929293500726, 10.130132561563048, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 4.911556770999392, 9.923401837518323, 1.1667576614553692, 22.197941559132655, 4.328759511777898, 10.16203884278529, 1.4429150695423887, 2.7798400139676525, 0.8489400329589845, 4.677744515332277, 0.6600000262260437, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 20.508410215310054, 20.43158124595764, 5.039999961853027, 5.039999961853027, 5.079858977087948, 23.77046341461735, 10.273589385217289, 4.911570804279356, 3.7461460345497763, 18.48071784471744, 0.7619477304635802, 5.024395136738836, 9.101825621005613, 0.42447001647949223, 4.329325430779514, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.150321155269107, 13.354506404167624, 5.039999961853027, 5.039999961853027, 4.862403048960143, 4.1901134044435455, 31.592030745562166, 4.0836420997461245, 19.602449727409056, 5.801090225219727, 4.163753777126986, 3.001455730121641, 12.831516285444028, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 4.606589309017523, 23.043910854671616, 16.301063403329465, 5.039999961853027, 5.039999961853027, 3.60730184207132, 1.0300627872452097, 22.92972961198795, 4.634745466040215, 9.82407536141784, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 15.39213217800844, 4.358712738248258, 5.039999961853027, 5.039999961853027, 9.241320741777773, 12.343701122691156, 14.487585812934558, 9.260506394454394, 5.039999961853027, 5.039999961853027, 5.039999961853027, 3.7461460345497763, 2.06012274084735, 6.220594079816656, 3.830700324522244, 0.6600000262260437, 5.250411365644541, 6.218188451785943, 12.42801522767963, 9.494998184716678, 12.876482152897166, 9.966428953370313, 16.48542507911194, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027]

"""
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
 """ 
# Total itens
n = len(M)

# Fronteiras com o primeiro front
F = [[]]

R = [] #populacao pais + filhos

# Arquivo de nao dominados
A = []

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
        for i in range(0,int(n*initAte/float(100))): # até x% da solução inicial
            self.alelos[randrange(0,n)] = True
                
        # Calcula valor e peso para armazenar
        self.calculaValor()
        self.calculaPeso()

                
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
        self.valor = valor #- self.calculaFitness()

#tem erro aqui (28/01). Gerando filhos com mesmo id de pais
def geraFilhos(populacao):
    # Crio vetor de nova populacao
    novaPop = []
    
    # Verifico se vai entrar no crossover
    r = randrange(0,100)
    if r < crossover:
        if not cluster:
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
            """
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
            """
            cortesV = [0]*cortes
            alpha = 1
            inicio = 0
            for i in range(0,cortes):
                cortesV[i] = randrange(inicio+1, n-cortes+alpha)
                alpha = alpha+1
                inicio = cortesV[i]
            
            atual = 0
            tmp = 0
            for i in range(0,cortes):
                # Alternando entre os pais
                if tmp % 2 == 0:
                    pai1 = j
                    pai2 = j+1
                else:
                    pai1 = j+1
                    pai2 = j

                for k in range(atual,cortesV[i]):
                    filho1.alelos[k] = populacao[torneio[pai1]].alelos[k]
                    filho2.alelos[k] = populacao[torneio[pai2]].alelos[k]
                    
                atual = cortesV[i]
                tmp = tmp + 1
            # Ultima parte
            for k in range(atual, n):
                filho1.alelos[k] = populacao[torneio[pai2]].alelos[k]
                filho2.alelos[k] = populacao[torneio[pai1]].alelos[k] # Inverte pais
                
            # Calcula valor e peso para filho1 e filho2
            filho1.calculaValor()
            filho1.calculaPeso()
            filho2.calculaValor()
            filho2.calculaPeso()
            
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
        # Se não entrou no crossover, novaPop é populacao
        if len(novaPop) == 0:
            novaPop = copy.copy(populacao)
            
        # Para cada indivíduo de novaPop, seleciono um bit aleatório e inverto o valor
        for j in range(0,N):
            bit = randrange(0,n)
            if novaPop[j].alelos[bit]:
                novaPop[j].alelos[bit] = False
                novaPop[j].valor = novaPop[j].valor - V[bit]
                novaPop[j].peso = novaPop[j].peso - M[bit]
            else:
                novaPop[j].alelos[bit] = True
                novaPop[j].valor = novaPop[j].valor + V[bit]
                novaPop[j].peso = novaPop[j].peso + M[bit]
                
        # Fim mutação
        # Calcula penalidade dos filhos
        #for j in range(0,N):
            #novaPop[j].calculaPenalidade()

    # Atualiza população, se não entrou nem crossover nem mutação, é a mesma coisa
    if len(novaPop) != 0:
        populacao = novaPop
        
    # Retorna a população
    return copy.deepcopy(populacao)
    
def domina(um,dois):
    """
    Verifica se 'um' domina 'dois' e retorna em bool
    """
    # Calcula f1 e f2
    solucoesUm = [um.valor,um.peso]
    solucoesDois = [dois.valor,dois.peso]
    
    # Verifico se dois é dominado por um
    if solucoesUm[0] > solucoesDois[0] and solucoesUm[1] < solucoesDois[1]:
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
    global R
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
    if not cluster:
        print fmin,fmax,(fmax - fmin),l
    
    if fmin != fmax:
        for i in range(1,l-1):
            R[pop[i]].distance = R[pop[i]].distance + (R[pop[i+1]].valor - R[pop[i-1]].valor) / float(fmax - fmin)
        
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
            
            if (R[v[i]].rank > R[v[j]].rank) or (R[v[i]].rank == R[v[j]].rank and R[v[i]].distance < R[v[j]].distance):
                # trocam
                tmp = v[i]
                v[i] = v[j]
                v[j] = tmp
    return v
        

def nsgaII():
    global F
    global R
    # Gera a população inicial randômica Pt
    if not cluster:
        print 'Iniciou o algoritmo'
    # Crio os cromossomos e gero populacao 0
    pais = [0]*N
    if not cluster:    
        print 'Instaciou população'
    for i in range(0,N):
        pais[i] = Cromossomo(n)
        
    
    if not cluster:
        print 'Criou populacao'

    #  Gera os filhos Qt (problema irrestrito)
    filhos = geraFilhos(pais)
    
    # LOOP GERAÇÕES
    for t in range(0,g):
        print '##### GERACAO %d #####' % (t)
        # Combina os pais com filhos e se torna Rt
        R = pais + filhos
        
        if not cluster:
            for i in range(0,len(R)):
                print 'R[%d].valor = %f R[%d].peso = %f' % (i, R[i].valor, i, R[i].peso)
       
            print 'Combinou pais e filhos. Tamanho: %d' % (len(R))
        # Fast non-dominated sort em Rt (atualiza F)
        F =[[]]
        fastNonDominatedSort()
        
        if not cluster:
            print 'Executou fastNonDominatedSort e atualizou F'
        c = 0
        for i in range(0,len(F)):
            c = c + len(F[i])
        if not cluster:
            print 'Tamanho de todas as fronteiras de F: %d' % (c)

        # Inicia próximos pais Pt+1
        pais = []
        i = 0 # i = 1 mas por causa do indice começa do 0
        
        # Enquanto Pt+1 + Fi for menorigual ao tamanho da população
        print 'Tamanho len(pais) + len(F[%d]) = %d' % (i,len(pais)+len(F[i]))
        while (len(pais)+len(F[i])) <= N:
            # crowding-distance assignment(Fi)
            if not cluster:
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
        
        if t == g-1:
            break
        # Qt+1 = nova população a partir de Pt+1
        filhos = geraFilhos(pais)
        
        # Busca local (diversidade)
        if buscaLocal > 0:
            # Para cada individuo da populacao, executo n buscas locais aleatórias
            for j in range(0,N):
                # altera ate buscaLocal posicoes aleatórias
                tmp = copy.copy(filhos[j].alelos)
                tmpValues = [copy.copy(filhos[j].valor), copy.copy(filhos[j].peso)]
                for k in range(0,buscaLocal):
                    pos = randrange(0,n)
                    if filhos[j].alelos[pos]:
                        filhos[j].alelos[pos] = False
                        filhos[j].valor = filhos[j].valor - V[pos]
                        filhos[j].peso = filhos[j].peso - M[pos]
                    else:
                        filhos[j].alelos[pos] = True
                        filhos[j].valor = filhos[j].valor + V[pos]
                        filhos[j].peso = filhos[j].peso + M[pos]
                # Verifico NÃO se melhorou em pelo menos 2 objetivos
                if (filhos[j].valor < tmpValues[0] and filhos[j].peso > tmpValues[1]):
                    # Volta
                    filhos[j].alelos = tmp
                    filhos[j].valor= tmpValues[0]
                    filhos[j].peso = tmpValues[1]
        
        #t = t+1
        
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
    
    print 'ic = [ ',
    """
    for j in range(0,len(F[0])):
        print '%.20f, ' % (R[F[0][j]].calculaValor()),
    """
    for j in range(0,len(pais)):
        print '%.20f, ' % (pais[j].valor),
    
    print ' ]'
    
    print 'preco = [ ',
    """
    for j in range(0,len(F[0])):
        print '%.20f, ' % (R[F[0][j]].calculaPeso()),
    """
    for j in range(0,len(pais)):
        print '%.20f, ' % (pais[j].peso),
    
    print ' ]'
    
    
nsgaII()