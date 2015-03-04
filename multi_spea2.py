# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 14:32:14 2014

@author: torres
@todo Melhorar o operador de truncamento
        Este deve desempatar até o último caso de números iguais [1,2,3,4] != [1,2,3,5] != [1,2,3,6]
"""
import d519
import math # math.floor() para baixo round() para cima
#import sys
#sys.setrecursionlimit(100000)

# PARAMETROS
#Numero de gerações
g = 100
#Tamanho da população
N = 50
# Probabilidade crossover
crossover = 90
# Probabilidade mutacao
mutacao = 5
# Tamanho Arquivo
tamArq = 50

W=500
M=[57, 72, 51, 96, 82, 61, 65, 66, 53, 82, 61, 70, 54, 83, 66, 89, 83, 66, 52, 52, 54, 85, 62, 72, 87, 89, 68, 50, 71, 57, 73, 85, 58, 77, 75, 99, 71, 55, 84, 59, 82, 97, 99, 53, 73, 62, 93, 63, 89, 59, 84, 54, 93, 71, 78, 55, 69, 67, 57, 91, 82, 60, 78, 64, 54, 86, 66, 73, 56, 71, 87, 58, 53, 95, 92, 94, 53, 78, 72, 82, 74, 68, 55, 74, 82, 59, 68, 66, 64, 93, 76, 92, 88, 76, 54, 97, 78, 82, 60, 63, 84, 95, 58, 89, 77, 96, 89, 76, 77, 54, 79, 70, 98, 53, 76, 94, 79, 83, 63, 71, 99, 77, 64, 98, 52, 87, 50, 80, 51, 67, 56, 62, 62, 52, 51, 84, 89, 79, 52, 53, 57, 74, 92, 79, 84, 95, 55, 87, 76, 69, 90, 71, 79, 50, 68, 57, 96, 73, 63, 96, 80, 93, 72, 80, 88, 71, 73, 77, 99, 56, 76, 87, 58, 56, 52, 94, 83, 63, 68, 89, 60, 90, 78, 51, 68, 57, 79, 73, 57, 56, 83, 57, 57, 75, 77, 60, 70, 87, 87, 99, 54, 88, 80, 86, 74, 96, 84, 87, 82, 80, 82, 52, 99, 62, 77, 50, 52, 58, 90, 80, 80, 64, 82, 61, 70, 54, 82, 66, 70, 82, 90, 62, 69, 75, 69, 78, 50, 71, 81, 71, 95, 58, 69, 96, 51, 78, 70, 75, 87, 95, 87, 81, 67, 66, 72, 98, 73, 60, 97, 97, 70, 97, 54, 56, 69, 73, 85, 90, 89, 80, 93, 79, 63, 67, 99, 73, 74, 93, 94, 53, 65, 79, 65, 56, 78, 94, 60, 86, 64, 65, 75, 67, 85, 56, 99, 87, 92, 78, 74, 58, 55, 94, 89, 98, 84, 71, 53, 80, 52, 52, 51, 70, 57, 56, 84, 98, 60, 57, 89, 63, 51, 54, 77, 96, 92, 62, 64, 62, 75, 90, 71, 88, 55, 66, 72, 66, 71, 60, 93, 80, 96, 63, 92, 86, 60, 77, 57, 65, 67, 86, 78, 59, 65, 98, 81, 66, 90, 61, 94, 84, 52, 55, 66, 60, 65, 79, 76, 88, 95, 66, 65, 92, 62, 75, 99, 63, 92, 97, 97, 72, 90, 87, 64, 87, 68, 86, 72, 66, 82, 90, 76, 68, 55, 56, 83, 50, 83, 90, 67, 83, 56, 83, 87, 55, 73, 90, 53, 94, 54, 50, 62, 75, 98, 77, 96, 81, 78, 95, 52, 69, 94, 51, 53, 72, 72, 78, 68, 60, 97, 67, 77, 60, 88, 85, 73, 85, 65, 88, 56, 51, 73, 66, 75, 83, 91, 60, 56, 99, 81, 53, 50, 72, 94, 61, 54, 67, 63, 65, 73, 50, 85, 73, 70, 86, 59, 61, 57, 52, 66, 70, 90, 96, 53, 95, 50, 94, 73, 58, 71, 74, 90, 90, 61, 98, 93, 84, 69, 83, 62, 83, 77, 99, 52, 74, 86, 50, 85, 51, 55, 58]
V=[164, 835, 881, 190, 440, 785, 685, 80, 630, 192, 649, 220, 538, 625, 722, 43, 587, 863, 183, 907, 616, 278, 485, 997, 208, 513, 951, 512, 699, 241, 772, 460, 79, 247, 527, 942, 993, 520, 566, 837, 749, 133, 835, 175, 751, 644, 331, 287, 903, 268, 758, 790, 345, 915, 287, 432, 38, 630, 347, 628, 915, 266, 652, 785, 240, 713, 946, 634, 253, 323, 949, 47, 685, 981, 493, 634, 418, 856, 866, 693, 159, 830, 501, 104, 59, 377, 732, 336, 666, 298, 673, 822, 36, 734, 68, 245, 629, 688, 723, 83, 363, 77, 103, 188, 700, 286, 33, 355, 716, 59, 427, 308, 735, 698, 266, 998, 259, 686, 865, 798, 16, 868, 551, 912, 97, 54, 614, 794, 714, 772, 316, 461, 387, 609, 41, 655, 936, 38, 998, 976, 41, 607, 930, 726, 593, 82, 654, 631, 36, 323, 120, 843, 823, 932, 240, 172, 15, 333, 559, 801, 753, 457, 408, 986, 46, 259, 620, 642, 782, 15, 955, 179, 230, 407, 660, 904, 532, 204, 485, 473, 219, 672, 888, 586, 492, 888, 500, 846, 489, 730, 539, 977, 559, 135, 46, 322, 417, 357, 237, 646, 95, 891, 17, 6, 785, 832, 850, 574, 512, 2, 854, 698, 79, 35, 395, 924, 108, 323, 666, 86, 168, 427, 847, 166, 218, 421, 655, 929, 885, 281, 535, 805, 839, 509, 899, 783, 237, 515, 634, 724, 201, 354, 891, 108, 526, 181, 957, 582, 397, 364, 558, 900, 679, 530, 53, 718, 906, 909, 963, 909, 957, 404, 996, 119, 968, 633, 21, 36, 52, 266, 466, 121, 82, 918, 538, 269, 625, 21, 858, 905, 41, 437, 358, 550, 294, 960, 417, 807, 24, 631, 80, 8, 170, 112, 801, 421, 856, 504, 203, 507, 361, 782, 378, 250, 617, 500, 663, 171, 267, 721, 288, 317, 344, 560, 693, 401, 188, 155, 423, 921, 341, 215, 439, 309, 320, 832, 770, 544, 138, 47, 480, 49, 464, 21, 133, 778, 133, 917, 105, 581, 234, 652, 942, 599, 355, 195, 206, 57, 186, 896, 543, 83, 259, 951, 84, 602, 696, 51, 788, 82, 256, 816, 210, 627, 618, 634, 49, 691, 305, 812, 952, 900, 635, 229, 835, 685, 828, 372, 666, 531, 958, 980, 744, 146, 446, 937, 918, 426, 359, 808, 237, 518, 376, 47, 971, 851, 447, 545, 211, 965, 230, 859, 83, 892, 247, 957, 779, 816, 144, 464, 182, 957, 964, 364, 919, 824, 352, 870, 410, 396, 547, 799, 737, 532, 506, 813, 57, 317, 871, 734, 947, 301, 738, 222, 587, 351, 534, 614, 922, 693, 885, 312, 344, 178, 294, 382, 322, 173, 577, 280, 127, 502, 359, 879, 543, 385, 276, 55, 494, 186, 100, 886, 497, 335, 521, 891, 622, 95, 617, 360, 413, 903, 72, 6, 331, 746, 684, 354, 325, 642, 191, 871, 327, 148, 503, 264, 424, 864, 946, 558, 657, 357, 727, 228, 339, 440, 819, 978, 129, 814]
# Total itens
n = len(M)

#Populacao
P = []
# Arquivo
Pa = [[]]*tamArq
# Conjunto não dominado
A = []

class Cromossomo:
    alelos = [0]
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
        for i in range(0,n):
            pos = d519.randrange(0,100)
            if pos > 50:
                self.alelos[i] = 1

                
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
    

def calculaFitness():
    global P
    global Pa
    # fitnessPopulation
    fP = P + Pa
    print 'Tamanho fp: %d P: %d Pa: %d' % (len(fP), len(P), len(Pa))
    # Como o arquivo inicial é vazio, retiro as posições vazias pois não servem para nada (lista vazia)
    for i in range(0,len(fP)):
        if not fP[i]:
            del fP[i:len(fP)]
            break
    
    # Calculando S(i)
    for i in range(0,len(fP)):
        for j in range(0,len(fP)):
            if i == j:
                continue
            # Verifico se i domkina j
            if fP[i].calculaValor() > fP[j].calculaValor() and fP[i].calculaPeso() < fP[j].calculaPeso():
                fP[i].S = fP[i].S + 1
                
    # Calculando R(i)
    for i in range(0,len(fP)):
        totalDominadores = 0
        for j in range(0,len(fP)):
            if i == j:
                continue
            # Verifico se i é dominado por j
            if fP[j].calculaValor() > fP[i].calculaValor() and fP[j].calculaPeso() < fP[i].calculaPeso():
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
            lista.append(math.sqrt(pow(fP[j].calculaValor() - fP[i].calculaValor(), 2) + pow(fP[j].calculaPeso() - fP[i].calculaPeso(), 2)))
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
    P = [0]*N
    print 'Instaciou população'
    for i in range(0,N):
        P[i] = Cromossomo(n)
        
    
    print 'Criou populacao'
    
    # Gera arquivo vazio
    

    # LOOP GERAÇÕES
    for t in range(0,g):
        print 'Iniciou geração %d' % (t)
        # Calcula fitness de Pt e Pat
        calculaFitness()
        print 'Calculou fitness de P+Pa'
            
        # Copiar todos os invidíduos não dominados em P[t] e Pa[t] para P[t+1]
        nPa = [] # novo arquivo, i.e, Pa[t+1]
        tabu = [] # lista de indices de PPa aos quais entraram em nPa
        PPa = P + Pa
        for i in range(0,len(PPa)):
            if PPa[i].F < 1:
                nPa.append(PPa[i])
                tabu.append(i)
       
        print 'Terminou de criar o arquivo. Tamanho: %d' % (len(nPa))
        # Verifica se o tamanho da proxima populacao é maior que o tamanho do arquivo
        if len(nPa) > tamArq:
            # Calculo a distância de cada cromossomo do arquivo um em relação a todos vizinhos
            for i in range(0,len(PPa)):
                # Reseto as distancias, se existirem
                PPa[i].Dv = []
                # Somente quem entrou em tabu
                if i not in tabu:
                    PPa[i].Dv.append(float('inf')) # Assim nunca será o primeiro a escolher
                    continue
                # Calculo da distancia para todos os vizinhos
                for j in range(0,len(PPa)):
                    if i == j:
                        continue
                    PPa[i].Dv.append(math.sqrt(pow(PPa[i].calculaValor() - PPa[j].calculaValor(),2) + pow(PPa[i].calculaPeso() - PPa[j].calculaPeso(),2)))
                
                # Ordeno do menor para o maior
                PPa[i].Dv.sort()
                
            # Reduzir por meio de um operador de truncamento
            i = 0
            while len(nPa) > tamArq:
                # Se 0 e 1 são exatamente iguais, escolho qualquer um
                if i == tamArq -2:
                    menorPos = 0
                    break
                print 'Tamanho de nPa é maior que tamArq. i = %d' % (i)
                menorPos = -1
                
                # Buscando quem tem menor
                PPa.sort(key=lambda x: min(x.Dv))
                
                #Verifico se tem iguais
                PPa[0].Dv.sort()
                PPa[1].Dv.sort()
                if PPa[0].Dv[i] == PPa[1].Dv[i]:
                    print '--------'
                    #print PPa[0].Dv
                    #print PPa[1].Dv
                    i = i +1
                    continue
                elif PPa[0].Dv[i] < PPa[1].Dv[i]:
                    menorPos = 0
                else:
                    menorPos = 1
                    
                # Retiro quem é menor
                for i in range(0,len(nPa)):
                    if PPa[menorPos].alelos == nPa[i].alelos:
                        # Retira
                        nPa.pop(i)
                        PPa.pop(menorPos)
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
            
        # Se critério de parada, então pegar os não dominados de P[t+1] e montar o pareto resposta
        if t == g-2: # Quer dizer que a última rodada seria inicializada
            A = nPa
            break # sai das gerações
        
        # Atualizo o arquivo definitivamente
        Pa = nPa
        
        # Torneio binario de Pa[t+1]
        torneio = []
        vencedorAnterior = -1 # para não deixar que dois pais sejam o mesmo pai
        j = 0
        while j < tamArq:
            pai1Pos = d519.randrange(0,tamArq)
            pai2Pos = d519.randrange(0,tamArq)
            # Nao deixo escolher o mesmo pai
            while pai1Pos == pai2Pos:
                pai2Pos = d519.randrange(0,tamArq)
                
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
            pontoCorte = d519.randrange(0,(n)*2+1) # m+1 para englobar m
            
            ate = int(round(pontoCorte/float(2)))
            
            #Gerando primeira metade de filho1 e filho2
            for k in range(0,ate):
                filho1.alelos[k] = Pa[torneio[j]].alelos[k]
                filho2.alelos[k] = Pa[torneio[j+1]].alelos[k]
            #Gerando segunda metade de filho1 e filho2
            for k in range(ate,n):
                filho1.alelos[k] = Pa[torneio[j+1]].alelos[k]
                filho2.alelos[k] = Pa[torneio[j]].alelos[k]
            
            # Adiciono os filhos gerados na nova população
            P.append(filho1)
            P.append(filho2)
            j = j+2
            
        # Inicio mutação
        r = d519.randrange(0,100)
        if r < mutacao:
            print 'Entrou mutação'
            # Para cada indivíduo de novaPop, seleciono um bit aleatório e inverto o valor
            for j in range(0,N):
                bit = d519.randrange(0,n)
                if P[j].alelos[bit] == 1:
                    P[j].alelos[bit] = 0
                else:
                    P[j].alelos[bit] = 1
        # Fim mutação
        
        # Proxima iteração
        
    # Retorna o conjunto de vetores-decisão representados pelos indivíduos não dominados de P[t+1]
    A2 = []
    for i in range(0,len(A)):
        dominado = False
        for j in range(0,len(A)):
            if i == j:
                continue
            if A[i].calculaValor() <= A[j].calculaValor() and A[i].calculaPeso() >= A[j].calculaPeso():
                dominado = True
        if not dominado:
            A2.append(A[i])

    # Solução pareto final
    print 'F0dV = [ ',
    for i in range(0,len(A2)):
        print '%d, ' % (A2[i].calculaValor()),
    print ' ]'
        
        
    print 'F0dW = [ ',
    for i in range(0,len(A2)):
        print '%d, ' % (A2[i].calculaPeso()),
    print ' ]',
        
    

spea2()