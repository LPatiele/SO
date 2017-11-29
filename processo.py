# -*- coding: utf-8 -*-
from random import randint

def randonProcessos(qtdProcessos):
    # listas de prioridade
    processos = []
    for i in range(qtdProcessos):
        processos.insert(i,Processo("P"+str(i), randint(1,4), randint(1,5), 0, randint(0,1), randint(1,3),randint(1,10)))
    return processos

class Processo(object):

    def __init__(self, nome, prioridade, burst, cpu, tipo, chegada, memoria):
        self.nome       = nome
        self.prioridade = prioridade
        self.burst      = burst

        self.cpu        = cpu           # tempo de burst em que já esteve no CPU
        self.tipo       = tipo          # identifica se o processo é IO bound (0) ou CPU bound(1)
        self.chegada    = chegada       # indentifica o tempo de chegada do processo
        self.memoria    = memoria       # indica o espaço em memóra necessário

    def burstRestante(self):
        return self.burst - self.cpu

    def substituiPorNome(self):
        return self.nome
