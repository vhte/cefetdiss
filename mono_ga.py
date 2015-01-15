# -*- coding: utf-8 -*-
"""
Genetic Algorithm

Problema: Otimização mono-objetivo para maximização de IC com limite de custo
Entrada: Equipamentos do Segmento
Saida: Melhor solução de troca

Alterar:
Roleta p buscar pais
Torneio? Pg 33 Manual MH
Diversos pais provenientes do torneio
    Um ponto de corte p cada cruzamento
Função fitness: Penalidade. Se soma dos pesos do cromossomo > W, fitness -= 7*(SOMA - W)
    Ai vc terá o fitness para aquele cromossomo
@todo Melhorar a saída de um ótimo local
@todo Rever solução gulosa x aleatória
@todo elitismo pg 44 MCEM

@author Victor Torres - victorhugo@lsi.cefetmg.br

https://pythonhosted.org/ete2/tutorial/tutorial_trees.html
http://stackoverflow.com/questions/2349991/python-how-to-import-other-python-files
http://stackoverflow.com/questions/9542738/python-find-in-list
"""
import d519
import math # math.floor() para baixo round() para cima

########### PARAMETROS ###########
# Numero de geracoes
g = 500
# Tamanho populacao
m = 150
# Probabilidade crossover
crossover = 90
# Probabilidade mutacao
mutacao = 5
# Pressão seletiva
pS = 3
# Condição de parada: Qte de vezes em que o resultado é igual
v = 10
"""
# Limite knapsack
W = 269 # Best ~ V = 295
# Peso
M = [95, 4, 60, 32, 23, 72, 80, 62, 65,46]
# Valor
V = [55, 10, 47, 5, 4, 50, 8, 61, 85, 87]

W=878 # Best ~ V = 1020
M=[92,4,43,83,84,68,92,82,6,44,32,18,56,83,25,96,70,48,14,58]
V=[44,46,90,72,91,40,75,35,8,54,78,40,77,15,61,17,75,29,75,63]
"""
W=15000
M=[57, 72, 51, 96, 82, 61, 65, 66, 53, 82, 61, 70, 54, 83, 66, 89, 83, 66, 52, 52, 54, 85, 62, 72, 87, 89, 68, 50, 71, 57, 73, 85, 58, 77, 75, 99, 71, 55, 84, 59, 82, 97, 99, 53, 73, 62, 93, 63, 89, 59, 84, 54, 93, 71, 78, 55, 69, 67, 57, 91, 82, 60, 78, 64, 54, 86, 66, 73, 56, 71, 87, 58, 53, 95, 92, 94, 53, 78, 72, 82, 74, 68, 55, 74, 82, 59, 68, 66, 64, 93, 76, 92, 88, 76, 54, 97, 78, 82, 60, 63, 84, 95, 58, 89, 77, 96, 89, 76, 77, 54, 79, 70, 98, 53, 76, 94, 79, 83, 63, 71, 99, 77, 64, 98, 52, 87, 50, 80, 51, 67, 56, 62, 62, 52, 51, 84, 89, 79, 52, 53, 57, 74, 92, 79, 84, 95, 55, 87, 76, 69, 90, 71, 79, 50, 68, 57, 96, 73, 63, 96, 80, 93, 72, 80, 88, 71, 73, 77, 99, 56, 76, 87, 58, 56, 52, 94, 83, 63, 68, 89, 60, 90, 78, 51, 68, 57, 79, 73, 57, 56, 83, 57, 57, 75, 77, 60, 70, 87, 87, 99, 54, 88, 80, 86, 74, 96, 84, 87, 82, 80, 82, 52, 99, 62, 77, 50, 52, 58, 90, 80, 80, 64, 82, 61, 70, 54, 82, 66, 70, 82, 90, 62, 69, 75, 69, 78, 50, 71, 81, 71, 95, 58, 69, 96, 51, 78, 70, 75, 87, 95, 87, 81, 67, 66, 72, 98, 73, 60, 97, 97, 70, 97, 54, 56, 69, 73, 85, 90, 89, 80, 93, 79, 63, 67, 99, 73, 74, 93, 94, 53, 65, 79, 65, 56, 78, 94, 60, 86, 64, 65, 75, 67, 85, 56, 99, 87, 92, 78, 74, 58, 55, 94, 89, 98, 84, 71, 53, 80, 52, 52, 51, 70, 57, 56, 84, 98, 60, 57, 89, 63, 51, 54, 77, 96, 92, 62, 64, 62, 75, 90, 71, 88, 55, 66, 72, 66, 71, 60, 93, 80, 96, 63, 92, 86, 60, 77, 57, 65, 67, 86, 78, 59, 65, 98, 81, 66, 90, 61, 94, 84, 52, 55, 66, 60, 65, 79, 76, 88, 95, 66, 65, 92, 62, 75, 99, 63, 92, 97, 97, 72, 90, 87, 64, 87, 68, 86, 72, 66, 82, 90, 76, 68, 55, 56, 83, 50, 83, 90, 67, 83, 56, 83, 87, 55, 73, 90, 53, 94, 54, 50, 62, 75, 98, 77, 96, 81, 78, 95, 52, 69, 94, 51, 53, 72, 72, 78, 68, 60, 97, 67, 77, 60, 88, 85, 73, 85, 65, 88, 56, 51, 73, 66, 75, 83, 91, 60, 56, 99, 81, 53, 50, 72, 94, 61, 54, 67, 63, 65, 73, 50, 85, 73, 70, 86, 59, 61, 57, 52, 66, 70, 90, 96, 53, 95, 50, 94, 73, 58, 71, 74, 90, 90, 61, 98, 93, 84, 69, 83, 62, 83, 77, 99, 52, 74, 86, 50, 85, 51, 55, 58]
V=[164, 835, 881, 190, 440, 785, 685, 80, 630, 192, 649, 220, 538, 625, 722, 43, 587, 863, 183, 907, 616, 278, 485, 997, 208, 513, 951, 512, 699, 241, 772, 460, 79, 247, 527, 942, 993, 520, 566, 837, 749, 133, 835, 175, 751, 644, 331, 287, 903, 268, 758, 790, 345, 915, 287, 432, 38, 630, 347, 628, 915, 266, 652, 785, 240, 713, 946, 634, 253, 323, 949, 47, 685, 981, 493, 634, 418, 856, 866, 693, 159, 830, 501, 104, 59, 377, 732, 336, 666, 298, 673, 822, 36, 734, 68, 245, 629, 688, 723, 83, 363, 77, 103, 188, 700, 286, 33, 355, 716, 59, 427, 308, 735, 698, 266, 998, 259, 686, 865, 798, 16, 868, 551, 912, 97, 54, 614, 794, 714, 772, 316, 461, 387, 609, 41, 655, 936, 38, 998, 976, 41, 607, 930, 726, 593, 82, 654, 631, 36, 323, 120, 843, 823, 932, 240, 172, 15, 333, 559, 801, 753, 457, 408, 986, 46, 259, 620, 642, 782, 15, 955, 179, 230, 407, 660, 904, 532, 204, 485, 473, 219, 672, 888, 586, 492, 888, 500, 846, 489, 730, 539, 977, 559, 135, 46, 322, 417, 357, 237, 646, 95, 891, 17, 6, 785, 832, 850, 574, 512, 2, 854, 698, 79, 35, 395, 924, 108, 323, 666, 86, 168, 427, 847, 166, 218, 421, 655, 929, 885, 281, 535, 805, 839, 509, 899, 783, 237, 515, 634, 724, 201, 354, 891, 108, 526, 181, 957, 582, 397, 364, 558, 900, 679, 530, 53, 718, 906, 909, 963, 909, 957, 404, 996, 119, 968, 633, 21, 36, 52, 266, 466, 121, 82, 918, 538, 269, 625, 21, 858, 905, 41, 437, 358, 550, 294, 960, 417, 807, 24, 631, 80, 8, 170, 112, 801, 421, 856, 504, 203, 507, 361, 782, 378, 250, 617, 500, 663, 171, 267, 721, 288, 317, 344, 560, 693, 401, 188, 155, 423, 921, 341, 215, 439, 309, 320, 832, 770, 544, 138, 47, 480, 49, 464, 21, 133, 778, 133, 917, 105, 581, 234, 652, 942, 599, 355, 195, 206, 57, 186, 896, 543, 83, 259, 951, 84, 602, 696, 51, 788, 82, 256, 816, 210, 627, 618, 634, 49, 691, 305, 812, 952, 900, 635, 229, 835, 685, 828, 372, 666, 531, 958, 980, 744, 146, 446, 937, 918, 426, 359, 808, 237, 518, 376, 47, 971, 851, 447, 545, 211, 965, 230, 859, 83, 892, 247, 957, 779, 816, 144, 464, 182, 957, 964, 364, 919, 824, 352, 870, 410, 396, 547, 799, 737, 532, 506, 813, 57, 317, 871, 734, 947, 301, 738, 222, 587, 351, 534, 614, 922, 693, 885, 312, 344, 178, 294, 382, 322, 173, 577, 280, 127, 502, 359, 879, 543, 385, 276, 55, 494, 186, 100, 886, 497, 335, 521, 891, 622, 95, 617, 360, 413, 903, 72, 6, 331, 746, 684, 354, 325, 642, 191, 871, 327, 148, 503, 264, 424, 864, 946, 558, 657, 357, 727, 228, 339, 440, 819, 978, 129, 814]
# Total itens
n = len(M)

