# -*- coding: utf-8 -*-
"""
Variable Neighborhood Search (VNS)
Problema: Otimização mono-objetivo para maximização de IC com limite de custo
Entrada: Equipamentos do Segmento
Saida: Melhor solução de troca
Vizinho: Como a definição da entrada é binária, é a troca de 1 bit e avaliação deste

@author Victor Torres

https://pythonhosted.org/ete2/tutorial/tutorial_trees.html
http://stackoverflow.com/questions/2349991/python-how-to-import-other-python-files

@todo Talvez melhorar a solução inicial
"""
import d519
def mono_ils(params):
    debug = params[0]
    
    melhoresGeracao = [] # a resposta do algoritmo, para cada geração uma única resposta será enviada
    
    ########### PARAMETROS #################
    # Número máximo de iterações no loop princpal do ILS.
    iterMaxILS = params[1]#600
    # Número máximo de iterações na busca local. 10% do tamanho da populacao
    # Isto fará com que chegue uma hora em que a restrição monetária não suporte nenhuma outra solução
    iterMaxBL = params[2]#20
    pPert = params[3] #0.001
    iterMaxBL_P = params[4]#1 # Quantas posições serão afetadas da solução corrente
    
    # Problema knapsack
    meuCusto = params[5]#1500
    custos = params[6]
    ics = params[7]
    intermediarias = params[8]
    sIntermediarias = []
    
    ################ METODOS ###############
    
    def calculaPeso(s):
        peso = 0
        for i in range(0,len(s)):
            if s[i]:
                peso = peso + custos[i]
        return peso
    
    def calculaValor(s):
        valor = 0
        for i in range(0,len(s)):
            if s[i]:
                valor = valor + ics[i]
        return valor
        
    # Utilizando Subida (IC) randômico com o número de trocas fornecidas
    # Os vizinhos sao sempre trocas. S
    def buscaLocal(solucaoCorrente):
        # Rodo iterMax vezes
        k = 0
        # Armazeno o valor e peso atuais para não recalcular a todo momento
        valorCorrente = calculaValor(solucaoCorrente)
        valorBL = valorCorrente
        pesoBL = calculaPeso(solucaoCorrente)
        
        # Encontrando um vizinho k qualquer
        s0 = d519.copy.copy(solucaoCorrente)
        
        while k < iterMaxBL:
            k = k+1
            
            #j = 0
            #while j < iterMaxBL_P: # Altera UMA posição
            # Mudo uma posicao
            pos = d519.randrange(0,len(s0))
            while s0[pos]:
                pos = d519.randrange(0,len(s0))

            s0[pos] = True
            valorBL = valorBL + ics[pos]
            pesoBL = pesoBL + custos[pos]
                
            #j = j+1
            
            # RESTRIÇÃO: Verificando se a soma das trocas são válidas
            if pesoBL > meuCusto:
                s0[pos] = False
                valorBL = valorBL - ics[pos]
                pesoBL = pesoBL - custos[pos]
                # Voltou solução antiga, nada a fazer
                continue
            
            # Se sim, entao verifico qual tem IC melhor
            # Usar >= aqui pode implicar em loop infinito quando muito próximo do ótimo
            if valorBL > valorCorrente:
                k=0 #reseto a iteração
                solucaoCorrente = d519.copy.copy(s0) # nova solução corrente
                s0 = d519.copy.copy(solucaoCorrente)
        return solucaoCorrente #[0]*len(solucaoCorrente)
        
    ################# MAIN #################    
    
        
    # Perturbacao: x% da solucao
    p = int(round(len(ics)*pPert))
    if p < 1:
        p = 1 # Há pelo menus uma pertubação
    
    # Monto a solucao de forma binaria
    s = [False]*len(ics)
    
    # Gerando a solução inicial: Aleatória ou Gulosa. Nao posso permitir que a solucao inicial extrapole muito a restricao, senao a perturbacao nunca encontrara uma solucao factivel
    
    # Aleatório
    aleatorio = int(len(ics)*0.1)
    for i in range(0,aleatorio):
        s[d519.randrange(0,len(ics))] = True
    """ 
    # Guloso
    for i in range(0,len(ics)):
        if ics[i]/float(custos[i]) > 3:
            s[i] = True
    """
    # Nao deixa gerar solução inicial infactível
    while calculaPeso(s) > meuCusto:
        s[d519.randrange(0,len(ics))] = 0
            
    
    
    if debug:
        print 'Solução inicial:'
        print s
        print 'O IC da solucao inicial é %f' % (calculaValor(s))
        print 'O preco da solucao inicial é %d' % (calculaPeso(s))
    # busca local s com Best improvement
    s = buscaLocal(s)
    
    if debug:
        print 'Fim busca local'
    # Inicio loop ILS
    i = 0
    while i < iterMaxILS:
        #print 'Loop ILS %d' % (i)
        # Perturbacao: Gero um número n <= totalEquips*0.1 e esta será a qte de trocas a ser feita
        perturbacao = d519.copy.copy(s)
        for j in range(0,p+1): # o segundo parametro pega ele -1. Se sao 6 equips, só iria pegar até o 5o
            pos = d519.randrange(0,len(ics))
            if perturbacao[pos]:
                perturbacao[pos] = False
            else:
                perturbacao[pos] = True # solucao qualquer pois buscaLocal irá cuidar disto
        
        #print n
        #print perturbacao        
        # Faço novamente buscaLocal
        temp = buscaLocal(perturbacao)
        if debug:
            print 'Executou busca local na iteracao %i do ILS' % (i)
    
        # Restrição (caso o perturbacao gerado tenha sido o ganhador na buscaLocal)
        if calculaPeso(temp) > meuCusto:
            if debug:
                print 'Peso (%i) é maior que meuCusto (%i)' % (calculaPeso(temp),meuCusto)
                
            melhoresGeracao.append(calculaValor(s))
            if i in intermediarias:
                sIntermediarias.append(calculaValor(s))
                
            i = i+1 # Demora muito se permitir que a iteração só suba com solução factível
            continue
        
        # Avalio o melhor
        valorS = calculaValor(s)
        valorT = calculaValor(temp)
        if valorT > valorS:
            s = d519.copy.deepcopy(temp)
            melhoresGeracao.append(valorT)
            if i in intermediarias:
                sIntermediarias.append(valorT)
        else:
            melhoresGeracao.append(valorS)
            if i in intermediarias:
                sIntermediarias.append(valorS)
        i = i+1
        #print calculaValor(temp)
        #print calculaPeso(temp)
    if debug:
        print 'Solução final'
        print s
        print 'O IC da solucao final é %f' % (calculaValor(s))
        print 'O preco da solucao final é %f' % (calculaPeso(s))
    
    # Enquanto o critério de parada não for satisfeito
        # Perturbacao
        # Busca local na perturbacao
        # Verificar se s' melhor que s
    
    # Retorna resultado final
    """
    # Fecha as conexões
    cursor.close()
    cnx.close()
    """
    #return [melhoresGeracao, intermediarias]
    return [melhoresGeracao, sIntermediarias]
