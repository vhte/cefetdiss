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
@todo Condição de parada: Se der o mesmo resultado n vezes. Ele pode sair do ótimo global se ficar muito tempo gerando novas populações em cima dele

@author Victor Torres - victorhugo@lsi.cefetmg.br

https://pythonhosted.org/ete2/tutorial/tutorial_trees.html
http://stackoverflow.com/questions/2349991/python-how-to-import-other-python-files
http://stackoverflow.com/questions/9542738/python-find-in-list
"""
import d519
import math # math.floor() para baixo round() para cima

########### PARAMETROS ###########
# Numero de geracoes
g = 100
# Tamanho populacao
m = 150
# Probabilidade crossover
crossover = 90
# Probabilidade mutacao
mutacao = 5
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
W=1500 # Best ~ V = 1020
M=[8, 19, 38, 66, 15, 62, 19, 95, 74, 55, 7, 41, 65, 65, 61, 29, 82, 45, 27, 7, 97, 79, 91, 14, 93, 41, 61, 55, 80, 74, 27, 66, 72, 49, 33, 47, 55, 61, 40, 16, 60, 29, 68, 9, 21, 88, 74, 10, 32, 96, 45, 98, 39, 42, 9, 40, 48, 2, 56, 36, 7, 50, 52, 59, 98, 64, 52, 87, 54, 23, 64, 84, 18, 64, 92, 56, 40, 31, 47, 36, 80, 61, 27, 61, 35, 55, 34, 39, 46, 82, 42, 81, 35, 10, 54, 24, 84, 2, 11, 49]
V=[27, 48, 99, 54, 42, 43, 38, 96, 49, 81, 85, 63, 89, 46, 73, 3, 9, 3, 89, 89, 20, 32, 1, 92, 88, 71, 76, 47, 7, 32, 22, 66, 32, 26, 1, 94, 6, 58, 67, 37, 58, 94, 79, 1, 17, 1, 65, 61, 92, 57, 67, 60, 78, 23, 93, 58, 52, 82, 50, 24, 49, 42, 54, 21, 83, 70, 1, 53, 7, 5, 3, 26, 60, 98, 21, 71, 19, 36, 74, 50, 16, 97, 15, 24, 8, 78, 9, 67, 22, 41, 17, 11, 87, 25, 87, 89, 69, 4, 7, 27]
# Total itens
n = len(M)

class Cromossomo:
    alelos = [0]
    fitness = 0
    penalidade = 0
    
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

    def calculaPenalidade(self):
        # Calcula a penalidade do problema e armazena (se houver)
        if self.calculaPeso() < W:
            self.penalidade = 0
            return

        totalPesoCrom = self.calculaPeso()
        rho = self.calculaRho()
        self.penalidade = rho * (totalPesoCrom - W)
        
####################### MAIN #######################
def mono_ga(params):
    debug = params[0]
    
    melhoresGeracao = [] # a resposta do algoritmo, para cada geração uma única resposta será enviada
    avg = [0]*g
    if debug:
        print 'Iniciou o algoritmo'
    # Crio os cromossomos e gero populacao 1
    populacao = [0]*m
    if debug:
        print 'Instaciou população'
    for i in range(0,m):
        populacao[i] = Cromossomo(n)
        
        # Avalio cada cromossomo e armazeno seu valor
        populacao[i].fitness = populacao[i].calculaFitness()
    
    if debug:
        print 'Criou populacao'
    
    # Seto o número de vezes em que a geração deu o mesmo resultado
    #mesmoResultado = 0
    #ultimoResultado = 0
    # Inicio as gerações
    for i in range(0,g):
        if debug:
            print 'Inicio geração %d' % (i)
            for j in range(0,m):
                print populacao[j].alelos
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
            while j < m:
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
                    if novaPop[j].alelos[bit] == 1:
                        novaPop[j].alelos[bit] = 0
                    else:
                        novaPop[j].alelos[bit] = 1
            # Fim mutação
            # Calcula penalidade dos filhos
            for j in range(0,m):
                novaPop[j].calculaPenalidade()    

            # Atualiza população
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
        if debug:
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
