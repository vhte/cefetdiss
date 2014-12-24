# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 14:32:14 2014

@author: torres
@todo Melhorar o operador de truncamento
        Este deve desempatar até o último caso de números iguais [1,2,3,4] != [1,2,3,5] != [1,2,3,6]
"""
import d519
import math # math.floor() para baixo round() para cima
import sys
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

M=[8, 19, 38, 66, 15, 62, 19, 95, 74, 55, 7, 41, 65, 65, 61, 29, 82, 45, 27, 7, 97, 79, 91, 14, 93, 41, 61, 55, 80, 74, 27, 66, 72, 49, 33, 47, 55, 61, 40, 16, 60, 29, 68, 9, 21, 88, 74, 10, 32, 96, 45, 98, 39, 42, 9, 40, 48, 2, 56, 36, 7, 50, 52, 59, 98, 64, 52, 87, 54, 23, 64, 84, 18, 64, 92, 56, 40, 31, 47, 36, 80, 61, 27, 61, 35, 55, 34, 39, 46, 82, 42, 81, 35, 10, 54, 24, 84, 2, 11, 49]
V=[27, 48, 99, 54, 42, 43, 38, 96, 49, 81, 85, 63, 89, 46, 73, 3, 9, 3, 89, 89, 20, 32, 1, 92, 88, 71, 76, 47, 7, 32, 22, 66, 32, 26, 1, 94, 6, 58, 67, 37, 58, 94, 79, 1, 17, 1, 65, 61, 92, 57, 67, 60, 78, 23, 93, 58, 52, 82, 50, 24, 49, 42, 54, 21, 83, 70, 1, 53, 7, 5, 3, 26, 60, 98, 21, 71, 19, 36, 74, 50, 16, 97, 15, 24, 8, 78, 9, 67, 22, 41, 17, 11, 87, 25, 87, 89, 69, 4, 7, 27]
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