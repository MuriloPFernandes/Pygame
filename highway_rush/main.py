# Highway Rush - arquivo principal
# Abre a janela e alterna entre as telas: menu, corrida e Game Over.

import pygame

from config import ALTURA, LARGURA, TITULO
from screens.game import tela_jogo
from screens.game_over import tela_game_over
from screens.menu import tela_menu

pygame.init()

window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

clock = pygame.time.Clock()

# "estado" guarda em qual tela o jogo está: "menu", "jogo", "fim" ou "sair".
estado = "menu"
dificuldade = None
pontuacao = 0
recorde = 0  # maior pontuação desde que o programa foi aberto

while estado != "sair":
    if estado == "menu":
        dificuldade = tela_menu(window, clock)
        if dificuldade is None:
            estado = "sair"
        else:
            estado = "jogo"

    elif estado == "jogo":
        pontuacao = tela_jogo(window, clock, dificuldade)
        if pontuacao is None:
            estado = "sair"
        else:
            if pontuacao > recorde:
                recorde = pontuacao
            estado = "fim"

    elif estado == "fim":
        # A tela de Game Over devolve o próximo estado ("jogo", "menu" ou "sair").
        estado = tela_game_over(window, clock, pontuacao, recorde, dificuldade)

pygame.quit()
