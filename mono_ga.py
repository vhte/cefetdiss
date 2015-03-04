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
W = 0
M = []
V = []
n = 0

class Cromossomo:
    alelos = [False]
    fitness = 0
    penalidade = 0
    valor = 0
    peso = 0
    
    # Inicia o cromossomo aleatório
    def __init__(self,n,novo=False):
        self.alelos = self.alelos * n
        
        if novo:
            return
            
        
        # Gerando posições de alelos aleatórias
        
        for i in range(0,int(n*0.5)): # até 50% da solução inicial
            self.alelos[d519.randrange(0,n)] = True
        """
        for i in range(0,n):
            if d519.randrange(0,100) > 89:
                self.alelos[i] = True
        """
        
        
        """
        # Gerando posições de alelos gulosos
        for i in range(0,n):
            if V[i]/float(M[i]) > 3:
                self.alelos[i] = True
        """
                
        # Verifica se respeita o knapsack
        self.calculaPeso()
        while self.peso > W:
            # Retira um item aleatorio
            tmp = d519.randrange(0,n)
            self.alelos[tmp] = False
            # Recalculo
            self.valor = self.valor - V[tmp]
            self.peso = self.peso - M[tmp]

    def calculaRho(self):
        rho = 0
        for i in range(0,n):
            # calculo rho
            if V[i]/float(M[i]) > rho:
                rho = V[i]/float(M[i])
        return rho
                
    def calculaPeso(self):
        peso = 0
        for i in range(0,n):
            if self.alelos[i]:
                peso = peso + M[i]
        self.peso = peso
    
    def calculaValor(self):
        valor = 0
        for i in range(0,n):
            if self.alelos[i]:
                valor = valor + V[i]
        self.valor = valor

    def calculaFitness(self):
        return self.valor - self.penalidade

    def calculaPenalidade(self):
        # Calcula a penalidade do problema e armazena (se houver)
        if self.calculaPeso() < W:
            self.penalidade = 0
            return
        self.penalidade = self.calculaRho() * (self.calculaPeso() - W)
        
####################### MAIN #######################
def mono_ga(params):
    ########### PARAMETROS ###########
    global W,M,V,n
    # debug
    debug = params[0]
    # problem knapsack
    W=params[1]
    M=params[2]
    V=params[3]
    # Total itens
    n = len(M)
    # Numero de geracoes
    g = params[4] #600
    # Tamanho populacao
    m = params[5] #150
    # Probabilidade crossover
    crossover = params[6] #90
    # Probabilidade mutacao
    mutacao = params[7] #5
    # Pressão seletiva
    pS = params[8] #3
    
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
                
                # Calculo valor e peso dos filhos
                filho1.calculaValor()
                filho2.calculaPeso()
                
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
                        novaPop[j].valor = novaPop[j].valor - V[bit]
                        novaPop[j].peso = novaPop[j].peso - M[bit]
                    else:
                        novaPop[j].alelos[bit] = True
                        novaPop[j].valor = novaPop[j].valor + V[bit]
                        novaPop[j].peso = novaPop[j].peso + M[bit]
            # Fim mutação
                        
            # Iniciou Elitismo
            # Se a melhor solucao de novaPop for pior que a melhor solucao de populacao, O(2N)
            bests = [-1,0,-1,0] # [pospopulacao, fitnesspopulacao, posnovapop, fitnessnovapop]
            for j in range(0,m):
                fitness = populacao[j].calculaFitness()
                if fitness > bests[1]:
                    bests[0] = j
                    bests[1] = fitness
                    
                fitness = novaPop[j].calculaFitness()
                if fitness > bests[3]:
                    bests[2] = j
                    bests[3] = fitness
                
            if bests[1] > bests[3]:
                # Selecionar um membro aleatório de novaPop e adicionar o melhor de populacao
                novaPop[d519.randrange(0,m)] = populacao[bests[0]]
            
            # Fim Elitismo

            # Atualiza população somente se gerou, pelo menos, uma solução factível.
            # Se não gerou solução alguma factível, a população não é atualizada
            aceitaNovaPop = False
            for j in range(0,m):
                if novaPop[j].peso <= W:
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
            valor = populacao[j].valor
            peso = populacao[j].peso
            if valor > best[1] and peso <= W:
                best = [j, valor, peso]
        if best[0] == -1:
            if debug:
                print 'Nao obteve solução factível ):'
            # Como nenhuma solução é factível, recupero a com maior fitness e vou retirando aleatoriamente até ela ser factível
            populacao.sort(key=lambda x: x.calculaFitness(), reverse=True)
            while populacao[0].peso > W:
                tmp = d519.randrange(0,n)
                populacao[0].alelos[tmp] = False
                populacao[0].valor = populacao[0].valor - V[tmp]
                populacao[0].peso = populacao[0].peso - M[tmp]

            melhoresGeracao.append(populacao[0].valor)
        else:
            melhoresGeracao.append(best[1])
        
        if debug:
            print 'Fim da geração %d' % (i)
        
        # Mostro os cromossomos da população
        for j in range(0,m):
            if debug:
                print 'Cromossomo %d: Valor: %f Peso: %f Penalidade: %f' % (j, populacao[j].valor, populacao[j].peso, populacao[j].penalidade)
                print populacao[j].alelos
            avg[i] = avg[i]+populacao[j].valor
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
        valor = populacao[j].valor
        peso = populacao[j].peso
        if valor > best[1] and peso <= W:
            best = [j, valor, peso]
    if best[0] == -1:
        print 'Nao obteve solução factível ):'
        raw_input('Nao obteve solucao factivel')
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