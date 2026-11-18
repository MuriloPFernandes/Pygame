# Highway Rush - arquivo principal
# Abre a janela e roda o loop do jogo.

import pygame
from config import LARGURA, ALTURA, FPS, TITULO
from sprites.road import desenhar_pista, atualizar_faixas

pygame.init()

window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

clock = pygame.time.Clock()
deslocamento_faixas = 0

# Loop principal
game = True
while game:
    clock.tick(FPS)  # mantém o jogo em 60 quadros por segundo

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # clicou no X da janela
            game = False

    # Desenho
    desenhar_pista(window, deslocamento_faixas)
    pygame.display.update()
    deslocamento_faixas = atualizar_faixas(deslocamento_faixas)

pygame.quit()
