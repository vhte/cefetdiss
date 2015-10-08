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
        if tipoProblema == 0:
            aleatorio = int(n*0.1)
        else:
            aleatorio = int(n*0.1)
        for i in range(0,aleatorio): # até 50% da solução inicial
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
                
        self.calculaPeso()
        self.calculaValor()
        
        # Verifica se respeita o knapsack
        if tipoProblema == 0:
            while self.peso > W:
                # Retira um item aleatorio
                tmp = d519.randrange(0,n)
                self.alelos[tmp] = False
                # Recalculo
                self.valor = self.valor - V[tmp]
                self.peso = self.peso - M[tmp]
        else:
            while self.calculaICAlim() < ICLimite:
                # Adiciona um item aleatorio
                tmp = d519.randrange(0,n)
                self.alelos[tmp] = True
                # Recalculo
                self.valor = self.valor + V[tmp]
                self.peso = self.peso + M[tmp]
        
    '''
    def calculaRho(self):
        rho = 0
        for i in range(0,n):
            # calculo rho
            if V[i]/float(M[i]) > rho:
                rho = V[i]/float(M[i])
        self.rho = rho
    '''         
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

    # Maior fitness para max() menor fitness para min()
    def calculaFitness(self):
        if tipoProblema == 0:
            return self.valor - self.penalidade
        else:
            return self.peso + self.penalidade

    # Calcula a penalidade do problema e armazena (se houver)
    def calculaPenalidade(self):
        if tipoProblema == 0:
            if self.peso <= W:
                self.penalidade = 0
            else:
                self.penalidade = rho * (self.peso - W)
        else:
            if self.calculaICAlim() >= ICLimite:
                self.penalidade = 0
            else:
                self.penalidade = rho * (self.peso + 100) #rho * (ICLimite - self.calculaICAlim())

    def calculaICAlim(self):
        # Monta os vetores de segmento
        produtoAlim = 1
        for i in range(0,len(gruposSegmentos)):
            produtoSeg = 1
            for j in range(0,len(gruposSegmentos[i])):
                # Se está na solucao deve ser 1
                if self.alelos[gruposSegmentos[i][j]]:
                    produtoSeg = produtoSeg * 0.9999999
                else:
                    produtoSeg = produtoSeg * (1 - V[gruposSegmentos[i][j]]) # pois ics na verdade é 1-IC mono.py
            #print 'produtoSeg = %f' % (produtoSeg)
            produtoSeg = pow(produtoSeg, 1/float(len(gruposSegmentos[i])))
            produtoAlim = produtoAlim * produtoSeg
        return pow(produtoAlim, 1/float(len(gruposSegmentos)))
        