class Cromossomo:
    alelos = [False]
    fitness = 0
    penalidade = 0
    
    # Inicia o cromossomo aleatório
    def __init__(self,n,novo=False):
        self.alelos = self.alelos * n
        
        if novo:
            return
            
        
        # Gerando posições de alelos aleatórias
        """
        for i in range(0,n):
            if d519.randrange(0,100) > 60:
                self.alelos[i] = True
        
        """
        # Gerando posições de alelos gulosos
        for i in range(0,n):
            if V[i]/float(M[i]) > 3:
                self.alelos[i] = True
        
                
        # Verifica se respeita o knapsack
        while self.calculaPeso() > W:
            # Retira um item aleatorio
            self.alelos[d519.randrange(0,n)] = False

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
            if self.alelos[i]:
                peso = peso + M[i]
        return peso
    
    def calculaValor(self):
        valor = 0
        for i in range(0,len(self.alelos)):
            if self.alelos[i]:
                valor = valor + V[i]
        return valor

    def calculaFitness(self):
        return self.calculaValor() - self.penalidade

    def calculaPenalidade(self):
        # Calcula a penalidade do problema e armazena (se houver)
        if self.calculaPeso() < W:
            self.penalidade = 0
            return
        self.penalidade = self.calculaRho() * (self.calculaPeso() - W)
        
