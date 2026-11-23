# Highway Rush - arquivo principal
# Abre a janela e alterna entre as telas: menu, corrida e Game Over.

import pygame

from config import ALTURA, LARGURA, TITULO
from screens.game import tela_jogo
from screens.game_over import tela_game_over
from screens.menu import tela_menu
from screens.nome import tela_nome
from ranking import carregar_ranking, salvar_ranking

pygame.init()

window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

clock = pygame.time.Clock()

# "estado" guarda a tela atual: "menu", "nome", "jogo", "fim" ou "sair".
estado = "menu"
dificuldade = None
pontuacao = 0
recorde = 0  # maior pontuação desde que o programa foi aberto
aviso_ranking = ""
pode_salvar = True
try:
    resultados = carregar_ranking()
except (OSError, ValueError):
    # Preserva o arquivo original caso ele não possa ser lido.
    resultados = []
    pode_salvar = False
    aviso_ranking = "Ranking indisponível: resultados só nesta sessão."

while estado != "sair":
    if estado == "menu":
        dificuldade = tela_menu(window, clock, resultados, aviso_ranking)
        if dificuldade is None:
            estado = "sair"
        else:
            estado = "nome"

    elif estado == "nome":
        nome = tela_nome(window, clock, dificuldade, resultados)
        if nome is None:
            estado = "sair"
        elif nome == "":
            estado = "menu"
        else:
            estado = "jogo"

    elif estado == "jogo":
        pontuacao = tela_jogo(window, clock, dificuldade)
        if pontuacao is None:
            estado = "sair"
        else:
            novo_recorde = pontuacao > recorde
            if pontuacao > recorde:
                recorde = pontuacao
            resultados.append({"nome": nome, "pontos": pontuacao, "dificuldade": dificuldade})
            indice_partida = len(resultados) - 1
            if pode_salvar:
                try:
                    salvar_ranking(resultados)
                    aviso_ranking = ""
                except OSError:
                    aviso_ranking = "Não foi possível salvar: resultado só nesta sessão."
            estado = "fim"

    elif estado == "fim":
        # A tela de Game Over devolve o próximo estado ("jogo", "menu" ou "sair").
        estado = tela_game_over(window, clock, pontuacao, recorde, dificuldade,
                                resultados, indice_partida, novo_recorde, aviso_ranking)
        if estado == "jogo":
            estado = "nome"

pygame.quit()
