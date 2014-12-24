#!/usr/bin/python

#
# Example boxplot code
#
from pylab import *
import mono_ils

# fake up some data
spread= rand(50) * 100
center = ones(25) * 50
flier_high = rand(10) * 100 + 100
flier_low = rand(10) * -100
#data =concatenate((spread, center, flier_high, flier_low), 0)
data_ic = []
data_custo = []
for i in range(0,30):
    tmp = mono_ils.ils()
    data_ic.append(tmp[0])
    data_custo.append(tmp[1])

print '--------------------'
# basic plot
title('IC')
bIc = boxplot(data_ic)
#print data_ic
posMaxIc = data_ic.index(max(data_ic))
print 'IC: %f' % max(data_ic)
print 'Custo: %f' % data_custo[posMaxIc]

figure(2)
title('Custo (US)')
bCusto = boxplot(data_custo)
print bIc['medians'][0].get_ydata()
print bCusto['medians'][0].get_ydata()
#print data_custo

show()