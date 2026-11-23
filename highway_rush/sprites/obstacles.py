# Obstáculos extras que aparecem na pista:
#   "pneu": pneu solto rolando. Bater nele tira uma vida, como bater num carro.
#   "oleo": mancha de óleo. Passar por cima deixa o carro lento por alguns segundos.
# Cada obstáculo é um dicionário com seu retângulo, tipo e informações de desenho.

import math
from random import choice, randint

import pygame

from config import (
    ALTURA,
    ALTURA_OLEO,
    COR_OLEO,
    LARGURA_OLEO,
    LARGURA_PISTA,
    PISTA_X,
    TAMANHO_PNEU,
    TIPOS_OBSTACULO,
)


def criar_obstaculo(ocupados):
    # Sorteia o tipo e uma posição no topo da pista.
    # "ocupados" são os retângulos de carros e itens que já estão na pista;
    # o obstáculo não pode nascer em cima deles, para nunca fechar a passagem.
    tipo = choice(TIPOS_OBSTACULO)
    if tipo == "pneu":
        largura = TAMANHO_PNEU
        altura = TAMANHO_PNEU
    else:
        largura = LARGURA_OLEO
        altura = ALTURA_OLEO

    # Tenta algumas posições. Se todas estiverem ocupadas, não cria nada desta vez.
    retangulo = None
    tentativas = 0
    while retangulo is None and tentativas < 10:
        tentativas += 1
        x = randint(PISTA_X, PISTA_X + LARGURA_PISTA - largura)
        candidato = pygame.Rect(x, -altura, largura, altura)
        # inflate deixa uma folga em volta, para o obstáculo não ficar colado em outro.
        livre = True
        for outro in ocupados:
            if candidato.inflate(30, 160).colliderect(outro):
                livre = False
        if livre:
            retangulo = candidato
    if retangulo is None:
        return None

    obstaculo = {"retangulo": retangulo, "tipo": tipo}
    if tipo == "pneu":
        obstaculo["vx"] = choice([-1, 1])  # o pneu escorrega um pouco para o lado
        obstaculo["giro"] = 0              # ângulo usado para desenhar o pneu girando
    else:
        # A mancha é feita de várias elipses sorteadas uma vez só,
        # assim cada mancha tem um formato diferente que não fica "piscando".
        manchas = []
        for i in range(5):
            w = randint(largura // 2, largura)
            h = randint(altura // 2, altura)
            dx = randint(0, largura - w)
            dy = randint(0, altura - h)
            manchas.append((dx, dy, w, h))
        obstaculo["manchas"] = manchas
    return obstaculo


def mover_obstaculos(obstaculos, velocidade_pista):
    # O óleo está parado no asfalto, então desce junto com a pista.
    # O pneu está rolando na nossa direção, então desce um pouco mais rápido.
    visiveis = []
    for obstaculo in obstaculos:
        retangulo = obstaculo["retangulo"]
        if obstaculo["tipo"] == "pneu":
            retangulo.y += velocidade_pista + 2
            retangulo.x += obstaculo["vx"]
            # Quando encosta na borda da pista, o pneu volta para o outro lado.
            if retangulo.left <= PISTA_X:
                obstaculo["vx"] = 1
            elif retangulo.right >= PISTA_X + LARGURA_PISTA:
                obstaculo["vx"] = -1
            obstaculo["giro"] += 8
        else:
            retangulo.y += velocidade_pista
        if retangulo.top < ALTURA:
            visiveis.append(obstaculo)
    return visiveis


def verificar_obstaculos(carro, obstaculos):
    # Devolve (obstáculos que continuam na pista, tipos em que o carro encostou).
    # O pneu some depois da batida; o óleo continua no chão.
    restantes = []
    atingidos = []
    for obstaculo in obstaculos:
        if carro.colliderect(obstaculo["retangulo"]):
            atingidos.append(obstaculo["tipo"])
            if obstaculo["tipo"] == "oleo":
                restantes.append(obstaculo)
        else:
            restantes.append(obstaculo)
    return restantes, atingidos


def desenhar_pneu(tela, obstaculo):
    centro = obstaculo["retangulo"].center
    raio = TAMANHO_PNEU // 2
    pygame.draw.circle(tela, (25, 25, 25), centro, raio)             # borracha
    # Pontinhos da banda de rodagem: giram conforme o pneu rola.
    for i in range(8):
        angulo = math.radians(i * 45 + obstaculo["giro"])
        x = centro[0] + math.cos(angulo) * (raio - 4)
        y = centro[1] + math.sin(angulo) * (raio - 4)
        pygame.draw.circle(tela, (70, 70, 70), (int(x), int(y)), 2)
    pygame.draw.circle(tela, (160, 160, 165), centro, raio // 2)     # aro de metal
    pygame.draw.circle(tela, (90, 90, 95), centro, raio // 4)        # centro da roda


def desenhar_oleo(tela, obstaculo):
    retangulo = obstaculo["retangulo"]
    # Parte escura da mancha.
    for dx, dy, w, h in obstaculo["manchas"]:
        pygame.draw.ellipse(tela, (15, 15, 20), (retangulo.x + dx, retangulo.y + dy, w, h))
    # Brilho colorido, como o reflexo do óleo no asfalto.
    brilho = pygame.Rect(0, 0, retangulo.width // 3, retangulo.height // 4)
    brilho.center = (retangulo.centerx - 8, retangulo.centery - 4)
    pygame.draw.ellipse(tela, COR_OLEO, brilho)
    brilho.move_ip(16, 8)
    pygame.draw.ellipse(tela, (60, 120, 160), brilho)


def desenhar_obstaculos(tela, obstaculos, tipo):
    # Desenha só os obstáculos de um tipo. Assim o jogo pode desenhar o óleo
    # embaixo de tudo e os pneus por cima da pista.
    for obstaculo in obstaculos:
        if obstaculo["tipo"] != tipo:
            continue
        if tipo == "pneu":
            desenhar_pneu(tela, obstaculo)
        else:
            desenhar_oleo(tela, obstaculo)
