# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 20:37:08 2011

@author: Claudio
"""

from numpy import loadtxt
import csv

#arq_teste = 'teste.csv'
arq_treinamento = 'treinamento.csv'

with open(arq_treinamento, 'rb') as arq:
    cabecalhos = csv.reader(arq, delimiter=';').next()
    palavras = [palavra.strip('\'"') for palavra in cabecalhos]
    
palavras = zip(range(len(palavras)), palavras)

SPAM_OU_NAO = 0 # coluna onde as msgs estao classificadas como spam ou nao
#teste = loadtxt(arq_teste, skiprows=1, delimiter=';')
treinamento = loadtxt(arq_treinamento, skiprows=1, delimiter=';')

espaco_amostral = len(treinamento)
numero_de_spams = len([spam for spam in treinamento[:,SPAM_OU_NAO] if spam])

P_de_ser_spam = 1.0*numero_de_spams / espaco_amostral

P_da_palavra = {}
for linha in range(espaco_amostral):
    for coluna, palavra in palavras:
        if treinamento[linha,coluna] and treinamento[linha,SPAM_OU_NAO]:
            P_da_palavra[palavra] = P_da_palavra.get(palavra, 0) + 1

for palavra, F_da_palavra in P_da_palavra.items():
    P_da_palavra[palavra] = (1.0 * F_da_palavra / espaco_amostral) / P_de_ser_spam
    print palavra, P_da_palavra[palavra]

#prob_make_dado_spam = (1.0 * MAKE_num_spam / espaco_amostral) / P_de_ser_spam
