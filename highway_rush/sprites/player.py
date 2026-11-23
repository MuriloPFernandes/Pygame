from pathlib import Path

import pygame

from config import (
    ALTURA,
    ALTURA_CARRO,
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


def mover_carro(carro, teclas, velocidade=VELOCIDADE_CARRO):
    # A velocidade pode ser menor quando o carro passa no óleo.
    if pygame.K_LEFT in teclas or pygame.K_a in teclas:
        carro.x -= velocidade
    if pygame.K_RIGHT in teclas or pygame.K_d in teclas:
        carro.x += velocidade
    if pygame.K_UP in teclas or pygame.K_w in teclas:
        carro.y -= velocidade
    if pygame.K_DOWN in teclas or pygame.K_s in teclas:
        carro.y += velocidade

    # Mantém o retângulo inteiro dentro da pista e da altura da janela.
    limites = pygame.Rect(PISTA_X, 0, LARGURA_PISTA, ALTURA)
    carro.clamp_ip(limites)


def carregar_imagem_carro(carro):
    caminho = Path(__file__).resolve().parents[1] / "assets" / "images" / "cars" / "player.png"
    imagem = pygame.image.load(caminho).convert_alpha()

    # Remove a margem transparente e preserva a proporção do sprite.
    imagem = imagem.subsurface(imagem.get_bounding_rect())
    tamanho = imagem.get_rect().fit(carro).size
    return pygame.transform.scale(imagem, tamanho)


def desenhar_carro(tela, carro, imagem):
    tela.blit(imagem, imagem.get_rect(center=carro.center))
