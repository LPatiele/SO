# -*- coding: utf-8 -*-
from processo import *
import copy


if __name__ == '__main__':

    #Gera os processos aleatóriamente... passa como parametro o numero de processos que quer gerar
    listaProcessos = randonProcessos(3)
    
    # Escreve o txt com os processos que foram gerados aleatoriamente
    f = open('processos.txt', 'w')
    for p in listaProcessos:
        f.write("--------" + p.nome + "--------\n")
        f.write("Tempo de chegada = " + str(p.chegada) + "\n")
        f.write("Tempo de burst = " + str(p.burst) + "\n")
        f.write("Memória requerida = " + str(p.memoria) + "\n")
        f.write("Prioridade inicial = " + str(p.prioridade) + "\n\n")
        
    # Filas de prioridade
    prioridade4 = [] # tempo de quantum 1
    prioridade3 = [] # tempo de quantum 2
    prioridade2 = [] # tempo de quantum 4
    prioridade1 = [] # tempo de quantum 8

    # Fila de bloqueados... nesse caso estou utilizando a estrutura de dicionários para manipular o tempo de cada processo na fila
    bloqueados = {}

    #Escalonador
    a = open('escalonamento.txt', 'w')
    tempo = 0  # Marcas os quantuns de tempo
    cpu = [] 
    memoriaDisponivel = 100

    while listaProcessos:
        tempo = tempo + 1 
        
        # print do quantum de tempo atual
        print "--------------Quantum " + str(tempo)+"-----------------" 
        a.write("--------------Quantum " + str(tempo)+"-----------------\n")

        # trata a fila de bloqueados
        desbloquear= []
        for p in bloqueados.keys():
            bloqueados[p] = bloqueados[p] - 1
            if bloqueados[p] <= 0:   # verifica se o processo sai da fila de bloqueados 
                desbloquear.append(p)  
                if p.memoria > memoriaDisponivel:  # reinsere o processo no proximo quantum se não houver memória suficiente
                    for d in listaProcessos:
                        if d.nome == p.nome: 
                            p.chegada = tempo + 1
                            d = p  # substitui as alteraçõe da cópia do processo em bloqueados para o processo original
                else:                               # reinsere o processo se houver memória suficiente
                    memoriaDisponivel = memoriaDisponivel - p.memoria
                    if p.prioridade == 4:
                        prioridade4.append(copy.copy(p))
                        prioridade4.sort(key=Processo.burstRestante)
                    elif p.prioridade == 3:
                        prioridade3.append(copy.copy(p))
                        prioridade3.sort(key=Processo.burstRestante)   
                    elif p.prioridade == 2:
                        prioridade2.append(copy.copy(p))
                        prioridade2.sort(key=Processo.burstRestante)
                    else:
                        prioridade1.append(copy.copy(p))
        for p in desbloquear:
            del bloqueados[p]             

        # adicionando nas filas os processos que acabaram de chegar
        for p in listaProcessos:
            if p.chegada == tempo:
                if p.memoria > memoriaDisponivel:
                    p.chegada = p.chegada + 1
                else:
                    memoriaDisponivel = memoriaDisponivel - p.memoria
                    if p.prioridade == 4:
                        prioridade4.append(copy.copy(p))
                        prioridade4.sort(key=Processo.burstRestante)
                    elif p.prioridade == 3:
                        prioridade3.append(copy.copy(p))
                        prioridade3.sort(key=Processo.burstRestante)   
                    elif p.prioridade == 2:
                        prioridade2.append(copy.copy(p))
                        prioridade2.sort(key=Processo.burstRestante)
                    else:
                        prioridade1.append(copy.copy(p))
                        prioridade1.sort(key=Processo.burstRestante) 
        
        # insere processo no cpu se não houver nenhum
        if not cpu:  
            if prioridade4:
                cpu = [copy.copy(prioridade4[0]),3]
                prioridade4.pop(0)
            elif prioridade3:
                cpu = [copy.copy(prioridade3[0]),2]
                prioridade3.pop(0)
            elif prioridade2:
                cpu = [copy.copy(prioridade2[0]),1]
                prioridade2.pop(0)
            elif prioridade1:
                cpu = [copy.copy(prioridade1[0]),0]
                prioridade1.pop(0)

        # print do processo que foi processado nesse quantum  
        if cpu:      
            print "Processo no cpu = " + cpu[0].nome
            a.write("Processo no cpu = " + cpu[0].nome + "\n")
        else:
            print "Processo no cpu = " 
            a.write("Processo no cpu = \n")

        # print da memória disponivel
        print "Memória disponivel = " + str(memoriaDisponivel)
        a.write("Memória disponivel = " + str(memoriaDisponivel) + "\n")

        # print das filas de prioridade
        printar = ""
        for p in prioridade4:
            printar = printar + p.nome + "  "
        print "Fila de prioridade 4 =" + printar
        a.write("Fila de prioridade 4 =" + printar + "\n")
        printar = ""
        for p in prioridade3:
            printar = printar + p.nome + "  "
        print "Fila de prioridade 3 =" + printar
        a.write("Fila de prioridade 3 =" + printar + "\n")
        printar = ""
        for p in prioridade2:
            printar = printar + p.nome + "  "
        print "Fila de prioridade 2 =" + printar
        a.write("Fila de prioridade 2 =" + printar + "\n")
        printar = ""
        for p in prioridade1:
            printar = printar + p.nome + "  "
        print "Fila de prioridade 1 =" + printar
        a.write("Fila de prioridade 1 =" + printar + "\n")

        # se existe ou foi inserido algo no cpu manipula o processo que estiver no cpu   
        if cpu:
            cpu[0].cpu = cpu[0].cpu + 1          # Incrementa o tempo de cpu do processo
            # verifica se o processo foi totalmente execultado
            if cpu[0].burst == cpu[0].cpu:       
                for p in listaProcessos:
                    if p.nome == cpu[0].nome:
                        memoriaDisponivel = memoriaDisponivel + p.memoria
                        listaProcessos.remove(p) # Exclui o processo que foi encerrado nessa iteração se houver
                        cpu = []
                        break
            else:
                if cpu[1] == 0: # verifica se acabou o tempo de processamento do processo
                    if cpu[0].tipo == 1:  # verifica se o processo é CPU bound
                        if cpu[0].prioridade <= 1:   # se a prioridade estiver baixa
                            cpu[0].tipo = 0          # torna o processo CPU bound em IO bound
                            #reinsere em uma das filas de prioridade
                            if cpu[0].prioridade == 4:
                                prioridade4.append(copy.copy(cpu[0]))
                                prioridade4.sort(key=Processo.burstRestante)
                            elif cpu[0].prioridade == 3:
                                prioridade3.append(copy.copy(cpu[0]))
                                prioridade3.sort(key=Processo.burstRestante)   
                            elif cpu[0].prioridade == 2:
                                prioridade2.append(copy.copy(cpu[0]))
                                prioridade2.sort(key=Processo.burstRestante)
                            else:
                                prioridade1.append(copy.copy(cpu[0]))
                                prioridade4.sort(key=Processo.burstRestante)
                        else:
                            cpu[0].prioridade = cpu[0].prioridade - 1   # decrementa a prioridade do processo CPU bound
                            #reinsere em uma das filas de prioridade
                            if cpu[0].prioridade == 4:
                                prioridade4.append(copy.copy(cpu[0]))
                                prioridade4.sort(key=Processo.burstRestante)
                            elif cpu[0].prioridade == 3:
                                prioridade3.append(copy.copy(cpu[0]))
                                prioridade3.sort(key=Processo.burstRestante)   
                            elif cpu[0].prioridade == 2:
                                prioridade2.append(copy.copy(cpu[0]))
                                prioridade2.sort(key=Processo.burstRestante)
                            else:
                                prioridade1.append(copy.copy(cpu[0]))
                                prioridade4.sort(key=Processo.burstRestante)
                    else: # o processo é IO bound
                        if cpu[0].prioridade >= 4:   # se a prioridade estiver alta
                            cpu[0].tipo = 1          # torna o processo IO bound em CPU bound
                            #reinsere em uma das filas de prioridade
                            if cpu[0].prioridade == 4:
                                prioridade4.append(copy.copy(cpu[0]))
                                prioridade4.sort(key=Processo.burstRestante)
                            elif cpu[0].prioridade == 3:
                                prioridade3.append(copy.copy(cpu[0]))
                                prioridade3.sort(key=Processo.burstRestante)   
                            elif cpu[0].prioridade == 2:
                                prioridade2.append(copy.copy(cpu[0]))
                                prioridade2.sort(key=Processo.burstRestante)
                            else:
                                prioridade1.append(copy.copy(cpu[0]))
                                prioridade4.sort(key=Processo.burstRestante)
                        else:
                            if randint(0,1) == 0: # Joga alguns processos aleatóriamente na fila de bloqueados
                                bloqueados[copy.copy(cpu[0])] = randint(1,4) 
                            else:
                                #reinsere em uma das filas de prioridade
                                if cpu[0].prioridade == 4:
                                    prioridade4.append(copy.copy(cpu[0]))
                                    prioridade4.sort(key=Processo.burstRestante)
                                elif cpu[0].prioridade == 3:
                                    prioridade3.append(copy.copy(cpu[0]))
                                    prioridade3.sort(key=Processo.burstRestante)   
                                elif cpu[0].prioridade == 2:
                                    prioridade2.append(copy.copy(cpu[0]))
                                    prioridade2.sort(key=Processo.burstRestante)
                                else:
                                    prioridade1.append(copy.copy(cpu[0]))
                                    prioridade4.sort(key=Processo.burstRestante)
                    cpu = []
                else: 
                    # se o tempo de processamento não terminou
                    cpu[1] = cpu[1] - 1           # Decrementa o tempo de processamento restante do processo
                
      
        # print da fila de bloqueados
        printar = ""
        for p in bloqueados.keys():
            printar = printar + p.nome + "  "
        print "Fila de bloqueados = " + printar
        a.write("Fila de bloqueados = " + printar + "\n")

        # print de processos ainda não concluidos
        printar = ""
        for p in listaProcessos:
            printar = printar + p.nome + "  "
        print "Lista de processos não concluidos = " + printar
        a.write("Lista de processos não concluidos = " + printar + "\n\n")

        f.close
        a.close
            

   
