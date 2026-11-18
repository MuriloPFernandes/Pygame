import pygame

from config import (
    ALTURA,
    ALTURA_CARRO,
    COR_CARRO,
    LARGURA_CARRO,
    LARGURA_PISTA,
    MARGEM_INFERIOR_CARRO,
    PISTA_X,
    VELOCIDADE_CARRO,
)


def criar_carro():
    carro = pygame.Rect(0, 0, LARGURA_CARRO, ALTURA_CARRO)
    carro.centerx = PISTA_X + LARGURA_PISTA // 2
    carro.bottom = ALTURA - MARGEM_INFERIOR_CARRO
    return carro


def mover_carro(carro, teclas):
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        carro.x -= VELOCIDADE_CARRO
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        carro.x += VELOCIDADE_CARRO
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        carro.y -= VELOCIDADE_CARRO
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        carro.y += VELOCIDADE_CARRO

    # Mantém o retângulo inteiro dentro da pista e da altura da janela.
    limites = pygame.Rect(PISTA_X, 0, LARGURA_PISTA, ALTURA)
    carro.clamp_ip(limites)


def desenhar_carro(tela, carro):
    pygame.draw.rect(tela, COR_CARRO, carro)