####################### MAIN #######################
def mono_ga(params):
    ########### PARAMETROS ###########
    global W,M,V,n,rho,gruposSegmentos,tipoProblema,ICLimite,avaliacoes
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
    #Número de cortes para geração dos filhos
    cortes = params[9]
    #Número de buscas locais assim que nova população é gerada
    buscaLocal = params[10]
    # Posições das soluções intermediárias para justificar o ajuste de parâmetros
    intermediarias = params[11]
    sIntermediarias = []
    # Lista de listas com os ids de cada ics para fazer media geometrica
    gruposSegmentos = params[12]
    # Parte do knapsack, IC limite do alimentador
    ICLimite = params[13]
    # Tipo de problema, max(1-IC) [0] ou min(Custo) [1]
    tipoProblema = params[14]
    
    melhoresGeracao = [] # a resposta do algoritmo, para cada geração uma única resposta será enviada
    avaliacoes = 0  # numero de avaliacoes de solucao objetivo
    
    # calcula rho estatico para usar na penalização
    rho = 0
    for i in range(0,n):
        # calculo rho
        if V[i]/float(M[i]) > rho:
            rho = V[i]/float(M[i])
    
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
    
    """   
    for i in range(0,m):
        print 'V[%d]: %f' % (i,populacao[i].valor)
        print 'M[%d]: %f' % (i,populacao[i].peso)
    raw_input('parou')
    """
    # Seto o número de vezes em que a geração deu o mesmo resultado
    #mesmoResultado = 0
    #ultimoResultado = 0
    # Inicio as gerações
    for i in range(0,g):
    #i = 0 # para num avaliacoes
    #while i < g and avaliacoes < 210000:
        i = i +1
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
        
        # Crio vetor de nova populacao
        novaPop = []
        # Crio uma cópia da população atual caso a nova não consiga solução factível
        popBkp = d519.copy.copy(populacao)
        
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
                    
                if tipoProblema == 0:
                    melhor = [0, 0] # [pos, val]
                else:                    
                    melhor = [0, float('inf')] # [pos, pes]
                for k in range(0,pS):
                    fitnessCandidato = populacao[candidatos[k]].calculaFitness()
                    if tipoProblema == 0:
                        if fitnessCandidato > melhor[1]:
                            melhor = [k, fitnessCandidato]
                    else:
                        if fitnessCandidato < melhor[1]:
                            melhor = [k, fitnessCandidato]
                    
                vencedorAnterior = candidatos[melhor[0]]
                torneio.append(candidatos[melhor[0]])
                   
                j = j+1
            if debug:
                print 'torneio: '
                print torneio
            
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
                """
                for k in range(0,ate):
                    filho1.alelos[k] = populacao[torneio[j]].alelos[k]
                    if filho1.alelos[k]:
                        filho1.valor = filho1.valor + V[k]
                        filho1.peso = filho1.peso + M[k]
                    filho2.alelos[k] = populacao[torneio[j+1]].alelos[k]
                    if filho2.alelos[k]:
                        filho2.valor = filho2.valor + V[k]
                        filho2.peso = filho2.peso + M[k]
                #Gerando segunda metade de filho1 e filho2
                for k in range(ate,n):
                    filho1.alelos[k] = populacao[torneio[j+1]].alelos[k]
                    if filho1.alelos[k]:
                        filho1.valor = filho1.valor + V[k]
                        filho1.peso = filho1.peso + M[k]
                    filho2.alelos[k] = populacao[torneio[j]].alelos[k]
                    if filho2.alelos[k]:
                        filho2.valor = filho2.valor + V[k]
                        filho2.peso = filho2.peso + M[k]
                """
                
                # INICIO C/ CORTES
                cortesV = [0]*cortes
                alpha = 1
                inicio = 0
                for l in range(0,cortes):
                    cortesV[l] = d519.randrange(inicio+1, n-cortes+alpha)
                    alpha = alpha+1
                    inicio = cortesV[l]
                
                atual = 0
                tmp = 0
                for l in range(0,cortes):
                    # Alternando entre os pais
                    if tmp % 2 == 0:
                        pai1 = j
                        pai2 = j+1
                    else:
                        pai1 = j+1
                        pai2 = j
    
                    for k in range(atual,cortesV[l]):
                        filho1.alelos[k] = populacao[torneio[pai1]].alelos[k]
                        if filho1.alelos[k]:
                            filho1.valor = filho1.valor + V[k]
                            filho1.peso = filho1.peso + M[k]
                        filho2.alelos[k] = populacao[torneio[pai2]].alelos[k]
                        if filho2.alelos[k]:
                            filho2.valor = filho2.valor + V[k]
                            filho2.peso = filho2.peso + M[k]
                        
                    atual = cortesV[l]
                    tmp = tmp + 1
                # Ultima parte
                for k in range(atual, n):
                    filho1.alelos[k] = populacao[torneio[pai2]].alelos[k]
                    if filho1.alelos[k]:
                        filho1.valor = filho1.valor + V[k]
                        filho1.peso = filho1.peso + M[k]
                    filho2.alelos[k] = populacao[torneio[pai1]].alelos[k]
                    if filho2.alelos[k]:
                        filho2.valor = filho2.valor + V[k]
                        filho2.peso = filho2.peso + M[k] # Inverte pais
                # FIM C/ CORTES
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
                #filho1.calculaValor()
                #filho2.calculaValor()
                #filho1.calculaPeso()
                #filho2.calculaPeso()
                avaliacoes = avaliacoes + 2 # Calculo dos dois filhos
                
                # Adiciono os filhos gerados na nova população
                novaPop.append(filho1)
                novaPop.append(filho2)
                j = j+2
            
                        
            # Iniciou Elitismo
            # Se a melhor solucao de novaPop for pior que a melhor solucao de populacao, O(2N)
            # [pospopulacao, fitnesspopulacao, posnovapop, fitnessnovapop]
            if tipoProblema == 0:
                bests = [-1,0,-1,0]
            else:
                bests = [-1,float('inf'),-1,float('inf')]
            for j in range(0,m):
                fitness = populacao[j].calculaFitness()
                if tipoProblema == 0:
                    if fitness > bests[1]:
                        bests[0] = j
                        bests[1] = fitness
                else:
                    if fitness < bests[1]:
                        bests[0] = j
                        bests[1] = fitness
                    
                # Computa penalidade, se existir
                novaPop[j].calculaPenalidade()
                fitness = novaPop[j].calculaFitness()
                if tipoProblema == 0:
                    if fitness > bests[3]:
                        bests[2] = j
                        bests[3] = fitness
                else:
                    if fitness < bests[3]:
                        bests[2] = j
                        bests[3] = fitness
                
            if tipoProblema == 0:
                if bests[1] > bests[3]:
                    # Selecionar um membro aleatório de novaPop e adicionar o melhor de populacao
                    novaPop[d519.randrange(0,m)] = populacao[bests[0]]
            else:
                if bests[1] < bests[3]:
                    # Selecionar um membro aleatório de novaPop e adicionar o melhor de populacao
                    novaPop[d519.randrange(0,m)] = populacao[bests[0]]
            
            # Fim Elitismo

            
        # Inicio mutação
        r = d519.randrange(0,100)
        if r < mutacao:
            # Verifica se entrou no crossover
            if len(novaPop) == 0:
                novaPop = d519.copy.copy(populacao)
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
                avaliacoes = avaliacoes + 1
        # Fim mutação    
        
        #terminou crossover/mutacao
                    
        
        if len(novaPop) != 0:
            populacao = d519.copy.copy(novaPop)
        
        # Atualiza população somente se gerou, pelo menos, uma solução factível.
        # Se não gerou solução alguma factível, a população não é atualizada
        popValida = False
        for j in range(0,m):
            if tipoProblema == 0:
                if populacao[j].peso <= W:
                    # Aceita nova população
                    popValida = True
                    break
            else:
                if populacao[j].calculaICAlim() >= ICLimite:
                    # Aceita nova população
                    popValida = True
                    break
        if not popValida:
            # Usa o backup
            populacao = popBkp
        
        # Procedimentos para fim geração
        # Busca local (diversidade)
        if buscaLocal > 0:
            # Para cada individuo da populacao, executo n buscas locais aleatórias
            for j in range(0,m):
                # altera ate buscaLocal posicoes aleatórias
                tmp = d519.copy.copy(populacao[j].alelos)
                tmpValues = [d519.copy.copy(populacao[j].valor), d519.copy.copy(populacao[j].peso)]
                for k in range(0,buscaLocal):
                    pos = d519.randrange(0,n)
                    if populacao[j].alelos[pos]:
                        populacao[j].alelos[pos] = False
                        populacao[j].valor = populacao[j].valor - V[pos]
                        populacao[j].peso = populacao[j].peso - M[pos]
                    else:
                        populacao[j].alelos[pos] = True
                        populacao[j].valor = populacao[j].valor + V[pos]
                        populacao[j].peso = populacao[j].peso + M[pos]
                # Verifico NÃO se melhorou 'populacao' já alterada.
                # Lembrando: tmp é o original, populacao é o alterado
                if tipoProblema == 0:
                    if populacao[j].valor < tmpValues[0] or populacao[j].peso > W:
                        # Volta
                        populacao[j].alelos = tmp
                        populacao[j].valor= tmpValues[0]
                        populacao[j].peso = tmpValues[1]
                else:
                    if populacao[j].peso > tmpValues[0] or populacao[j].calculaICAlim() < ICLimite:
                        # Volta
                        populacao[j].alelos = tmp
                        populacao[j].valor= tmpValues[0]
                        populacao[j].peso = tmpValues[1]
            
        
        # Verifico quem é o melhor para adicionar em melhoresGeracao
        # Imprime melhor solução FACTÍVEL
        if tipoProblema == 0:
            best = [-1, 0, 0]
        else:
            best = [-1, float('inf'), 0]
        
        for j in range(0,m):
            valor = populacao[j].valor
            peso = populacao[j].peso

            if tipoProblema == 0:
                if valor > best[1] and peso <= W:
                    best = [j, valor, peso]
            else:
                if peso < best[1] and populacao[j].calculaICAlim() >= ICLimite:
                    best = [j, peso, valor]
                    
        if best[0] == -1:
            for j in range(0,m):
                populacao[j].calculaPenalidade()
            if debug:
                print 'Nao obteve solução factível ):'
            # Como nenhuma solução é factível, recupero a com maior/menor fitness e vou retirando aleatoriamente até ela ser factível
            if tipoProblema == 0:
                populacao.sort(key=lambda x: x.calculaFitness(), reverse=True)
                while populacao[0].peso > W:
                    tmp = d519.randrange(0,n)
                    populacao[0].alelos[tmp] = False
                    populacao[0].valor = populacao[0].valor - V[tmp]
                    populacao[0].peso = populacao[0].peso - M[tmp]
                melhoresGeracao.append(populacao[0].valor)
                # Verifica se é para inserir nas soluções intermediárias
                if i in intermediarias:
                        sIntermediarias.append(populacao[0].valor)
            else:
                populacao.sort(key=lambda x: x.calculaFitness(), reverse=False)
                while populacao[0].calculaICAlim() < ICLimite:
                    tmp = d519.randrange(0,n)
                    populacao[0].alelos[tmp] = True
                    populacao[0].valor = populacao[0].valor + V[tmp]
                    populacao[0].peso = populacao[0].peso + M[tmp]
                melhoresGeracao.append(populacao[0].peso)
                # Verifica se é para inserir nas soluções intermediárias
                if i in intermediarias:
                        sIntermediarias.append(populacao[0].peso)
        else:
            melhoresGeracao.append(best[1])
            if i in intermediarias:
                    sIntermediarias.append(best[1])
        
        if debug:
            print 'Fim da geração %d' % (i)
    
    # Imprime melhor solução FACTÍVEL
    if tipoProblema == 0:
        best = [-1, 0, 0]
    else:
        best = [-1, float('inf'), 0]
    for j in range(0,m):
        valor = populacao[j].valor
        peso = populacao[j].peso
        if tipoProblema == 0:
            if valor > best[1] and peso <= W:
                best = [j, valor, peso]
        else:
            if peso < best[1] and populacao[j].calculaICAlim() >= ICLimite:
                best = [j, peso, valor]
    if best[0] == -1:
        print 'Nao obteve solução factível ):'
        raw_input('Nao obteve solucao factivel. Pressione qualquer tecla para terminar ...')
        return 0
    
    if debug:
        # Obteve solução factível e imprima a melhor (cromossomo)
        print '---------------'
        print 'Melhor solução no cromossomo %d: %f com peso %f' % (best[0], best[1], best[2])
        print populacao[best[0]].alelos
        
    #return populacao[best[0]].alelos
    return [melhoresGeracao, sIntermediarias,avaliacoes]