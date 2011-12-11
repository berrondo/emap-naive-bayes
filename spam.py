# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 20:37:08 2011

@authors: Claudio, Debora, Gerson, Diego
"""

import csv
from numpy import loadtxt


class Relatorio:
    ACERTOS_EM_SPAM = 0
    ACERTOS_EM_NAO_SPAM = 0
    
    def __init__(self, total_de_mensagens, numero_de_spams):
        self.total_de_mensagens = total_de_mensagens
        self.numero_de_spams = numero_de_spams
        self.numero_de_nao_spams = total_de_mensagens - numero_de_spams

    acertou = "ACERTOU!"
    errou = "errou..."
    def __call__(self, Spam, r):
        msg = ""
        if Spam:
            if r >= 1.0:
                msg = self.acertou
                self.ACERTOS_EM_SPAM += 1
            else:
                msg = self.errou
        if not Spam:
            if r < 1.0:
                msg = self.acertou
                self.ACERTOS_EM_NAO_SPAM += 1
            else:
                msg = self.errou
        return "%s %s %s" % (msg, Spam, r)
        
    def __str__(self):
        msg = "\n"
        msg += "em um total de %s mensagens:\n" % self.total_de_mensagens
        msg += "%s acertos e %s erros em %s spams (%.2f%% correto)\n" % (
                                                    self.ACERTOS_EM_SPAM, 
                                                    self.numero_de_spams-self.ACERTOS_EM_SPAM, 
                                                    self.numero_de_spams, 
                                                    (1.0*self.ACERTOS_EM_SPAM / self.numero_de_spams) * 100)
        msg += "%s acertos e %s erros em %s NAO spams (%.2f%% correto)\n" % (
                                                    self.ACERTOS_EM_NAO_SPAM, 
                                                    self.numero_de_nao_spams-self.ACERTOS_EM_NAO_SPAM, 
                                                    self.numero_de_nao_spams, 
                                                    (1.0*self.ACERTOS_EM_NAO_SPAM / self.numero_de_nao_spams) * 100)
        return msg


class Palavra:
    def __init__(self, palavra, coluna):
        self.palavra = palavra.strip('\'"')
        self.coluna = coluna
        self.em_spam = 0
        self.em_nao_spam = 0

    @property
    def P_em_spam(self):
        return (1.0 * self.em_spam / espaco_amostral) / P_de_ser_spam
        
    @property
    def P_em_nao_spam(self):
        return (1.0 * self.em_nao_spam / espaco_amostral) / P_de_nao_ser_spam
        
        
# arquivos csv para treinamento e teste:
arq_teste = 'teste.csv'
arq_treinamento = 'treinamento.csv'

# obtendo do cabecalho as palavras:
with open(arq_treinamento, 'rb') as arq:
    palavras = [Palavra(palavra, n) for n, palavra in enumerate(csv.reader(arq, delimiter=';').next())]

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
for linha in range(espaco_amostral):
    for palavra in palavras:
        
        # se a palavra esta presente...
        if treinamento[linha,palavra.coluna]:
            # em um spam...
            if treinamento[linha,SPAM]:
                palavra.em_spam += 1
            # ou nao spam:
            else:
                palavra.em_nao_spam += 1

                
                
# obtendo dados para classificar:  
teste = loadtxt(arq_teste, skiprows=1, delimiter=';')
total_de_mensagens_no_teste = len(teste)
numero_de_spams_no_teste = list(teste[:,SPAM]).count(1.0)

acertou = Relatorio(total_de_mensagens_no_teste, numero_de_spams_no_teste)

# para cada mensagem,
for linha in range(total_de_mensagens_no_teste):
    Produtorio_spam = 1.0
    Produtorio_nao_spam = 1.0

    # para cada palavra...
    for palavra in palavras[1:]:
        # ...presente na mensagem...
        if teste[linha,palavra.coluna]:
            # ...multiplica suas probabilidades para spam e nao spam:
            Produtorio_spam *= palavra.P_em_spam
            Produtorio_nao_spam *= palavra.P_em_nao_spam

    # em cada linha/mensagem, levando em conta as palavras...
    P_spam_dado_palavras = Produtorio_spam * P_de_ser_spam
    P_nao_spam_dado_palavras = Produtorio_nao_spam * P_de_nao_ser_spam
    
    # ...calcula razao entre ser ou nao ser spam:
    r = P_spam_dado_palavras / P_nao_spam_dado_palavras
    
    # acertou?
    print linha, acertou(teste[linha,SPAM], r)

# relatorio final:
print acertou
