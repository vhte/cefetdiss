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
def ils():
    ########### PARAMETROS #################
    # Número máximo de iterações no loop princpal do ILS.
    iterMaxILS = 10
    # Número máximo de iterações na busca local. 10% do tamanho da populacao
    # Isto fará com que chegue uma hora em que a restrição monetária não suporte nenhuma outra solução
    iterMaxBL = 10
    # Numero de vizinhanças diferentes (vizinhancas é a qte de trocas de equips, primeira vizinhanca só 1 troca)
    vizinhancas = 5
    # Limite de dinheiro que possuo
    meuCusto = 300
    
    ################ METODOS ###############
        
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
            if d519.calculaPreco(s0, custos) > meuCusto:
                continue
            
            # Se sim, entao verifico qual tem IC melhor
            # Usar >= aqui pode implicar em loop infinito quando muito próximo do ótimo
            if d519.calculaIc(s0, ics) > d519.calculaIc(solucaoCorrente, ics):
                i=0 #reseto a iteração
                solucaoCorrente = s0 # nova solução corrente
    
        return solucaoCorrente #[0]*len(solucaoCorrente)
        
    ################# MAIN #################
    
    # Buscando os Equips (ICs)
    cnx = d519.mysql.connector.connect(user='root', password='root', database='cemig_d519')
    cursor = cnx.cursor()
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
    #ics = [0.6512, 0.3541, 0.6985, 0.5896, 0.7445, 0.4565, 0.9546, 0.5164, 0.1238]
    
    #custos = [500, 300, 550, 500, 200, 310, 100, 580, 800]
    
    # Gerando solução inicial s0 gulosa. Uma troca com o menor IC
    # Inicio com uma única troca
    troca = d519.randrange(0,len(ics)-1)
        
    # Monto a solucao de forma binaria
    s = [0]*len(ics)
    
    # Aloco a primeira troca aleatória
    s[troca] = 1
    
    print 'Solução inicial:'
    print s
    print 'O IC da solucao inicial é %f' % (d519.calculaIc(s, ics))
    print 'O preco da solucao inicial é %d' % (d519.calculaPreco(s, custos))
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
        if d519.calculaPreco(temp, custos) > meuCusto:
            continue
        
        # Avalio o melhor
        if d519.calculaIc(temp, ics) > d519.calculaIc(s, ics):
            s = temp
        i = i+1
        
    print 'Solução final'
    print s
    print 'O IC da solucao final é %f' % (d519.calculaIc(s, ics))
    print 'O preco da solucao final é %f' % (d519.calculaPreco(s, custos))
    
    # Enquanto o critério de parada não for satisfeito
        # Perturbacao
        # Busca local na perturbacao
        # Verificar se s' melhor que s
    
    # Retorna resultado final
    
    # Fecha as conexões
    cursor.close()
    cnx.close()
    
    return [d519.calculaIc(s, ics), d519.calculaPreco(s, custos)]
    #return d519.calculaPreco(s, custos)
    #return d519.calculaIc(s, ics)