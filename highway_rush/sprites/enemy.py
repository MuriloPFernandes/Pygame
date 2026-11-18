from random import randint

import pygame

from config import (
    ALTURA,
    ALTURA_CARRO,
    COR_ADVERSARIO,
    LARGURA_CARRO,
    LARGURA_PISTA,
    PISTA_X,
    VELOCIDADE_ADVERSARIO,
)


def criar_adversario():
    # Desconta a largura do carro para ele nascer inteiro sobre o asfalto.
    x_maximo = PISTA_X + LARGURA_PISTA - LARGURA_CARRO
    x = randint(PISTA_X, x_maximo)
    return pygame.Rect(x, -ALTURA_CARRO, LARGURA_CARRO, ALTURA_CARRO)


def mover_adversarios(adversarios):
    visiveis_ou_entrando = []
    for adversario in adversarios:
        adversario.y += VELOCIDADE_ADVERSARIO
        # Quando o topo chega ao fim da janela, o carro já saiu por inteiro.
        if adversario.top < ALTURA:
            visiveis_ou_entrando.append(adversario)
    return visiveis_ou_entrando


def desenhar_adversarios(tela, adversarios):
    for adversario in adversarios:
        pygame.draw.rect(tela, COR_ADVERSARIO, adversario)
