# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 14:25:41 2014

@author: victor

@todo Adicionar roleta genérico aqui pois vários algoritmos vão precisar
"""
import copy
from random import randrange
import mysql.connector
from scipy import stats as scistats
# Calcula a media geometrica dos valores
def calculaIc(solucao, icG):
    ics = copy.copy(icG) # evitar puxar por valor e alterar o valor global. Deixar local
    # Primeiro alterar quem esta em solucao para ic = 1
    for i in range(0,len(solucao)-1):
        if solucao[i] == 1:
            ics[i] = 1

    # Media geometrica
    return scistats.gmean(ics)
    
def calculaPreco(solucao, custos):
    preco = 0
    for i in range(0,len(solucao)-1):
        if solucao[i] == 1:
            preco = preco + custos[i]
    return preco