# Power-ups que aparecem na pista e dão um efeito temporário ao jogador.
#   "dobro": pontuação em dobro
#   "lento": câmera lenta (os carros e a pista ficam mais devagar)

from random import choice, randint

import pygame

from config import ALTURA, AMARELO, AZUL, BRANCO, LARGURA_PISTA, PISTA_X, PRETO, TAMANHO_POWERUP

TIPOS_POWERUP = ("dobro", "lento")
CORES_POWERUP = {"dobro": AMARELO, "lento": AZUL}
TEXTOS_POWERUP = {"dobro": "2x", "lento": "S"}


def criar_powerup():
    x = randint(PISTA_X, PISTA_X + LARGURA_PISTA - TAMANHO_POWERUP)
    retangulo = pygame.Rect(x, -TAMANHO_POWERUP, TAMANHO_POWERUP, TAMANHO_POWERUP)
    return retangulo, choice(TIPOS_POWERUP)


def mover_powerups(powerups, velocidade):
    # Os power-ups estão "parados" na pista, então descem junto com as faixas.
    visiveis = []
    for retangulo, tipo in powerups:
        retangulo.y += velocidade
        if retangulo.top < ALTURA:
            visiveis.append((retangulo, tipo))
    return visiveis


def coletar_powerups(carro, powerups):
    # Devolve (power-ups que sobraram, tipos que o jogador pegou).
    restantes = []
    coletados = []
    for retangulo, tipo in powerups:
        if carro.colliderect(retangulo):
            coletados.append(tipo)
        else:
            restantes.append((retangulo, tipo))
    return restantes, coletados


def desenhar_powerups(tela, powerups, fonte, contador_quadros):
    # Um leve "pulsar" ajuda o jogador a notar o item na pista.
    pulso = 2 if (contador_quadros // 10) % 2 == 0 else 0
    for retangulo, tipo in powerups:
        raio = TAMANHO_POWERUP // 2
        pygame.draw.circle(tela, BRANCO, retangulo.center, raio + pulso)
        pygame.draw.circle(tela, CORES_POWERUP[tipo], retangulo.center, raio - 3)
        texto = fonte.render(TEXTOS_POWERUP[tipo], True, PRETO)
        tela.blit(texto, texto.get_rect(center=retangulo.center))
