# Tela de menu: título animado, trânsito passando no fundo e escolha da dificuldade.

import math
from pathlib import Path
from random import choice, randint

import pygame

from config import (
    ALTURA_CARRO,
    AMARELO,
    BRANCO,
    CINZA,
    DIFICULDADES,
    FPS,
    LARGURA,
    LARGURA_CARRO,
    LARGURA_PISTA,
    PISTA_X,
    PRETO,
)
from screens.estilo import desenhar_painel, desenhar_tecla, desenhar_xadrez, escrever
from sprites.enemy import carregar_imagens_adversarios, desenhar_adversarios, mover_adversarios
from sprites.player import carregar_imagem_carro, criar_carro, desenhar_carro
from sprites.road import atualizar_faixas, desenhar_pista


def tocar_musica_menu():
    # Só toca se o arquivo existir, assim o menu funciona mesmo sem a música.
    caminho = Path(__file__).resolve().parents[1] / "assets" / "sounds" / "music" / "menu.wav"
    if pygame.mixer.get_init() and caminho.exists():
        pygame.mixer.music.load(str(caminho))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


def desenhar_barra(tela, fonte, nome, fracao, y):
    # Desenha "nome [■■■■■□□□]" para mostrar o quanto a dificuldade é intensa.
    texto = fonte.render(nome, True, CINZA)
    tela.blit(texto, texto.get_rect(midleft=(90, y)))
    fracao = min(fracao, 1)
    pygame.draw.rect(tela, (40, 40, 45), (210, y - 7, 170, 14), border_radius=7)                # fundo
    pygame.draw.rect(tela, AMARELO, (210, y - 7, int(170 * fracao), 14), border_radius=7)       # preenchimento


def desenhar_opcao_escolhida(tela, fonte, nome, y, tempo):
    # Faixa amarela atrás do nome e duas setas que "empurram" para dentro.
    destaque = pygame.Rect(0, 0, 220, 40)
    destaque.center = (LARGURA // 2, y)
    pygame.draw.rect(tela, AMARELO, destaque, border_radius=10)
    escrever(tela, nome, fonte, PRETO, y, sombra=False)

    movimento = int(4 * math.sin(tempo / 150))
    esquerda = destaque.left - 14 + movimento
    direita = destaque.right + 14 - movimento
    pygame.draw.polygon(tela, AMARELO, [(esquerda, y - 9), (esquerda + 10, y), (esquerda, y + 9)])
    pygame.draw.polygon(tela, AMARELO, [(direita, y - 9), (direita - 10, y), (direita, y + 9)])


def criar_carro_fundo(imagens):
    # Os carros do fundo só passam nas faixas da esquerda e da direita,
    # para não atravessar o carro do jogador, que fica no meio.
    faixa = choice([0, 2])
    centro_x = PISTA_X + LARGURA_PISTA * (2 * faixa + 1) // 6
    carro = pygame.Rect(0, -ALTURA_CARRO, LARGURA_CARRO, ALTURA_CARRO)
    carro.centerx = centro_x
    return carro, choice(imagens)


def tela_menu(tela, clock):
    # Devolve o nome da dificuldade escolhida, ou None se a janela for fechada.
    fonte_titulo = pygame.font.Font(None, 88)
    fonte_opcao = pygame.font.Font(None, 44)
    fonte_texto = pygame.font.Font(None, 26)
    fonte_tecla = pygame.font.Font(None, 28)
    fonte_pequena = pygame.font.Font(None, 22)

    opcoes = list(DIFICULDADES.keys())  # ["Fácil", "Médio", "Difícil"]
    escolhida = 1  # começa em "Médio"

    # Carro do jogador parado no meio da pista, como no começo da corrida.
    carro = criar_carro()
    imagem_carro = carregar_imagem_carro(carro)

    # Trânsito de fundo, usando as mesmas imagens dos adversários do jogo.
    imagens_adversarios = carregar_imagens_adversarios()
    carros_fundo = []
    quadros_ate_carro = 30
    deslocamento_faixas = 0

    painel = pygame.Rect(50, 30, 380, 580)

    tocar_musica_menu()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    escolhida = (escolhida - 1) % len(opcoes)  # sobe e volta pro fim
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    escolhida = (escolhida + 1) % len(opcoes)  # desce e volta pro começo
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    pygame.mixer.music.stop()
                    return opcoes[escolhida]

        # O fundo anda na velocidade da dificuldade selecionada,
        # assim o jogador já sente a diferença antes de começar.
        config = DIFICULDADES[opcoes[escolhida]]

        quadros_ate_carro -= 1
        if quadros_ate_carro <= 0:
            carros_fundo.append(criar_carro_fundo(imagens_adversarios))
            quadros_ate_carro = randint(config["intervalo_min"], config["intervalo_max"])
        carros_fundo = mover_adversarios(carros_fundo, config["velocidade_adversario"])
        deslocamento_faixas = atualizar_faixas(deslocamento_faixas, config["velocidade_pista"])

        # ----- Fundo -----
        desenhar_pista(tela, deslocamento_faixas)
        desenhar_adversarios(tela, carros_fundo)
        desenhar_carro(tela, carro, imagem_carro)
        desenhar_painel(tela, painel, AMARELO)
        desenhar_xadrez(tela, 70, 44, 340)

        # ----- Título (sobe e desce devagar) -----
        tempo = pygame.time.get_ticks()
        balanco = int(5 * math.sin(tempo / 300))
        escrever(tela, "HIGHWAY", fonte_titulo, BRANCO, 110 + balanco)
        escrever(tela, "RUSH", fonte_titulo, AMARELO, 168 + balanco)
        escrever(tela, "Desvie do trânsito e vá longe!", fonte_texto, CINZA, 216)
        pygame.draw.line(tela, CINZA, (90, 240), (390, 240))

        # ----- Opções de dificuldade -----
        escrever(tela, "DIFICULDADE", fonte_pequena, CINZA, 262)
        for i, nome in enumerate(opcoes):
            y = 300 + i * 46
            if i == escolhida:
                desenhar_opcao_escolhida(tela, fonte_opcao, nome, y, tempo)
            else:
                escrever(tela, nome, fonte_opcao, BRANCO, y)

        # ----- Detalhes da dificuldade escolhida -----
        escrever(tela, config["descricao"], fonte_texto, BRANCO, 436)
        desenhar_barra(tela, fonte_texto, "Velocidade", config["velocidade_adversario"] / 8, 466)
        desenhar_barra(tela, fonte_texto, "Trânsito", 30 / config["intervalo_min"], 492)
        pygame.draw.line(tela, CINZA, (90, 516), (390, 516))

        # ----- Instruções -----
        # O ENTER pisca: aparece meio segundo, some meio segundo.
        if tempo // 500 % 2 == 0:
            desenhar_tecla(tela, fonte_tecla, "ENTER", "começar corrida", AMARELO, 538)
        desenhar_tecla(tela, fonte_pequena, "SETAS / WASD", "dirigir", CINZA, 568)
        desenhar_xadrez(tela, 70, 586, 340)

        pygame.display.update()
