# -*- coding: utf-8 -*-
"""
INESC - SPEA2

Assinatura
python spea2.py GERACOES POPULACAO CROSSOVER MUTACAO CORTES POPINICIAL BUSCALOCAL

@author: torres
@todo Melhorar o operador de truncamento
        Este deve desempatar até o último caso de números iguais [1,2,3,4] != [1,2,3,5] != [1,2,3,6]
"""
from random import randrange
import math # math.floor() para baixo round() para cima
import sys
import copy
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

# Tamanho Arquivo
tamArq = N

# Limite custo
W =float('inf')#11000
# ICs
V = [0.0, 0.0, 0.04400000000000004, 0.10450000000000004, 0.15949999999999998, 0.35750000000000004, 0.43999999999999995, 0.46199999999999997, 0.10450000000000004, 0.13749999999999996, 0.0, 0.5389999999999999, 0.616, 0.6985, 0.00990000000000002, 0.02849999999999997, 0.726, 0.8415, 0.9185, 0.0, 0.08250000000000002, 0.1925, 0.20350000000000001, 0.31899999999999995, 0.0595, 0.37949999999999995, 0.4125, 0.484, 0.07540000000000002, 0.08799999999999997, 0.5665, 0.627, 0.6599999999999999, 0.8305, 0.913, 0.0, 0.04949999999999999, 0.07699999999999996, 0.13749999999999996, 0.35750000000000004, 0.4235, 0.46199999999999997, 0.5555, 0.10999999999999999, 0.13439999999999996, 0.9223, 0.9289000000000001, 0.935, 0.9436, 0.9403, 0.909, 0.9099, 0.781, 0.8415, 0.21860000000000002, 0.22499999999999998, 0.9678, 0.9, 0.9017, 0.9057, 0.908, 0.9111, 0.9158, 0.9138, 0.9156, 0.9177, 0.9, 0.9181, 0.9297, 0.9359, 0.938, 0.9417, 0.9526, 0.9544, 0.9696, 0.9, 0.9, 0.906, 0.9446, 0.9498, 0.9001, 0.9015, 0.9024, 0.9038, 0.22550000000000003, 0.08440000000000003, 0.28049999999999997, 0.12119999999999997, 0.374, 0.4345, 0.5885, 0.649, 0.825, 0.14790000000000003, 0.7755, 0.8745, 0.0, 0.03300000000000003, 0.08250000000000002, 0.15400000000000003, 0.913, 0.16149999999999998, 0.1795, 0.3245, 0.39049999999999996, 0.4565, 0.0, 0.6214999999999999, 0.737, 0.792, 0.8745, 0.01100000000000001, 0.24080000000000001, 0.24, 0.0, 0.04949999999999999, 0.09899999999999998, 0.13749999999999996, 0.253, 0.29700000000000004, 0.363, 0.5665, 0.121, 0.13749999999999996, 0.2643, 0.2824, 0.32509999999999994, 0.0, 0.6930000000000001, 0.759, 0.8140000000000001, 0.0, 0.0605, 0.23099999999999998, 0.011600000000000055, 0.07699999999999996, 0.13749999999999996, 0.22550000000000003, 0.29700000000000004, 0.37949999999999995, 0.40700000000000003, 0.48950000000000005, 0.31899999999999995, 0.10440000000000005, 0.04039999999999999, 0.07720000000000005, 0.9376, 0.9460999999999999, 0.9509, 0.9715, 0.9209, 0.9106, 0.0, 0.05500000000000005, 0.10450000000000004, 0.14849999999999997, 0.253, 0.28600000000000003, 0.3355, 0.396, 0.5775, 0.627, 0.4125, 0.125, 0.12870000000000004, 0.15569999999999995, 0.44420000000000004, 0.6875, 0.7424999999999999, 0.836, 0.8634999999999999, 0.0, 0.09350000000000003, 0.16500000000000004, 0.21450000000000002, 0.31899999999999995, 0.374, 0.506, 0.5720000000000001, 0.6214999999999999, 0.20189999999999997, 0.23350000000000004, 0.5335, 0.6435, 0.2733, 0.27559999999999996, 0.6819999999999999, 0.7645, 0.0, 0.04400000000000004, 0.12649999999999995, 0.13749999999999996, 0.21450000000000002, 0.2915, 0.374, 0.40149999999999997, 0.495, 0.7095, 0.748, 0.45709999999999995, 0.0, 0.0, 0.02849999999999997, 0.04039999999999999, 0.5335, 0.605, 0.07540000000000002, 0.08979999999999999, 0.6655, 0.792, 0.913, 0.0, 0.02200000000000002, 0.10999999999999999, 0.16500000000000004, 0.22550000000000003, 0.31899999999999995, 0.8525, 0.9185, 0.12119999999999997, 0.1421, 0.16749999999999998, 0.9226, 0.9274, 0.9359, 0.9097999999999999, 0.911, 0.6545000000000001, 0.671, 0.8525, 0.913, 0.04949999999999999, 0.0, 0.01649999999999996, 0.2378, 0.25539999999999996, 0.09899999999999998, 0.14300000000000002, 0.27559999999999996, 0.31299999999999994, 0.24750000000000005, 0.31899999999999995, 0.363, 0.4125, 0.0, 0.016599999999999948, 0.02510000000000001, 0.9267, 0.9372, 0.9441, 0.967, 0.9045, 0.0, 0.01100000000000001, 0.10450000000000004, 0.14300000000000002, 0.25849999999999995, 0.31899999999999995, 0.385, 0.04390000000000005, 0.06299999999999994, 0.09160000000000001, 0.11560000000000004, 0.12680000000000002]
# Custo
M = [6.649294590463687, 0.6600000262260437, 0.9100000262260437, 16.70063082477171, 13.176766277561896, 1.4567244917036588, 35.92700160294864, 9.780029213543866, 0.9100000262260437, 0.6600000262260437, 5.039999961853027, 5.124980290103762, 2.903134252763179, 4.5826210065809425, 5.039999961853027, 5.039999961853027, 3.375060234277073, 3.7031472551284823, 10.810925833996153, 21.48596417965391, 19.345787513770162, 5.563273627089104, 0.9100000262260437, 0.6600000262260437, 5.039999961853027, 5.534409868911316, 13.207794939044863, 3.40753216463016, 5.039999961853027, 5.039999961853027, 4.282265636033321, 7.8510539508563815, 4.562911264871829, 3.7220220166797517, 9.097963230566355, 9.522319901323062, 3.2665514052772195, 4.829350896454708, 13.018736432406818, 0.6600000262260437, 0.6600000262260437, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 8.10961281625653, 28.6129575572412, 12.236691965552048, 4.254123512290593, 0.6600000262260437, 5.039999961853027, 5.039999961853027, 4.2658669387833505, 32.262974814426855, 5.039999961853027, 5.039999961853027, 9.687679436551523, 15.221070813182394, 10.225780159346876, 7.832646065734676, 10.554715923765325, 5.565297118111572, 10.399967707155621, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 16.65846729537903, 3.8437458774731788, 11.813269047654467, 17.074448256963514, 4.282265636033321, 0.7074500274658203, 4.829350896454708, 3.9844009028084986, 3.830700324522244, 22.068053837720306, 3.8437458774731788, 0.9100000262260437, 0.6600000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 15.240595423544292, 5.039999961853027, 2.546820098876953, 5.039999961853027, 32.77431946974667, 4.406677949422884, 2.8614513632092566, 2.8439208279560555, 0.9100000262260437, 5.039999961853027, 6.2616970170889985, 5.14253916178766, 9.548070970056578, 7.6877319399303525, 15.977900714391494, 5.722916759698477, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 2.6669309420868523, 2.4750706371298876, 10.691155027954606, 0.9100000262260437, 4.703354171783081, 4.529887178926321, 19.044978760331404, 4.709720962954336, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 3.7220220166797517, 5.189047070812201, 7.38194407081214, 4.358712738248258, 4.529887178926321, 7.5513354753224995, 18.489206899612444, 16.34605733734253, 0.9100000262260437, 0.6600000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 1.334815229692249, 4.496623177867587, 3.9134154452071526, 4.303248628028378, 5.113250627020199, 0.6600000262260437, 5.039999961853027, 5.356104093174741, 4.163753777126986, 5.388491284106509, 14.487585812934558, 9.546840359352064, 9.270000448091421, 10.978209008062725, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.494524048805062, 4.328759511777898, 5.663491216467286, 4.328759511777898, 0.9100000262260437, 5.039999961853027, 13.04914223215601, 0.721460368414264, 4.051665382253297, 5.55059617786645, 6.327631303515693, 6.632853523503058, 31.282167288097554, 4.496623177867587, 10.406929293500726, 10.130132561563048, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 4.911556770999392, 9.923401837518323, 1.1667576614553692, 22.197941559132655, 4.328759511777898, 10.16203884278529, 1.4429150695423887, 2.7798400139676525, 0.8489400329589845, 4.677744515332277, 0.6600000262260437, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 20.508410215310054, 20.43158124595764, 5.039999961853027, 5.039999961853027, 5.079858977087948, 23.77046341461735, 10.273589385217289, 4.911570804279356, 3.7461460345497763, 18.48071784471744, 0.7619477304635802, 5.024395136738836, 9.101825621005613, 0.42447001647949223, 4.329325430779514, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.150321155269107, 13.354506404167624, 5.039999961853027, 5.039999961853027, 4.862403048960143, 4.1901134044435455, 31.592030745562166, 4.0836420997461245, 19.602449727409056, 5.801090225219727, 4.163753777126986, 3.001455730121641, 12.831516285444028, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 5.039999961853027, 4.606589309017523, 23.043910854671616, 16.301063403329465, 5.039999961853027, 5.039999961853027, 3.60730184207132, 1.0300627872452097, 22.92972961198795, 4.634745466040215, 9.82407536141784, 0.6600000262260437, 0.9100000262260437, 5.039999961853027, 5.039999961853027, 15.39213217800844, 4.358712738248258, 5.039999961853027, 5.039999961853027, 9.241320741777773, 12.343701122691156, 14.487585812934558, 9.260506394454394, 5.039999961853027, 5.039999961853027, 5.039999961853027, 3.7461460345497763, 2.06012274084735, 6.220594079816656, 3.830700324522244, 0.6600000262260437, 5.250411365644541, 6.218188451785943, 12.42801522767963, 9.494998184716678, 12.876482152897166, 9.966428953370313, 16.48542507911194, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027, 5.039999961853027]

