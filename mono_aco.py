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

########### PARAMETROS ###########
# Numero de iteracoes
g = 500
# Numero de formigas
m = 10 # Generally, it is defined that the number of ants (m) is equal to that of articles (n)

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

W=1500 # Best ~ V = 1020
M=[8, 19, 38, 66, 15, 62, 19, 95, 74, 55, 7, 41, 65, 65, 61, 29, 82, 45, 27, 7, 97, 79, 91, 14, 93, 41, 61, 55, 80, 74, 27, 66, 72, 49, 33, 47, 55, 61, 40, 16, 60, 29, 68, 9, 21, 88, 74, 10, 32, 96, 45, 98, 39, 42, 9, 40, 48, 2, 56, 36, 7, 50, 52, 59, 98, 64, 52, 87, 54, 23, 64, 84, 18, 64, 92, 56, 40, 31, 47, 36, 80, 61, 27, 61, 35, 55, 34, 39, 46, 82, 42, 81, 35, 10, 54, 24, 84, 2, 11, 49]
V=[27, 48, 99, 54, 42, 43, 38, 96, 49, 81, 85, 63, 89, 46, 73, 3, 9, 3, 89, 89, 20, 32, 1, 92, 88, 71, 76, 47, 7, 32, 22, 66, 32, 26, 1, 94, 6, 58, 67, 37, 58, 94, 79, 1, 17, 1, 65, 61, 92, 57, 67, 60, 78, 23, 93, 58, 52, 82, 50, 24, 49, 42, 54, 21, 83, 70, 1, 53, 7, 5, 3, 26, 60, 98, 21, 71, 19, 36, 74, 50, 16, 97, 15, 24, 8, 78, 9, 67, 22, 41, 17, 11, 87, 25, 87, 89, 69, 4, 7, 27]
"""
W=15000
M=[57, 72, 51, 96, 82, 61, 65, 66, 53, 82, 61, 70, 54, 83, 66, 89, 83, 66, 52, 52, 54, 85, 62, 72, 87, 89, 68, 50, 71, 57, 73, 85, 58, 77, 75, 99, 71, 55, 84, 59, 82, 97, 99, 53, 73, 62, 93, 63, 89, 59, 84, 54, 93, 71, 78, 55, 69, 67, 57, 91, 82, 60, 78, 64, 54, 86, 66, 73, 56, 71, 87, 58, 53, 95, 92, 94, 53, 78, 72, 82, 74, 68, 55, 74, 82, 59, 68, 66, 64, 93, 76, 92, 88, 76, 54, 97, 78, 82, 60, 63, 84, 95, 58, 89, 77, 96, 89, 76, 77, 54, 79, 70, 98, 53, 76, 94, 79, 83, 63, 71, 99, 77, 64, 98, 52, 87, 50, 80, 51, 67, 56, 62, 62, 52, 51, 84, 89, 79, 52, 53, 57, 74, 92, 79, 84, 95, 55, 87, 76, 69, 90, 71, 79, 50, 68, 57, 96, 73, 63, 96, 80, 93, 72, 80, 88, 71, 73, 77, 99, 56, 76, 87, 58, 56, 52, 94, 83, 63, 68, 89, 60, 90, 78, 51, 68, 57, 79, 73, 57, 56, 83, 57, 57, 75, 77, 60, 70, 87, 87, 99, 54, 88, 80, 86, 74, 96, 84, 87, 82, 80, 82, 52, 99, 62, 77, 50, 52, 58, 90, 80, 80, 64, 82, 61, 70, 54, 82, 66, 70, 82, 90, 62, 69, 75, 69, 78, 50, 71, 81, 71, 95, 58, 69, 96, 51, 78, 70, 75, 87, 95, 87, 81, 67, 66, 72, 98, 73, 60, 97, 97, 70, 97, 54, 56, 69, 73, 85, 90, 89, 80, 93, 79, 63, 67, 99, 73, 74, 93, 94, 53, 65, 79, 65, 56, 78, 94, 60, 86, 64, 65, 75, 67, 85, 56, 99, 87, 92, 78, 74, 58, 55, 94, 89, 98, 84, 71, 53, 80, 52, 52, 51, 70, 57, 56, 84, 98, 60, 57, 89, 63, 51, 54, 77, 96, 92, 62, 64, 62, 75, 90, 71, 88, 55, 66, 72, 66, 71, 60, 93, 80, 96, 63, 92, 86, 60, 77, 57, 65, 67, 86, 78, 59, 65, 98, 81, 66, 90, 61, 94, 84, 52, 55, 66, 60, 65, 79, 76, 88, 95, 66, 65, 92, 62, 75, 99, 63, 92, 97, 97, 72, 90, 87, 64, 87, 68, 86, 72, 66, 82, 90, 76, 68, 55, 56, 83, 50, 83, 90, 67, 83, 56, 83, 87, 55, 73, 90, 53, 94, 54, 50, 62, 75, 98, 77, 96, 81, 78, 95, 52, 69, 94, 51, 53, 72, 72, 78, 68, 60, 97, 67, 77, 60, 88, 85, 73, 85, 65, 88, 56, 51, 73, 66, 75, 83, 91, 60, 56, 99, 81, 53, 50, 72, 94, 61, 54, 67, 63, 65, 73, 50, 85, 73, 70, 86, 59, 61, 57, 52, 66, 70, 90, 96, 53, 95, 50, 94, 73, 58, 71, 74, 90, 90, 61, 98, 93, 84, 69, 83, 62, 83, 77, 99, 52, 74, 86, 50, 85, 51, 55, 58]
V=[164, 835, 881, 190, 440, 785, 685, 80, 630, 192, 649, 220, 538, 625, 722, 43, 587, 863, 183, 907, 616, 278, 485, 997, 208, 513, 951, 512, 699, 241, 772, 460, 79, 247, 527, 942, 993, 520, 566, 837, 749, 133, 835, 175, 751, 644, 331, 287, 903, 268, 758, 790, 345, 915, 287, 432, 38, 630, 347, 628, 915, 266, 652, 785, 240, 713, 946, 634, 253, 323, 949, 47, 685, 981, 493, 634, 418, 856, 866, 693, 159, 830, 501, 104, 59, 377, 732, 336, 666, 298, 673, 822, 36, 734, 68, 245, 629, 688, 723, 83, 363, 77, 103, 188, 700, 286, 33, 355, 716, 59, 427, 308, 735, 698, 266, 998, 259, 686, 865, 798, 16, 868, 551, 912, 97, 54, 614, 794, 714, 772, 316, 461, 387, 609, 41, 655, 936, 38, 998, 976, 41, 607, 930, 726, 593, 82, 654, 631, 36, 323, 120, 843, 823, 932, 240, 172, 15, 333, 559, 801, 753, 457, 408, 986, 46, 259, 620, 642, 782, 15, 955, 179, 230, 407, 660, 904, 532, 204, 485, 473, 219, 672, 888, 586, 492, 888, 500, 846, 489, 730, 539, 977, 559, 135, 46, 322, 417, 357, 237, 646, 95, 891, 17, 6, 785, 832, 850, 574, 512, 2, 854, 698, 79, 35, 395, 924, 108, 323, 666, 86, 168, 427, 847, 166, 218, 421, 655, 929, 885, 281, 535, 805, 839, 509, 899, 783, 237, 515, 634, 724, 201, 354, 891, 108, 526, 181, 957, 582, 397, 364, 558, 900, 679, 530, 53, 718, 906, 909, 963, 909, 957, 404, 996, 119, 968, 633, 21, 36, 52, 266, 466, 121, 82, 918, 538, 269, 625, 21, 858, 905, 41, 437, 358, 550, 294, 960, 417, 807, 24, 631, 80, 8, 170, 112, 801, 421, 856, 504, 203, 507, 361, 782, 378, 250, 617, 500, 663, 171, 267, 721, 288, 317, 344, 560, 693, 401, 188, 155, 423, 921, 341, 215, 439, 309, 320, 832, 770, 544, 138, 47, 480, 49, 464, 21, 133, 778, 133, 917, 105, 581, 234, 652, 942, 599, 355, 195, 206, 57, 186, 896, 543, 83, 259, 951, 84, 602, 696, 51, 788, 82, 256, 816, 210, 627, 618, 634, 49, 691, 305, 812, 952, 900, 635, 229, 835, 685, 828, 372, 666, 531, 958, 980, 744, 146, 446, 937, 918, 426, 359, 808, 237, 518, 376, 47, 971, 851, 447, 545, 211, 965, 230, 859, 83, 892, 247, 957, 779, 816, 144, 464, 182, 957, 964, 364, 919, 824, 352, 870, 410, 396, 547, 799, 737, 532, 506, 813, 57, 317, 871, 734, 947, 301, 738, 222, 587, 351, 534, 614, 922, 693, 885, 312, 344, 178, 294, 382, 322, 173, 577, 280, 127, 502, 359, 879, 543, 385, 276, 55, 494, 186, 100, 886, 497, 335, 521, 891, 622, 95, 617, 360, 413, 903, 72, 6, 331, 746, 684, 354, 325, 642, 191, 871, 327, 148, 503, 264, 424, 864, 946, 558, 657, 357, 727, 228, 339, 440, 819, 978, 129, 814]

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
        # Como vai começar uma nova colônia, o peso das formigas já mudou e por isto um novo ferormonioDelta deve ser calculado
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
#print mono_aco([False])