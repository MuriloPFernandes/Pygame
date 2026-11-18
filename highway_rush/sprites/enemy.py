from pathlib import Path
from random import choice, randint

import pygame

from config import (
    ALTURA,
    ALTURA_CARRO,
    LARGURA_CARRO,
    LARGURA_PISTA,
    PISTA_X,
    VELOCIDADE_ADVERSARIO,
)


def carregar_imagens_adversarios():
    pasta = Path(__file__).resolve().parents[1] / "assets" / "images" / "cars"
    nomes = ("SuperB.png", "BuickerB.png", "GalardB.png", "JeepB.png")
    limites = pygame.Rect(0, 0, LARGURA_CARRO, ALTURA_CARRO)
    imagens = []
    for nome in nomes:
        imagem = pygame.image.load(pasta / nome).convert_alpha()
        imagem = imagem.subsurface(imagem.get_bounding_rect())
        # Vira a frente do carro para a direção em que ele desce na pista.
        imagem = pygame.transform.rotate(imagem, 180)
        tamanho = imagem.get_rect().fit(limites).size
        imagens.append(pygame.transform.scale(imagem, tamanho))
    return imagens


def criar_adversario(imagens):
    # Desconta a largura do carro para ele nascer inteiro sobre o asfalto.
    x_maximo = PISTA_X + LARGURA_PISTA - LARGURA_CARRO
    x = randint(PISTA_X, x_maximo)
    carro = pygame.Rect(x, -ALTURA_CARRO, LARGURA_CARRO, ALTURA_CARRO)
    return carro, choice(imagens)


def mover_adversarios(adversarios, velocidade=VELOCIDADE_ADVERSARIO):
    # A velocidade vem da dificuldade escolhida no menu.
    visiveis_ou_entrando = []
    for carro, imagem in adversarios:
        carro.y += velocidade
        # Quando o topo chega ao fim da janela, o carro já saiu por inteiro.
        if carro.top < ALTURA:
            visiveis_ou_entrando.append((carro, imagem))
    return visiveis_ou_entrando


def remover_adversarios_colididos(carro_jogador, adversarios):
    restantes = []
    for carro, imagem in adversarios:
        if not carro_jogador.colliderect(carro):
            restantes.append((carro, imagem))
    return restantes


def desenhar_adversarios(tela, adversarios):
    for carro, imagem in adversarios:
        tela.blit(imagem, imagem.get_rect(center=carro.center))
