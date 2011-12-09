# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 20:37:08 2011

@authors: Claudio, Debora, Gerson, Diego
"""

import csv
from numpy import loadtxt

# arquivos csv para treinamento e teste:
arq_teste = 'teste.csv'
arq_treinamento = 'treinamento.csv'

# obtendo do cabecalho as palavras:
with open(arq_treinamento, 'rb') as arq:
    cabecalhos = csv.reader(arq, delimiter=';').next()
    
palavras = [palavra.strip('\'"') for palavra in cabecalhos]
palavras = zip(range(len(palavras)), palavras)

# coluna onde as msgs estao classificadas como spam ou nao:
SPAM = 0

# obtendo os dados para treinamento como um ndarray:
treinamento = loadtxt(arq_treinamento, skiprows=1, delimiter=';')

# tamanho do espaco amostral e quantidade de spams:
espaco_amostral = len(treinamento)
numero_de_spams = list(treinamento[:,SPAM]).count(1.0)

# probabilidades de ser e nao ser spam:
P_de_ser_spam = 1.0*numero_de_spams / espaco_amostral
P_de_nao_ser_spam = 1.0 - P_de_ser_spam

# contando as palavras:
P_em_spam = {}
P_em_nao_spam = {}
for linha in range(espaco_amostral):
    for coluna, palavra in palavras:
        
        # se a palavra esta presente...
        if treinamento[linha,coluna]:
            # em um spam...
            if treinamento[linha,SPAM]:
                P_em_spam[palavra] = P_em_spam.get(palavra, 0) + 1
            # ou nao spam:
            else:
                P_em_nao_spam[palavra] = P_em_nao_spam.get(palavra, 0) + 1           

# calculando as probabilidades para cada palavra:
for palavra, N_da_palavra in P_em_spam.items():
    P_em_spam[palavra] = (1.0 * N_da_palavra / espaco_amostral) / P_de_ser_spam
    
for palavra, N_da_palavra in P_em_nao_spam.items():
    P_em_nao_spam[palavra] = (1.0 * N_da_palavra / espaco_amostral) / P_de_nao_ser_spam


def acertou(linha, Spam, r):
    if (r > 1.0 and Spam) or (r < 1.0 and not Spam):
        print "ACERTOU!",
    else:
        print "errou...",
    print linha, Spam, r

# obtendo dados para classificar:  
teste = loadtxt(arq_teste, skiprows=1, delimiter=';')

for linha in range(len(teste)):
    Produtorio_spam = 1.0
    Produtorio_nao_spam = 1.0

    for coluna, palavra in palavras[1:]:
        # se a palavra esta presente...
        if teste[linha,coluna]:
            Produtorio_spam *= P_em_spam[palavra]
            Produtorio_nao_spam *= P_em_nao_spam[palavra]

    # totaliza para cada linha/mensagem:
    P_spam_dado_palavras = Produtorio_spam * P_de_ser_spam
    P_nao_spam_dado_palavras = Produtorio_nao_spam * P_de_nao_ser_spam
    
    # razao entre ser ou nao ser spam:
    r = P_spam_dado_palavras / P_nao_spam_dado_palavras
    acertou(linha, teste[linha,0], r)