# Total itens
n = len(M)

#Populacao
P = []
# Arquivo
Pa = []

class Cromossomo:
    alelos = [False]
    valor = 0 # ic
    peso = 0 # custo
    S = 0 # Strength value, representing the number of solutions it dominates
    R = 0
    F = 0 # Fitness
    Dv = [] # Distancia vizinhos
    
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
        
    

def calculaFitness():
    global P
    global Pa
    # fitnessPopulation
    fP = P + Pa
    if not cluster:
        print 'Tamanho fp: %d P: %d Pa: %d' % (len(fP), len(P), len(Pa))

    # Calculando S(i)
    for i in range(0,len(fP)):
        for j in range(0,len(fP)):
            if i == j:
                continue
            # Verifico se i domina j
            if fP[i].valor > fP[j].valor and fP[i].peso < fP[j].peso:
                fP[i].S = fP[i].S + 1
                
    # Calculando R(i)
    for i in range(0,len(fP)):
        totalDominadores = 0
        for j in range(0,len(fP)):
            if i == j:
                continue
            # Verifico se i é dominado por j
            if fP[j].valor > fP[i].valor and fP[j].peso < fP[i].peso:
                totalDominadores = totalDominadores + fP[j].S
        fP[i].R = totalDominadores
        
    # Calculando D(i)
    k = int(round(math.sqrt(len(fP))))
    
    # d(u,v): sqrt((x2 - x1)^2 + (y2-y1)^2)
    for i in range(0,len(fP)):
        lista = []
        for j in range(0,len(fP)):
            if i == j:
                continue
            lista.append(math.sqrt(pow(fP[j].valor - fP[i].valor, 2) + pow(fP[j].peso - fP[i].peso, 2)))
        lista.sort() # ordena de forma ascendente
        fP[i].D = 1/float(lista[k]+2)
        
    # Finalmente, F(i)
    for i in range(0,len(fP)):
        fP[i].F = fP[i].R + fP[i].D
        
    # Separo fP novamente em P e Pa
    novoP = []
    novoPa = []
    for i in range(0,len(fP)):
        if i < len(P):
            novoP.append(fP[i])
        else:
            novoPa.append(fP[i])
            
    P = novoP
    Pa = novoPa
