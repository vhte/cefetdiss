# -*- coding: utf-8 -*-
#    Copyright (C) 2010 Simon Wessing
#    TU Dortmund University
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#http://pythonhosted.org/inspyred/reference.html
# setcover metric - % um melhor que outra
import inspyred
import numpy as np 
import matplotlib as plt
from pylab import *
from copy import copy

# Qual grupo de nao-dominados
grupoNSGAII = 'multi_nsgaII_SED_'
grupoSPEA2 = 'multi_spea2_SED_'
# ic 0: NSGA-II 1: SPEA2
x = [[],[]]
# preco 0: NSGA-II 1: SPEA2
y = [[],[]]

for i in range(1,31):
    # Abrindo os NSGA-II
    with open(grupoNSGAII+str(i), 'r') as f:
        searchlines = f.readlines()
    for j,line in enumerate(searchlines):
        if "ic = " in line:
            exec(line)
        if "preco = " in line:
            exec(line)
    x[0] = x[0] + ic
    y[0] = y[0] + preco
    
    with open(grupoSPEA2+str(i), 'r') as f:
        searchlines = f.readlines()
    for j,line in enumerate(searchlines):
        if "ic = " in line:
            exec(line)
        if "custo = " in line:
            exec(line)

    x[1] = x[1] + ic
    y[1] = y[1] + custo

xReal = copy(x)
yReal = copy(y)
############################ Há 30x300(população/arquivo)
#print len(x[0])
i = 0
j = 0
y[0] = map(lambda d: d*(-1),y[0]) # Porque hypervolume do inspyred é para max()
y[1] = map(lambda d: d*(-1),y[1])

smetric = [[],[]] # 0 NSGA 1 SPEA
for i in range(0,30): # 9000 (30x300)
    # Cria combinação x e y de cada execução i
    c0 = zip(x[0][j:j+299],y[0][j:j+299])
    c1 = zip(x[1][j:j+299],y[1][j:j+299])
    
    j = j+300
    smetric[0].append(inspyred.ec.analysis.hypervolume(c0))
    smetric[1].append(inspyred.ec.analysis.hypervolume(c1))

data_to_plot = [smetric[0],smetric[1]]

# Create a figure instance
boxplot(data_to_plot)
#grid(True)
xticks([1, 2], ['NSGA-II', 'SPEA2'])

"""
frontNSGA = 1
frontSPEA = 1

referencePointNSGA = [16.7282,-614.12282223 ]
referencePointSPEA = [5,2836, -1078.5961772]
#AlimGra
#referencePoint = [10, 1205]
#AlimSED
#referencePoint = [460, 3135]
print inspyred.ec.analysis.hypervolume(frontNSGA)
print inspyred.ec.analysis.hypervolume(frontSPEA)
print len(frontNSGA)
"""

############ SET COVER METRIC ###########
# Pergunta: Entre[0,1] quantos pontos de NSGA são dominados por SPEA
cont = 0
for i in range(0,len(x[1])):
    print 'Verificando solucao %d/%d' % (i,len(x[1]))
    for j in range(0,len(x[0])):
        if x[1][i] >= x[0][j] and y[1][i] <= y[0][j]:
            cont = cont + 1
            break
res = cont/float(len(x[0]))
print 'C(SPEA2, NSGA-II) = %f' % (res)