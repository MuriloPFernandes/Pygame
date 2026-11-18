# Highway Rush - arquivo principal
# Abre a janela e roda o loop do jogo.

import pygame
from config import LARGURA, ALTURA, FPS, TITULO, PRETO

pygame.init()

window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

clock = pygame.time.Clock()

# Loop principal
game = True
while game:
    clock.tick(FPS)  # mantém o jogo em 60 quadros por segundo

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # clicou no X da janela
            game = False

    # Desenho
    window.fill(PRETO)
    pygame.display.update()

pygame.quit()
