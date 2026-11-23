# Efeitos visuais: fumaça do carro danificado, explosão do carro destruído,
# estilhaços da batida no pneu e respingos/pingos de óleo.
# Todos os efeitos são feitos de "partículas": pequenos círculos guardados em
# dicionários, que se movem, crescem ou encolhem e somem depois de um tempo.

import math
from random import choice, randint

import pygame

from config import AMARELO, BRANCO, COR_OLEO, FUMACA_CLARA, FUMACA_ESCURA, LARANJA, VERMELHO


def criar_fumaca(carro, vidas):
    # Quanto menos vidas, mais escura e mais grossa é a fumaça.
    if vidas >= 2:
        cor = FUMACA_CLARA
        raio = randint(5, 8)
    else:
        cor = FUMACA_ESCURA
        raio = randint(7, 11)

    # A fumaça sai do motor, na metade de trás do carro.
    return {
        "x": carro.centerx + randint(-6, 6),
        "y": carro.centery + randint(0, 20),
        "vx": randint(-10, 10) / 10,
        "vy": 0,
        "raio": raio,
        "crescimento": 0.3,
        "vida": 40,
        "vida_maxima": 40,
        "cor": cor,
    }


def criar_fumaca_destruido(carro):
    # Fumaça preta e grossa saindo do carro destruído, subindo devagar.
    return {
        "x": carro.centerx + randint(-12, 12),
        "y": carro.centery + randint(-20, 20),
        "vx": randint(-10, 10) / 10,
        "vy": -1,
        "raio": randint(8, 12),
        "crescimento": 0.5,
        "vida": 60,
        "vida_maxima": 60,
        "cor": FUMACA_ESCURA,
    }


def criar_chama(carro):
    # Pequenas chamas que continuam queimando no carro destruído.
    vida = randint(12, 22)
    return {
        "x": carro.centerx + randint(-12, 12),
        "y": carro.centery + randint(-25, 25),
        "vx": 0,
        "vy": -1,
        "raio": randint(4, 8),
        "crescimento": -0.2,
        "vida": vida,
        "vida_maxima": vida,
        "cor": choice([AMARELO, LARANJA, VERMELHO]),
    }


def criar_explosao(centro_x, centro_y):
    # Muitas partículas de fogo saindo do centro em todas as direções.
    particulas = []
    for i in range(80):
        angulo = math.radians(randint(0, 359))
        velocidade = randint(20, 100) / 10
        vida = randint(35, 70)
        particulas.append({
            "x": centro_x,
            "y": centro_y,
            "vx": math.cos(angulo) * velocidade,
            "vy": math.sin(angulo) * velocidade,
            "raio": randint(8, 16),
            "crescimento": -0.12,  # o fogo vai diminuindo
            "vida": vida,
            "vida_maxima": vida,
            "cor": choice([AMARELO, LARANJA, VERMELHO, BRANCO]),
        })
    return particulas


def criar_estilhacos_pneu(centro_x, centro_y):
    # Batida no pneu: pedaços de borracha voando e algumas faíscas.
    particulas = []
    for i in range(20):
        angulo = math.radians(randint(0, 359))
        if i < 12:
            # Pedaços de borracha: escuros e um pouco maiores.
            cor = choice([(30, 30, 30), (60, 60, 60)])
            raio = randint(3, 5)
            velocidade = randint(20, 50) / 10
            vida = randint(20, 35)
        else:
            # Faíscas: claras, pequenas e rápidas.
            cor = choice([AMARELO, BRANCO])
            raio = randint(2, 3)
            velocidade = randint(40, 70) / 10
            vida = randint(10, 18)
        particulas.append({
            "x": centro_x,
            "y": centro_y,
            "vx": math.cos(angulo) * velocidade,
            "vy": math.sin(angulo) * velocidade,
            "raio": raio,
            "crescimento": -0.08,
            "vida": vida,
            "vida_maxima": vida,
            "cor": cor,
        })
    return particulas


def criar_respingo_oleo(centro_x, centro_y):
    # Quando o carro entra no óleo, gotas escuras espirram para os lados.
    particulas = []
    for i in range(10):
        angulo = math.radians(randint(0, 359))
        velocidade = randint(15, 40) / 10
        vida = randint(15, 25)
        particulas.append({
            "x": centro_x,
            "y": centro_y,
            "vx": math.cos(angulo) * velocidade,
            "vy": math.sin(angulo) * velocidade,
            "raio": randint(2, 4),
            "crescimento": 0,
            "vida": vida,
            "vida_maxima": vida,
            "cor": choice([(20, 20, 25), COR_OLEO]),
        })
    return particulas


def criar_pingos_oleo(carro):
    # Enquanto escorrega, as rodas de trás espirram pingos de óleo para os lados:
    # a roda da esquerda joga para a esquerda e a da direita para a direita.
    pingos = []
    for x, direcao in ((carro.left + 4, -1), (carro.right - 4, 1)):
        vida = randint(15, 25)
        pingos.append({
            "x": x,
            "y": carro.centery + 18,
            "vx": direcao * randint(10, 25) / 10,
            "vy": -randint(5, 15) / 10,
            "raio": randint(2, 3),
            "crescimento": 0,
            "vida": vida,
            "vida_maxima": vida,
            "cor": choice([(20, 20, 25), COR_OLEO]),
        })
    return pingos


def atualizar_particulas(particulas, velocidade_pista):
    # Move todas as partículas e devolve só as que ainda não sumiram.
    restantes = []
    for p in particulas:
        p["x"] += p["vx"] + randint(-1, 1)    # o randint faz a partícula tremer um pouco
        p["y"] += p["vy"] + velocidade_pista  # a pista "leva" a partícula para trás
        p["vx"] *= 0.9                        # vai freando aos poucos
        p["vy"] *= 0.9
        p["raio"] += p["crescimento"]
        p["vida"] -= 1
        if p["vida"] > 0 and p["raio"] > 1:
            restantes.append(p)
    return restantes


def desenhar_particulas(tela, particulas):
    for p in particulas:
        # A partícula fica mais transparente conforme a vida acaba.
        transparencia = int(220 * p["vida"] / p["vida_maxima"])
        raio = int(p["raio"])
        cor = (p["cor"][0], p["cor"][1], p["cor"][2], transparencia)

        # Para desenhar com transparência, usamos uma superfície pequena com SRCALPHA.
        circulo = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(circulo, cor, (raio, raio), raio)
        tela.blit(circulo, (p["x"] - raio, p["y"] - raio))


def queimar_imagem(imagem):
    # Cria uma versão escurecida do carro, para parecer carbonizado.
    queimada = imagem.copy()
    queimada.fill((70, 60, 55), special_flags=pygame.BLEND_RGB_MULT)
    return queimada