def spea2():
    global P
    global Pa
    
    # Gera a população inicial randômica P0
    print 'Iniciou o algoritmo'
    # Crio os cromossomos e gero populacao 0
    print 'Instaciou população'
    for i in range(0,N):
        P.append(Cromossomo(n))
        
    
    print 'Criou populacao'
    
    # Gera arquivo vazio
    

    # LOOP GERAÇÕES
    for t in range(0,g):
        print 'Iniciou geração %d' % (t)
        # Calcula fitness de Pt e Pat
        calculaFitness()
        #print 'Calculou fitness de P+Pa'
            
        # Copiar todos os invidíduos não dominados em P[t] e Pa[t] para P[t+1]
        nPa = [] # novo arquivo, i.e, Pa[t+1]
        tabu = [] # lista de indices de PPa aos quais entraram em nPa
        PPa = P + Pa
        for i in range(0,len(PPa)):
            if PPa[i].F < 1:
                nPa.append(PPa[i])
                tabu.append(id(PPa[i]))
       
        print 'Terminou de criar o arquivo. Tamanho: %d' % (len(nPa))
        # Verifica se o tamanho da proxima populacao é maior que o tamanho do arquivo
        if len(nPa) > tamArq:
            # Calculo a distância de cada cromossomo do arquivo um em relação a todos vizinhos
            for i in range(0,len(PPa)):
                # Reseto as distancias, se existirem
                PPa[i].Dv = []
                # Somente quem entrou em tabu
                if id(PPa[i]) not in tabu:
                    PPa[i].Dv.append(float('inf')) # Assim nunca será o primeiro a escolher
                    continue
                # Calculo da distancia para todos os vizinhos
                for j in range(0,len(PPa)):
                    if i == j:
                        continue
                    PPa[i].Dv.append(math.sqrt(pow(PPa[i].valor - PPa[j].valor,2) + pow(PPa[i].peso - PPa[j].peso,2)))
                
                # Ordeno do menor para o maior
                PPa[i].Dv.sort()
                
            # Reduzir por meio de um operador de truncamento
            
            while len(nPa) > tamArq:
                i = 0
                """
                # Se 0 e 1 são exatamente iguais, escolho qualquer um
                if i == tamArq -2:
                    menorPos = 0
                    break
                """
                #print 'Tamanho de nPa é maior que tamArq: %d' % (len(nPa))
                
                
                # Buscando quem tem menor
                PPa.sort(key=lambda x: min(x.Dv))

                # por default é o primeiro                
                menorPos = id(PPa[0])
                
                #Verifico se tem iguais
                PPa[0].Dv.sort()
                PPa[1].Dv.sort()
                while PPa[0].Dv[i] == PPa[1].Dv[i]:
                    i = i+1
                    if i == len(PPa[0].Dv)-1:
                        break # sao iguais, deixa o 0 mesmo para ser retirado
                
                if PPa[0].Dv[i] < PPa[1].Dv[i]:
                    menorPos = id(PPa[0])
                    PPa.pop(0)
                else:
                    menorPos = id(PPa[1])
                    PPa.pop(1)
                    
                # Retiro quem é menor
                for i in range(0,len(nPa)):
                    if id(nPa[i]) == menorPos:
                        # Retira
                        nPa.pop(i)
                        break # for
                
            
        # Senao se o tamanho for menor
        elif len(nPa) < tamArq:
            # Copio PPa para uma variável auxiliar
            tmp = PPa
            # Ordeno por F
            """
             On large lists you will get better performance using operator.attrgetter('count') as your key. This is just an optimized (lower level) form of the lambda function in this answer. –  David Eyk Dec 31 '08 at 19:35 
            """
            tmp.sort(key=lambda x: x.F, reverse=False)
            # Preencher com os inviduos dominados em P e Pa
            i = 0
            while len(nPa) != tamArq:
                if tmp[i].F < 1:
                    i = i+1
                    continue
                # Incluo uma solucao dominada com F>=1
                nPa.append(tmp[i])
                i = i+1
        
        # Atualizo o arquivo definitivamente
        Pa = nPa
        
        # Se é a última geração, sair pois ja tenho só os nao-dominados
        if t == g-1:
            PPa = Pa
            break
        
        # Torneio binario de Pa[t+1]
        torneio = []
        vencedorAnterior = -1 # para não deixar que dois pais sejam o mesmo pai
        j = 0
        while j < tamArq:
            pai1Pos = randrange(0,tamArq)
            pai2Pos = randrange(0,tamArq)
            # Nao deixo escolher o mesmo pai
            while pai1Pos == pai2Pos:
                pai2Pos = randrange(0,tamArq)
                
            # Ganha quem tem Fitness menor
            if Pa[pai1Pos].F < Pa[pai2Pos]:
                if pai1Pos == vencedorAnterior:
                    continue
                torneio.append(pai1Pos)
                vencedorAnterior = pai1Pos
            else:
                if pai2Pos == vencedorAnterior:
                    continue
                torneio.append(pai2Pos)
                vencedorAnterior = pai2Pos
                
            j = j + 1
        
        #Aplica operadores crossover e mutação
        # Substituo o vetor de nova populacao
        P = []
        
        # Pais prontos em torneio, cruzamento de dois em dois
        j = 0
        while j < tamArq:
            # Antes de trabalhar com o ponto de corte, verifico se existe um pai acima de j (caso em que tamPop é ímpar)
            if len(torneio) % 2 == 1 and j == tamArq-1:
                P.append(Pa[j])
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
                filho1.alelos[k] = Pa[torneio[j]].alelos[k]
                filho2.alelos[k] = Pa[torneio[j+1]].alelos[k]
            #Gerando segunda metade de filho1 e filho2
            for k in range(ate,n):
                filho1.alelos[k] = Pa[torneio[j+1]].alelos[k]
                filho2.alelos[k] = Pa[torneio[j]].alelos[k]
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
                    filho1.alelos[k] = Pa[torneio[pai1]].alelos[k]
                    filho2.alelos[k] = Pa[torneio[pai2]].alelos[k]
                    
                atual = cortesV[i]
                tmp = tmp + 1
            # Ultima parte
            for k in range(atual, n):
                filho1.alelos[k] = Pa[torneio[pai2]].alelos[k]
                filho2.alelos[k] = Pa[torneio[pai1]].alelos[k] # Inverte pais
                
            # Calculo valor e peso dos novos filhos
            filho1.calculaValor()
            filho1.calculaPeso()
            filho2.calculaValor()
            filho2.calculaPeso()
            
            # Adiciono os filhos gerados na nova população
            P.append(filho1)
            P.append(filho2)
            j = j+2
            
        # Inicio mutação
        r = randrange(0,100)
        if r < mutacao:
            #print 'Entrou mutação'
            # Para cada indivíduo de novaPop, seleciono um bit aleatório e inverto o valor
            for j in range(0,N):
                bit = randrange(0,n)
                if P[j].alelos[bit]:
                    P[j].alelos[bit] = False
                    P[j].valor = P[j].valor - V[bit]
                    P[j].peso = P[j].peso - M[bit]
                else:
                    P[j].alelos[bit] = True
                    P[j].valor = P[j].valor + V[bit]
                    P[j].peso = P[j].peso + M[bit]
        
        # Busca local (diversidade)
        if buscaLocal > 0:
            # Para cada individuo da populacao, executo n buscas locais aleatórias
            for j in range(0,N):
                # altera ate buscaLocal posicoes aleatórias
                tmp = copy.copy(P[j].alelos)
                tmpValues = [copy.copy(P[j].valor), copy.copy(P[j].peso)]
                for k in range(0,buscaLocal):
                    pos = randrange(0,n)
                    if P[j].alelos[pos]:
                        P[j].alelos[pos] = False
                        P[j].valor = P[j].valor - V[pos]
                        P[j].peso = P[j].peso - M[pos]
                    else:
                        P[j].alelos[pos] = True
                        P[j].valor = P[j].valor + V[pos]
                        P[j].peso = P[j].peso + M[pos]
                # Verifico NÃO se melhorou em pelo menos 2 objetivos
                if (P[j].valor < tmpValues[0] and P[j].peso > tmpValues[1]):
                    # Volta
                    P[j].alelos = tmp
                    P[j].valor= tmpValues[0]
                    P[j].peso = tmpValues[1]
                
            

        # Proxima iteração
        """
        # Fim iteracao, atualizacao de arquivo            
        for i in range(0,len(nPa)):
            existe = False
            # Adiciono o que dominou somente se nao existir alguem com mesmo valor e peso igual a ele
            for j in range(0,len(A)):
                if (nPa[i].valor == A[j].valor and nPa[i].peso == A[j].peso) or (nPa[i].peso <= 0 or nPa[i].valor <= 0):
                    existe = True
                    break
            if existe:
                continue
            A.append(nPa[i])
        """
    # Retorna o conjunto de vetores-decisão representados pelos indivíduos não dominados de P[t+1]
    print 'Iniciando calculo de nao-dominados de A pode demorar um pouco...'
    
    """
    A2 = []
    for i in range(0,len(PPa)):
        dominado = False
        for j in range(0,len(PPa)):
            if i == j:
                continue
            if (PPa[i].valor < PPa[j].valor and PPa[i].peso < PPa[j].peso) and PPa[i].preco > PPa[j].preco or (PPa[i].valor <= 0):
                dominado = True
                break
        if not dominado:
            A2.append(PPa[i])
    """
    A2 = PPa
    
    # Solução pareto final
    print 'ic = [ ',
    for i in range(0,len(A2)):
        print '%.20f, ' % (A2[i].valor),
    print ' ]'
        
        
    print 'custo = [ ',
    for i in range(0,len(A2)):
        print '%.20f, ' % (A2[i].peso),
    print ' ]'
    

spea2()