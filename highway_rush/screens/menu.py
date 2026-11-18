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
)
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


def escrever(tela, texto, fonte, cor, centro_y):
    # Desenha um texto centralizado na horizontal.
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, imagem.get_rect(center=(LARGURA // 2, centro_y)))


def desenhar_barra(tela, fonte, nome, fracao, y):
    # Desenha "nome [■■■■■□□□]" para mostrar o quanto a dificuldade é intensa.
    texto = fonte.render(nome, True, CINZA)
    tela.blit(texto, texto.get_rect(midleft=(90, y)))
    fracao = min(fracao, 1)
    pygame.draw.rect(tela, CINZA, (210, y - 6, 170, 12), 1)              # contorno
    pygame.draw.rect(tela, AMARELO, (212, y - 4, int(166 * fracao), 8))  # preenchimento


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
    fonte_titulo = pygame.font.Font(None, 84)
    fonte_opcao = pygame.font.Font(None, 44)
    fonte_texto = pygame.font.Font(None, 26)
    fonte_enter = pygame.font.Font(None, 34)
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

    # Painel escuro e transparente para destacar os textos sobre a pista.
    painel = pygame.Surface((380, 560), pygame.SRCALPHA)
    painel.fill((0, 0, 0, 150))

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
        tela.blit(painel, (50, 40))

        # ----- Título (sobe e desce devagar) -----
        tempo = pygame.time.get_ticks()
        balanco = int(5 * math.sin(tempo / 300))
        escrever(tela, "HIGHWAY", fonte_titulo, BRANCO, 100 + balanco)
        escrever(tela, "RUSH", fonte_titulo, AMARELO, 160 + balanco)
        escrever(tela, "Desvie do trânsito e vá longe!", fonte_texto, CINZA, 212)
        pygame.draw.line(tela, CINZA, (90, 240), (390, 240))

        # ----- Opções de dificuldade -----
        escrever(tela, "DIFICULDADE", fonte_pequena, CINZA, 268)
        for i, nome in enumerate(opcoes):
            y = 308 + i * 44
            if i == escolhida:
                escrever(tela, f"> {nome} <", fonte_opcao, AMARELO, y)
            else:
                escrever(tela, nome, fonte_opcao, BRANCO, y)

        # ----- Detalhes da dificuldade escolhida -----
        escrever(tela, config["descricao"], fonte_texto, BRANCO, 440)
        desenhar_barra(tela, fonte_texto, "Velocidade", config["velocidade_adversario"] / 8, 472)
        desenhar_barra(tela, fonte_texto, "Trânsito", 30 / config["intervalo_min"], 500)
        pygame.draw.line(tela, CINZA, (90, 528), (390, 528))

        # ----- Instruções -----
        # Texto piscando: aparece meio segundo, some meio segundo.
        if tempo // 500 % 2 == 0:
            escrever(tela, "ENTER para começar", fonte_enter, AMARELO, 555)
        escrever(tela, "Setas ou WASD para dirigir", fonte_pequena, CINZA, 585)

        pygame.display.update()
