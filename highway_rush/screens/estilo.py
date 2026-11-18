# Funções de desenho usadas pelo menu e pela tela de Game Over,
# para as duas telas terem o mesmo visual.

import pygame

from config import BRANCO, LARGURA, PRETO


def escrever(tela, texto, fonte, cor, centro_y, sombra=True):
    # Desenha um texto centralizado na horizontal.
    # A sombra é o mesmo texto em preto, um pouco deslocado para baixo e para a direita.
    if sombra:
        imagem_sombra = fonte.render(texto, True, PRETO)
        tela.blit(imagem_sombra, imagem_sombra.get_rect(center=(LARGURA // 2 + 3, centro_y + 3)))
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, imagem.get_rect(center=(LARGURA // 2, centro_y)))


def desenhar_painel(tela, retangulo, cor_borda):
    # Painel escuro e transparente, com cantos arredondados e borda colorida.
    fundo = pygame.Surface(retangulo.size, pygame.SRCALPHA)
    pygame.draw.rect(fundo, (10, 10, 15, 190), fundo.get_rect(), border_radius=18)
    tela.blit(fundo, retangulo.topleft)
    pygame.draw.rect(tela, cor_borda, retangulo, 3, border_radius=18)


def desenhar_xadrez(tela, x, y, largura):
    # Faixa quadriculada, como a bandeira de chegada de uma corrida.
    tamanho = 10
    for linha in range(2):
        for coluna in range(largura // tamanho):
            if (linha + coluna) % 2 == 0:
                cor = BRANCO
            else:
                cor = PRETO
            pygame.draw.rect(tela, cor, (x + coluna * tamanho, y + linha * tamanho, tamanho, tamanho))


def desenhar_tecla(tela, fonte, tecla, texto, cor_texto, centro_y):
    # Desenha uma "teclinha" com o nome da tecla e, ao lado, o que ela faz.
    imagem_tecla = fonte.render(tecla, True, PRETO)
    imagem_texto = fonte.render(texto, True, cor_texto)

    largura_caixa = imagem_tecla.get_width() + 16
    largura_total = largura_caixa + 10 + imagem_texto.get_width()
    x = LARGURA // 2 - largura_total // 2

    caixa = pygame.Rect(x, centro_y - 14, largura_caixa, 28)
    pygame.draw.rect(tela, BRANCO, caixa, border_radius=6)
    tela.blit(imagem_tecla, imagem_tecla.get_rect(center=caixa.center))
    tela.blit(imagem_texto, imagem_texto.get_rect(midleft=(caixa.right + 10, centro_y)))
