import pygame

from config import (
    ALTURA,
    BRANCO,
    COMPRIMENTO_FAIXA,
    COR_ASFALTO,
    COR_GRAMA,
    ESPACO_ENTRE_FAIXAS,
    LARGURA,
    LARGURA_PISTA,
    VELOCIDADE_PISTA,
)


def atualizar_faixas(deslocamento):
    # As faixas se repetem a cada traço mais o espaço até o próximo.
    ciclo = COMPRIMENTO_FAIXA + ESPACO_ENTRE_FAIXAS
    return (deslocamento + VELOCIDADE_PISTA) % ciclo


def desenhar_pista(tela, deslocamento):
    esquerda = (LARGURA - LARGURA_PISTA) // 2
    direita = esquerda + LARGURA_PISTA
    largura_linha = 4
    ciclo = COMPRIMENTO_FAIXA + ESPACO_ENTRE_FAIXAS

    tela.fill(COR_GRAMA)
    pygame.draw.rect(tela, COR_ASFALTO, (esquerda, 0, LARGURA_PISTA, ALTURA))
    pygame.draw.rect(tela, BRANCO, (esquerda, 0, largura_linha, ALTURA))
    pygame.draw.rect(tela, BRANCO, (direita - largura_linha, 0, largura_linha, ALTURA))

    # Os traços começam acima da tela para entrar pelo topo sem saltos.
    for divisor in (1, 2):
        x = esquerda + divisor * LARGURA_PISTA // 3 - largura_linha // 2
        for y in range(deslocamento - ciclo, ALTURA, ciclo):
            pygame.draw.rect(tela, BRANCO, (x, y, largura_linha, COMPRIMENTO_FAIXA))
