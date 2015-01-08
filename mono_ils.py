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
    iterMaxILS = 100
    # Número máximo de iterações na busca local. 10% do tamanho da populacao
    # Isto fará com que chegue uma hora em que a restrição monetária não suporte nenhuma outra solução
    iterMaxBL = 10
    # Numero de vizinhanças diferentes (vizinhancas é a qte de trocas de equips, primeira vizinhanca só 1 troca)
    vizinhancas = 5
    # Limite de dinheiro que possuo
    meuCusto = 300
    
    ################ METODOS ###############
    
    def calculaPeso(s):
        peso = 0
        for i in range(0,len(s)):
            if s[i] == 1:
                peso = peso + custos[i]
        return peso
    
    def calculaValor(s):
        valor = 0
        for i in range(0,len(s)):
            if s[i] == 1:
                valor = valor + ics[i]
        return valor
        
    # Utilizando Subida (IC) randômico com o número de trocas fornecidas
    # Os vizinhos sao sempre trocas. S
    def buscaLocal(solucaoCorrente):
        # Rodo iterMax vezes
        i = 0
        while i < iterMaxBL:
            i = i+1
            
            # Encontrando um vizinho k qualquer
            s0 =  [0]*len(solucaoCorrente)
            for j in range(0,solucaoCorrente.count(1)):
                rand = d519.randrange(0,len(s0))
                
                while s0[rand] == 1: # Nao deixa repetir a mesma posicao
                    rand = d519.randrange(0,len(s0))
                s0[rand] = 1
            
            # RESTRIÇÃO: Verificando se a soma das trocas são válidas
            if calculaPeso(s0) > meuCusto:
                continue
            
            # Se sim, entao verifico qual tem IC melhor
            # Usar >= aqui pode implicar em loop infinito quando muito próximo do ótimo
            if calculaValor(s0) > calculaValor(solucaoCorrente):
                i=0 #reseto a iteração
                solucaoCorrente = s0 # nova solução corrente
    
        return solucaoCorrente #[0]*len(solucaoCorrente)
        
    ################# MAIN #################
    """
    # Buscando os Equips (ICs)
    cnx = d519.mysql.connector.connect(user='root', password='root', database='cemig_d519')
    cursor = cnx.cursor()
    """
    """
    query = ("select distinct EquipamentoMT.ID, EquipamentoMT.IC, "
            "IF(EquipamentoMT.TIPO_EQUIPAMENTO_ID != 1, EquipamentoNovo.CUSTO, (EquipamentoNovo.CUSTO/1000*CaboMT.COMPRIMENTO)) AS 'CUSTO', "
            "/*EquipamentoNovo.CUSTO,*/ "
            "EquipamentoMT.TIPO_EQUIPAMENTO_ID "
            "from EquipamentoMT "
            "join Segmento ON EquipamentoMT.SEGMENTO_ID = Segmento.ID "
            "join EquipamentoNovo ON EquipamentoNovo.TIPO_EQUIPAMENTO_ID = EquipamentoMT.TIPO_EQUIPAMENTO_ID "
            "left join CaboMT ON EquipamentoMT.ID = CaboMT.ID "
            "where Segmento.ID = 410")
    """
    
    """
    query = ("select distinct EquipamentoMT.ID, EquipamentoMT.IC, "
            "IF(EquipamentoMT.TIPO_EQUIPAMENTO_ID != 1, EquipamentoNovo.CUSTO, (EquipamentoNovo.CUSTO/1000*CaboMT.COMPRIMENTO)) AS 'CUSTO', "
            "/*EquipamentoNovo.CUSTO,*/ "
            "EquipamentoMT.TIPO_EQUIPAMENTO_ID "
            "from EquipamentoMT "
            "join Segmento ON EquipamentoMT.SEGMENTO_ID = Segmento.ID "
            "join Alimentador ON Segmento.ALIMENTADOR_ID = Alimentador.ID "
            "join EquipamentoNovo ON EquipamentoNovo.TIPO_EQUIPAMENTO_ID = EquipamentoMT.TIPO_EQUIPAMENTO_ID "
            "left join CaboMT ON EquipamentoMT.ID = CaboMT.ID "
            "where Alimentador.ID = 3")
    
    cursor.execute(query)
    
    ics = []
    custos = []
    for(ID, IC, CUSTO, TIPO_EQUIPAMENTO_ID) in cursor:
        ics.append(IC) 
        custos.append(CUSTO)
    
    print ics
    print custos
    """
    
    meuCusto=1500 # Best ~ V = 1020
    custos=[8, 19, 38, 66, 15, 62, 19, 95, 74, 55, 7, 41, 65, 65, 61, 29, 82, 45, 27, 7, 97, 79, 91, 14, 93, 41, 61, 55, 80, 74, 27, 66, 72, 49, 33, 47, 55, 61, 40, 16, 60, 29, 68, 9, 21, 88, 74, 10, 32, 96, 45, 98, 39, 42, 9, 40, 48, 2, 56, 36, 7, 50, 52, 59, 98, 64, 52, 87, 54, 23, 64, 84, 18, 64, 92, 56, 40, 31, 47, 36, 80, 61, 27, 61, 35, 55, 34, 39, 46, 82, 42, 81, 35, 10, 54, 24, 84, 2, 11, 49]
    ics=[27, 48, 99, 54, 42, 43, 38, 96, 49, 81, 85, 63, 89, 46, 73, 3, 9, 3, 89, 89, 20, 32, 1, 92, 88, 71, 76, 47, 7, 32, 22, 66, 32, 26, 1, 94, 6, 58, 67, 37, 58, 94, 79, 1, 17, 1, 65, 61, 92, 57, 67, 60, 78, 23, 93, 58, 52, 82, 50, 24, 49, 42, 54, 21, 83, 70, 1, 53, 7, 5, 3, 26, 60, 98, 21, 71, 19, 36, 74, 50, 16, 97, 15, 24, 8, 78, 9, 67, 22, 41, 17, 11, 87, 25, 87, 89, 69, 4, 7, 27]
    
    # Gerando solução inicial s0 gulosa. Uma troca com o menor IC
    # Inicio com uma única troca
    troca = d519.randrange(0,len(ics)-1)
        
    # Monto a solucao de forma binaria
    s = [0]*len(ics)
    
    # Gerando a solução inicial: Aleatória ou Gulosa
    s[troca] = 1
    
    if debug:
        print 'Solução inicial:'
        print s
        print 'O IC da solucao inicial é %f' % (calculaValor(s))
        print 'O preco da solucao inicial é %d' % (calculaPeso(s))
    # busca local s com Best improvement
    s = buscaLocal(s)
    
    # Inicio loop ILS
    i = 0
    while i < iterMaxILS:
        #print 'Loop ILS %d' % (i)
        # Perturbacao: Gero um número n <= totalEquips e esta será a qte de trocas a ser feita
        n = d519.randrange(1,len(ics))
        perturbacao = [0]*len(ics)
        for j in range(0,n+1): # o segundo parametro pega ele -1. Se sao 6 equips, só iria pegar até o 5o
            perturbacao[j] = 1 # solucao qualquer pois buscaLocal irá cuidar disto
        
        #print n
        #print perturbacao        
        # Faço novamente buscaLocal
        temp = buscaLocal(perturbacao)
    
        # Restrição (caso o perturbacao gerado tenha sido o ganhador na buscaLocal)
        if calculaPeso(temp) > meuCusto:
            continue
        
        # Avalio o melhor
        if calculaValor(temp) > calculaValor(s):
            s = temp
            
        melhoresGeracao.append(calculaValor(s))
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
    #return [calculaValor(s, ics), calculaPeso(s, custos)]
    return melhoresGeracao
