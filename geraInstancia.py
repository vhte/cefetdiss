# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 17:13:27 2015

Gera instancia para o knapsack
@author: victor
"""
from random import randrange

V = []
M = []
n = 100
for i in range(0,n):
    V.append(randrange(1,1000))
    M.append(randrange(50,100))
    
print V
print M