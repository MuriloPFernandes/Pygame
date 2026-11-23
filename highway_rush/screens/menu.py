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
from ranking import ordenar_ranking
from screens.ranking import desenhar_ranking, tela_ranking
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


def tela_menu(tela, clock, resultados, aviso_ranking=""):
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

    painel = pygame.Rect(20, 20, 440, 680)

    tocar_musica_menu()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Abre o ranking completo da dificuldade selecionada.
                    dificuldade_atual = opcoes[escolhida]
                    ranking_atual = ordenar_ranking(resultados, dificuldade_atual)
                    if tela_ranking(tela, clock, ranking_atual, dificuldade_atual) == "sair":
                        return None
                if event.key in (pygame.K_UP, pygame.K_w):
                    escolhida = (escolhida - 1) % len(opcoes)  # sobe e volta pro fim
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    escolhida = (escolhida + 1) % len(opcoes)  # desce e volta pro começo
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if pygame.mixer.get_init():
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

        # O ranking mostrado muda junto com a dificuldade selecionada.
        ranking = ordenar_ranking(resultados, opcoes[escolhida])
        escrever(tela, f"RANKING · {opcoes[escolhida]} · R: ver todos", fonte_pequena, AMARELO, 436)
        desenhar_ranking(tela, ranking, 458,
                         mensagem_vazia=f"Ninguém jogou no {opcoes[escolhida]} ainda")

        # ----- Instruções -----
        # O ENTER pisca: aparece meio segundo, some meio segundo.
        if tempo // 500 % 2 == 0:
            desenhar_tecla(tela, fonte_tecla, "ENTER", "informar nome e jogar", AMARELO, 642)
        desenhar_tecla(tela, fonte_pequena, "SETAS / WASD", "escolher / dirigir", CINZA, 674)
        if aviso_ranking:
            escrever(tela, aviso_ranking, pygame.font.Font(None, 19), AMARELO, 709)

        pygame.display.update()