####################### MAIN #######################
def mono_ga(params):
    debug = params[0]
    
    melhoresGeracao = [] # a resposta do algoritmo, para cada geração uma única resposta será enviada
    avg = [0]*g
    if debug:
        print 'Iniciou o algoritmo'
    # Crio os cromossomos e gero populacao 1
    populacao = [False]*m
    if debug:
        print 'Instaciou população'
    for i in range(0,m):
        populacao[i] = Cromossomo(n)
    
    if debug:
        print 'Criou populacao'
    
    # Seto o número de vezes em que a geração deu o mesmo resultado
    #mesmoResultado = 0
    #ultimoResultado = 0
    # Inicio as gerações
    for i in range(0,g):
        if debug:
            print 'Inicio geração %d e calculou penalidade' % (i)
            """
            for j in range(0,m):
                print populacao[j].alelos
                populacao[j].calculaPenalidade()
                print populacao[j].penalidade
            """
        # Calcula penalidade da populacao
        for j in range(0,m):
            populacao[j].calculaPenalidade()
        
        # Verifico se vai entrar no crossover
        r = d519.randrange(0,100)
        if r < crossover:
            if debug:
                print 'Entrou crossover'
            # Entrou no crossover, seleciono nova população a partir de torneio binário para seleção de pais
            # Devem ser 'm' tamanho da população de pais
            # O torneio selecionará dois cromossomos aleatórios e aquele que tiver maior fitness será o escolhido
            torneio = []
            vencedorAnterior = -1 # para não deixar que dois pais sejam o mesmo pai
            j = 0
            # Pressão seletiva: 2[2-5]
            while j < m:
                candidatos = []
                for k in range(0,pS):
                    candidato = d519.randrange(0,m)
                    while candidato in candidatos or candidato == vencedorAnterior:
                        candidato = d519.randrange(0,m)
                    candidatos.append(candidato)
                    
                melhor = [0, 0] # [pos, val]
                for k in range(0,pS):
                    valorCandidato = populacao[candidatos[k]].calculaFitness()
                    if valorCandidato > melhor[1]:
                        melhor = [k, valorCandidato]
                    
                vencedorAnterior = candidatos[melhor[0]]
                torneio.append(candidatos[melhor[0]])
                """   
                pai1Pos = d519.randrange(0,m)
                pai2Pos = d519.randrange(0,m)
                # Nao deixo escolher o mesmo pai
                while pai1Pos == pai2Pos:
                    pai2Pos = d519.randrange(0,m)
                    
               
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
            if debug:
                print 'torneio: '
                print torneio
            # Crio vetor de nova populacao
            novaPop = []
            
            # Pais prontos em torneio, cruzamento de dois em dois
            j = 0
            while j < m:
                # Antes de trabalhar com o ponto de corte, verifico se existe um pai acima de j (caso em que tamPop é ímpar)
                if len(torneio) % 2 == 1 and j == m-1:
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
                if debug:
                    print '==============='
                    print 'torneio: '
                    print torneio
                    print 'Pai1 (%d): ' % (torneio[j])
                    print populacao[torneio[j]].alelos
                    print 'Pai2 (%d):' % (torneio[j+1])
                    print populacao[torneio[j+1]].alelos
                    print 'Ponto de corte: %d' % (ate)
                    print 'Filho1: '
                    print filho1.alelos
                    print 'Filho2: '
                    print filho2.alelos
                    print '==============='
                
                # Adiciono os filhos gerados na nova população
                novaPop.append(filho1)
                novaPop.append(filho2)
                j = j+2
            # Inicio mutação
            r = d519.randrange(0,100)
            if r < mutacao:
                if debug:
                    print 'Entrou mutação'
                # Para cada indivíduo de novaPop, seleciono um bit aleatório e inverto o valor
                for j in range(0,m):
                    bit = d519.randrange(0,n)
                    if novaPop[j].alelos[bit]:
                        novaPop[j].alelos[bit] = False
                    else:
                        novaPop[j].alelos[bit] = True
            # Fim mutação

            # Atualiza população somente se gerou, pelo menos, uma solução factível.
            # Se não gerou solução alguma factível, a população não é atualizada
            aceitaNovaPop = False
            for j in range(0,m):
                if novaPop[j].calculaPeso() <= W:
                    aceitaNovaPop = True
                    break
                
            if aceitaNovaPop:
                del populacao
                populacao = novaPop
            #terminou crossover/mutacao
            
        # Procedimentos para fim geração
            
        # Verifico quem é o melhor para adicionar em melhoresGeracao
        # Imprime melhor solução FACTÍVEL
        best = [-1, 0, 0]
        for j in range(0,m):
            if populacao[j].calculaValor() > best[1] and populacao[j].calculaPeso() <= W:
                best = [j, populacao[j].calculaValor(), populacao[j].calculaPeso()]
        if best[0] == -1:
            if debug:
                print 'Nao obteve solução factível ):'
            melhoresGeracao.append(0)
        else:
            melhoresGeracao.append(best[1])
        
        if debug:
            print 'Fim da geração %d' % (i)
        
        # Mostro os cromossomos da população
        for j in range(0,m):
            if debug:
                print 'Cromossomo %d: Valor: %f Peso: %f Penalidade: %f' % (j, populacao[j].calculaValor(), populacao[j].calculaPeso(), populacao[j].penalidade)
                print populacao[j].alelos
            avg[i] = avg[i]+populacao[j].calculaValor()
        avg[i] = avg[i]/float(m)
        
        """
        # Verifico condição de parada
        if avg[i] == ultimoResultado:
            mesmoResultado = mesmoResultado + 1
            if mesmoResultado == v:
                break
        else:
            ultimoResultado = avg[i]
            mesmoResultado = 0
        """ 
    
    # Imprime melhor solução FACTÍVEL
    best = [-1, 0, 0]
    for j in range(0,m):
        if populacao[j].calculaValor() > best[1] and populacao[j].calculaPeso() <= W:
            best = [j, populacao[j].calculaValor(), populacao[j].calculaPeso()]
    if best[0] == -1:
        print 'Nao obteve solução factível ):'
        return 0
    
    if debug:
        # Obteve solução factível e imprima a melhor (cromossomo)
        print '---------------'
        print 'Melhor solução no cromossomo %d: %f com peso %f' % (best[0], best[1], best[2])
        print populacao[best[0]].alelos
        
        print '---------------'
        print 'Medias das gerações: '
        print avg
    #return populacao[best[0]].alelos
    return melhoresGeracao
    
#print len(mono_ga([False]))
#print mono_ga([False])