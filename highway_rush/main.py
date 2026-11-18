# Highway Rush - arquivo principal
# Abre a janela e roda o loop do jogo.

from random import randint

import pygame
from config import LARGURA, ALTURA, FPS, TITULO
from config import INTERVALO_MIN_ADVERSARIO, INTERVALO_MAX_ADVERSARIO
from sprites.enemy import criar_adversario, desenhar_adversarios, mover_adversarios
from sprites.player import carregar_imagem_carro, criar_carro, desenhar_carro, mover_carro
from sprites.road import desenhar_pista, atualizar_faixas

pygame.init()

window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

clock = pygame.time.Clock()
deslocamento_faixas = 0
carro = criar_carro()
imagem_carro = carregar_imagem_carro(carro)
adversarios = []
quadros_ate_adversario = INTERVALO_MIN_ADVERSARIO

# Loop principal
game = True
while game:
    clock.tick(FPS)  # mantém o jogo em 60 quadros por segundo

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # clicou no X da janela
            game = False

    mover_carro(carro, pygame.key.get_pressed())

    # Depois de cada chegada, sorteia quantos quadros faltam para a próxima.
    quadros_ate_adversario -= 1
    if quadros_ate_adversario == 0:
        adversarios.append(criar_adversario())
        quadros_ate_adversario = randint(INTERVALO_MIN_ADVERSARIO, INTERVALO_MAX_ADVERSARIO)

    adversarios = mover_adversarios(adversarios)

    # A pista é desenhada antes do carro para ele aparecer por cima.
    desenhar_pista(window, deslocamento_faixas)
    desenhar_adversarios(window, adversarios)
    desenhar_carro(window, carro, imagem_carro)
    pygame.display.update()
    deslocamento_faixas = atualizar_faixas(deslocamento_faixas)

pygame.quit()
