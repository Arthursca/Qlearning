import os.path
import random

from connection import connect, get_state_reward

alpha = 0.5
gamma = 0.4
estado = "0000000"


class EscreveArquivo:
    def pegaMatrix(self):
        matrix = []
        with open(os.path.dirname(__file__) + '/resultado.txt') as arquivo:
            lines = arquivo.readlines()
            for (index, line) in enumerate(lines):
                values = line.replace('\n', '').split(' ')
                plataforma = [round(float(values[0]), 6), round(float(values[1]), 6), round(float(values[2]), 6)]
                matrix.append(plataforma)

            return matrix

    @staticmethod
    def coloca_matrix(matrix):
        with open(os.path.dirname(__file__) + '/resultado.txt', "r+") as text_file:
            text_file.truncate(0)

            text = ''
            for plataforma in matrix:
                text += str(round(plataforma[0], 6)) + ' ' + str(round(plataforma[1], 6)) + ' ' + str(round(plataforma[2], 6)) + '\n'

            text_file.write(text)


class ProximoPasso:
    @staticmethod
    def daProximoPasso(acao):
        global estado
        escreve = EscreveArquivo()
        matrix = escreve.pegaMatrix()
        q_max = 0

        estado_anterior = estado

        estado_atual, recompensa = get_state_reward(conecta, acao)

        plataforma_anterior = str(int(estado_anterior[:-2], 2))
        plataforma_atual = str(int(estado_atual[:-2], 2))

        linha_anterior = (int(plataforma_anterior) + 1) * 4 - (int(estado_anterior[-2:]) % 4)
        linha_atual = (int(plataforma_atual) + 1) * 4 - (int(estado_atual[-2:]) % 4)

        for i, line in enumerate(matrix):
            if i == linha_atual - 1:
                q_max = max(line[0], line[1], line[2])
                break

        for i, line in enumerate(matrix):
            if i == linha_anterior - 1:
                if acao == 'left':
                    line[0] = line[0] + alpha * ((recompensa + gamma * q_max) - line[0])
                if acao == 'right':
                    line[1] = line[1] + alpha * ((recompensa + gamma * q_max) - line[1])
                else:
                    line[2] = line[2] + alpha * ((recompensa + gamma * q_max) - line[2])
                break

        estado = estado_atual

        escreve.coloca_matrix(matrix)


if __name__ == '__main__':
    conecta = connect(2037)

    # extrai a informação do estado p/ ação e recompensa pós ação
    estado, recompensa = get_state_reward(conecta, "jump")
    proximo_passo = ProximoPasso

    while True:
        acao = ''
        elemento_aleatorio_acao = random.randint(1,3)
        if elemento_aleatorio_acao == 1:
            acao += 'left'
        elif elemento_aleatorio_acao == 2:
            acao += 'right'
        else:
            acao += 'jump'

        proximo_passo.daProximoPasso(acao)
