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
    iterMaxILS = 500
    # Número máximo de iterações na busca local. 10% do tamanho da populacao
    # Isto fará com que chegue uma hora em que a restrição monetária não suporte nenhuma outra solução
    iterMaxBL = 20
    iterMaxBL_P = 0.01 # Quantas posições serão afetadas, em porcentagem, da solução corrente
    # Limite de dinheiro que possuo
    meuCusto = 1500
    
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
        i = 0
        while i < iterMaxBL:
            i = i+1
            
            # Encontrando um vizinho k qualquer
            s0 = d519.copy.deepcopy(solucaoCorrente)
            
            j = 0
            while j < int(len(ics)*iterMaxBL_P):
                # Mudo uma posicao
                pos = d519.randrange(0,len(s0))
                while s0[pos]:
                    pos = d519.randrange(0,len(s0))
    
                s0[pos] = True
                
                j = j+1
            
            # RESTRIÇÃO: Verificando se a soma das trocas são válidas
            if calculaPeso(s0) > meuCusto:
                continue
            
            # Se sim, entao verifico qual tem IC melhor
            # Usar >= aqui pode implicar em loop infinito quando muito próximo do ótimo
            if calculaValor(s0) > calculaValor(solucaoCorrente):
                i=0 #reseto a iteração
                solucaoCorrente = d519.copy.deepcopy(s0) # nova solução corrente
    
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
    
    meuCusto=15000
    custos=[57, 72, 51, 96, 82, 61, 65, 66, 53, 82, 61, 70, 54, 83, 66, 89, 83, 66, 52, 52, 54, 85, 62, 72, 87, 89, 68, 50, 71, 57, 73, 85, 58, 77, 75, 99, 71, 55, 84, 59, 82, 97, 99, 53, 73, 62, 93, 63, 89, 59, 84, 54, 93, 71, 78, 55, 69, 67, 57, 91, 82, 60, 78, 64, 54, 86, 66, 73, 56, 71, 87, 58, 53, 95, 92, 94, 53, 78, 72, 82, 74, 68, 55, 74, 82, 59, 68, 66, 64, 93, 76, 92, 88, 76, 54, 97, 78, 82, 60, 63, 84, 95, 58, 89, 77, 96, 89, 76, 77, 54, 79, 70, 98, 53, 76, 94, 79, 83, 63, 71, 99, 77, 64, 98, 52, 87, 50, 80, 51, 67, 56, 62, 62, 52, 51, 84, 89, 79, 52, 53, 57, 74, 92, 79, 84, 95, 55, 87, 76, 69, 90, 71, 79, 50, 68, 57, 96, 73, 63, 96, 80, 93, 72, 80, 88, 71, 73, 77, 99, 56, 76, 87, 58, 56, 52, 94, 83, 63, 68, 89, 60, 90, 78, 51, 68, 57, 79, 73, 57, 56, 83, 57, 57, 75, 77, 60, 70, 87, 87, 99, 54, 88, 80, 86, 74, 96, 84, 87, 82, 80, 82, 52, 99, 62, 77, 50, 52, 58, 90, 80, 80, 64, 82, 61, 70, 54, 82, 66, 70, 82, 90, 62, 69, 75, 69, 78, 50, 71, 81, 71, 95, 58, 69, 96, 51, 78, 70, 75, 87, 95, 87, 81, 67, 66, 72, 98, 73, 60, 97, 97, 70, 97, 54, 56, 69, 73, 85, 90, 89, 80, 93, 79, 63, 67, 99, 73, 74, 93, 94, 53, 65, 79, 65, 56, 78, 94, 60, 86, 64, 65, 75, 67, 85, 56, 99, 87, 92, 78, 74, 58, 55, 94, 89, 98, 84, 71, 53, 80, 52, 52, 51, 70, 57, 56, 84, 98, 60, 57, 89, 63, 51, 54, 77, 96, 92, 62, 64, 62, 75, 90, 71, 88, 55, 66, 72, 66, 71, 60, 93, 80, 96, 63, 92, 86, 60, 77, 57, 65, 67, 86, 78, 59, 65, 98, 81, 66, 90, 61, 94, 84, 52, 55, 66, 60, 65, 79, 76, 88, 95, 66, 65, 92, 62, 75, 99, 63, 92, 97, 97, 72, 90, 87, 64, 87, 68, 86, 72, 66, 82, 90, 76, 68, 55, 56, 83, 50, 83, 90, 67, 83, 56, 83, 87, 55, 73, 90, 53, 94, 54, 50, 62, 75, 98, 77, 96, 81, 78, 95, 52, 69, 94, 51, 53, 72, 72, 78, 68, 60, 97, 67, 77, 60, 88, 85, 73, 85, 65, 88, 56, 51, 73, 66, 75, 83, 91, 60, 56, 99, 81, 53, 50, 72, 94, 61, 54, 67, 63, 65, 73, 50, 85, 73, 70, 86, 59, 61, 57, 52, 66, 70, 90, 96, 53, 95, 50, 94, 73, 58, 71, 74, 90, 90, 61, 98, 93, 84, 69, 83, 62, 83, 77, 99, 52, 74, 86, 50, 85, 51, 55, 58]
    ics=[164, 835, 881, 190, 440, 785, 685, 80, 630, 192, 649, 220, 538, 625, 722, 43, 587, 863, 183, 907, 616, 278, 485, 997, 208, 513, 951, 512, 699, 241, 772, 460, 79, 247, 527, 942, 993, 520, 566, 837, 749, 133, 835, 175, 751, 644, 331, 287, 903, 268, 758, 790, 345, 915, 287, 432, 38, 630, 347, 628, 915, 266, 652, 785, 240, 713, 946, 634, 253, 323, 949, 47, 685, 981, 493, 634, 418, 856, 866, 693, 159, 830, 501, 104, 59, 377, 732, 336, 666, 298, 673, 822, 36, 734, 68, 245, 629, 688, 723, 83, 363, 77, 103, 188, 700, 286, 33, 355, 716, 59, 427, 308, 735, 698, 266, 998, 259, 686, 865, 798, 16, 868, 551, 912, 97, 54, 614, 794, 714, 772, 316, 461, 387, 609, 41, 655, 936, 38, 998, 976, 41, 607, 930, 726, 593, 82, 654, 631, 36, 323, 120, 843, 823, 932, 240, 172, 15, 333, 559, 801, 753, 457, 408, 986, 46, 259, 620, 642, 782, 15, 955, 179, 230, 407, 660, 904, 532, 204, 485, 473, 219, 672, 888, 586, 492, 888, 500, 846, 489, 730, 539, 977, 559, 135, 46, 322, 417, 357, 237, 646, 95, 891, 17, 6, 785, 832, 850, 574, 512, 2, 854, 698, 79, 35, 395, 924, 108, 323, 666, 86, 168, 427, 847, 166, 218, 421, 655, 929, 885, 281, 535, 805, 839, 509, 899, 783, 237, 515, 634, 724, 201, 354, 891, 108, 526, 181, 957, 582, 397, 364, 558, 900, 679, 530, 53, 718, 906, 909, 963, 909, 957, 404, 996, 119, 968, 633, 21, 36, 52, 266, 466, 121, 82, 918, 538, 269, 625, 21, 858, 905, 41, 437, 358, 550, 294, 960, 417, 807, 24, 631, 80, 8, 170, 112, 801, 421, 856, 504, 203, 507, 361, 782, 378, 250, 617, 500, 663, 171, 267, 721, 288, 317, 344, 560, 693, 401, 188, 155, 423, 921, 341, 215, 439, 309, 320, 832, 770, 544, 138, 47, 480, 49, 464, 21, 133, 778, 133, 917, 105, 581, 234, 652, 942, 599, 355, 195, 206, 57, 186, 896, 543, 83, 259, 951, 84, 602, 696, 51, 788, 82, 256, 816, 210, 627, 618, 634, 49, 691, 305, 812, 952, 900, 635, 229, 835, 685, 828, 372, 666, 531, 958, 980, 744, 146, 446, 937, 918, 426, 359, 808, 237, 518, 376, 47, 971, 851, 447, 545, 211, 965, 230, 859, 83, 892, 247, 957, 779, 816, 144, 464, 182, 957, 964, 364, 919, 824, 352, 870, 410, 396, 547, 799, 737, 532, 506, 813, 57, 317, 871, 734, 947, 301, 738, 222, 587, 351, 534, 614, 922, 693, 885, 312, 344, 178, 294, 382, 322, 173, 577, 280, 127, 502, 359, 879, 543, 385, 276, 55, 494, 186, 100, 886, 497, 335, 521, 891, 622, 95, 617, 360, 413, 903, 72, 6, 331, 746, 684, 354, 325, 642, 191, 871, 327, 148, 503, 264, 424, 864, 946, 558, 657, 357, 727, 228, 339, 440, 819, 978, 129, 814]
        
    # Perturbacao: x% da solucao
    p = int(len(ics)*0.01)
    
    # Monto a solucao de forma binaria
    s = [False]*len(ics)
    
    # Gerando a solução inicial: Aleatória ou Gulosa. Nao posso permitir que a solucao inicial extrapole muito a restricao, senao a perturbacao nunca encontrara uma solucao factivel
    """
    # Aleatório
    aleatorio = int(len(ics)*0.25)
    for i in range(0,aleatorio):
        pos = d519.randrange(0,len(s))
        while s[pos]:
            pos = d519.randrange(0,len(s))
        s[pos] = True
    """ 
    # Guloso
    for i in range(0,len(ics)):
        if ics[i]/float(custos[i]) > 15:
            s[i] = True
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
        perturbacao = d519.copy.deepcopy(s)
        for j in range(0,p): # o segundo parametro pega ele -1. Se sao 6 equips, só iria pegar até o 5o
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
            continue
        
        # Avalio o melhor
        if calculaValor(temp) > calculaValor(s):
            s = d519.copy.deepcopy(temp)
            
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
