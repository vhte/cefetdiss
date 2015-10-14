# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 12:50:54 2015

@author: victor
"""
import matplotlib.pyplot as plt
# Qual grupo de nao-dominados
grupoNSGAII = 'multi_nsgaII_GRA_'
grupoSPEA2 = 'multi_spea2_GRA_'
# ic 0: NSGA-II 1: SPEA2
x = [[],[]]
# preco 0: NSGA-II 1: SPEA2
y = [[],[]]

eliminar = [[],[]] # quem é dominado 0: NSGA-II 1: SPEA2
xs = [[],[]]
ys = [[],[]] # respostas

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

############################    
# Achando os não dominados
for i in range(0,len(x[0])):
    print i
    if i in eliminar[0]:
        continue
    for j in range(i+1,len(x[0])):
        if x[0][i] > x[0][j] and y[0][i] < y[0][j]:
            if j not in eliminar[0]:
                eliminar[0].append(j)
            continue
        if x[0][i] < x[0][j] and y[0][i] > y[0][j]:
            if i not in eliminar[0]:
                eliminar[0].append(i)
            break
            
for i in range(0,len(x[0])):
    if i not in eliminar[0]:
        xs[0].append(x[0][i])
        ys[0].append(y[0][i])
#############################
for i in range(0,len(x[1])):
    print i
    if i in eliminar[1]:
        continue
    for j in range(i+1,len(x[1])):
        if x[1][i] > x[1][j] and y[1][i] < y[1][j]:
            if j not in eliminar[1]:
                eliminar[1].append(j)
            continue
        if x[1][i] < x[1][j] and y[1][i] > y[1][j]:
            if i not in eliminar[1]:
                eliminar[1].append(i)
            break
            
for i in range(0,len(x[1])):
    if i not in eliminar[1]:
        xs[1].append(x[1][i])
        ys[1].append(y[1][i])


plt.plot(xs[0], ys[0], 'r+', label='NSGA-II', alpha=1)
plt.plot(xs[1], ys[1], 'b_', label='SPEA2', alpha=1)

"""
# AlimPeq Obj0
plt.plot(35.7361,98.325, 'm*',label='mono_ilsCONV',alpha=1)
plt.plot(36.1217,98.454, 'mv',label='mono_agCONV',alpha=1)
plt.plot(35.5559,96.951, 'm^',label='mono_acoCONV',alpha=1)

plt.plot(35.9889,99.485, 'gx',label='mono_ilsAVAL',alpha=1)
plt.plot(35.9868,99.584, 'gs',label='mono_agAVAL',alpha=1)
plt.plot(35.4704,97.298, 'go',label='mono_acoAVAL',alpha=1)
"""

"""
# AlimPeq Obj1
plt.plot(19.488,26.4979, 'm*',label='mono_ilsCONV',alpha=1)
plt.plot(19.256,26.6167, 'mv',label='mono_agCONV',alpha=1)
plt.plot(18.489,32.0824, 'm^',label='mono_acoCONV',alpha=1)

plt.plot(19.889,25.9725, 'gx',label='mono_ilsAVAL',alpha=1)
plt.plot(19.415,26.4580, 'gs',label='mono_agAVAL',alpha=1)
plt.plot(18.031,32.1694, 'go',label='mono_acoAVAL',alpha=1)
"""

"""
# AlimGra Obj0
plt.plot(57.3992,148.498, 'm*',label='mono_ilsCONV',alpha=1)
plt.plot(63.5019,149.321, 'mv',label='mono_agCONV',alpha=1)
plt.plot(57.1112,148.752, 'm^',label='mono_acoCONV',alpha=1)

plt.plot(57.7308,149.159, 'gx',label='mono_ilsAVAL',alpha=1)
plt.plot(57.8078,149.484, 'gs',label='mono_agAVAL',alpha=1)
plt.plot(57.3007,148.985, 'go',label='mono_acoAVAL',alpha=1)
"""
# AlimGra Obj1
plt.plot(55.3992,112.2897, 'm*',label='mono_ilsCONV',alpha=1)
plt.plot(55.5019,111.7414, 'mv',label='mono_agCONV',alpha=1)
plt.plot(57.1112,154.1631, 'm^',label='mono_acoCONV',alpha=1)

plt.plot(55.7308,110.0784, 'gx',label='mono_ilsAVAL',alpha=1)
plt.plot(55.8078,114.9827, 'gs',label='mono_agAVAL',alpha=1)
plt.plot(57.3007,144.1426, 'go',label='mono_acoAVAL',alpha=1)

#plt.axis([0, len(Y)+1, 0, max(Y)+max(Y)*0.1])
plt.legend(loc='best')
plt.xlabel('$\sum (1-IC)$')
plt.ylabel('$\sum Custo$')
plt.grid()
plt.show()
print 'NSGA-II'
print xs[0]
print ys[0]

print 'SPEA2'
print xs[1]
print ys[1]

print '-----'

print min(xs[0])
print max(ys[0]) 
print min(xs[1])
print max(ys[1])

ys[0] = map(lambda d: d*(-1),ys[0])
ys[1] = map(lambda d: d*(-1),ys[1])
c = zip(xs[1],ys[1])
print c