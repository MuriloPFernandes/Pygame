# Tela de Game Over: mostra a pontuação, o recorde e as opções para continuar.

import math
from pathlib import Path

import pygame

from config import AMARELO, BRANCO, CINZA, FPS, LARGURA, PRETO, VERMELHO
from screens.estilo import desenhar_painel, desenhar_tecla, desenhar_xadrez, escrever


def tocar_musica_game_over():
    # Só toca se o arquivo existir, assim a tela funciona mesmo sem a música.
    caminho = Path(__file__).resolve().parents[1] / "assets" / "sounds" / "music" / "game_over.wav"
    if pygame.mixer.get_init() and caminho.exists():
        pygame.mixer.music.load(str(caminho))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


def tela_game_over(tela, clock, pontuacao, recorde, dificuldade):
    # Devolve "jogo" (jogar de novo), "menu" (voltar ao menu) ou "sair" (fechou a janela).
    fonte_titulo = pygame.font.Font(None, 84)
    fonte_pontos = pygame.font.Font(None, 90)
    fonte_texto = pygame.font.Font(None, 30)
    fonte_tecla = pygame.font.Font(None, 28)

    # Guarda o último quadro da corrida (com o carro destruído) como fundo, escurecido.
    fundo = tela.copy()
    sombra = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
    sombra.fill((0, 0, 0, 140))
    fundo.blit(sombra, (0, 0))

    painel = pygame.Rect(50, 80, 380, 520)

    # Caixa onde a pontuação aparece.
    caixa_pontos = pygame.Rect(0, 0, 240, 80)
    caixa_pontos.center = (LARGURA // 2, 322)

    # O recorde só é "novo" se o jogador fez pontos e igualou o maior valor.
    novo_recorde = pontuacao > 0 and pontuacao == recorde

    # A pontuação "sobe" do zero até o valor final em cerca de 1 segundo.
    pontos_mostrados = 0
    passo = max(1, pontuacao // 60)

    tocar_musica_game_over()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "sair"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    return "jogo"
                if event.key == pygame.K_m:
                    pygame.mixer.music.stop()
                    return "menu"

        pontos_mostrados = min(pontuacao, pontos_mostrados + passo)
        tempo = pygame.time.get_ticks()

        tela.blit(fundo, (0, 0))
        desenhar_painel(tela, painel, VERMELHO)
        desenhar_xadrez(tela, 70, 94, 340)

        # Título balançando, como no menu.
        balanco = int(5 * math.sin(tempo / 300))
        escrever(tela, "GAME OVER", fonte_titulo, VERMELHO, 165 + balanco)
        escrever(tela, f"Dificuldade: {dificuldade}", fonte_texto, CINZA, 214)
        pygame.draw.line(tela, CINZA, (90, 238), (390, 238))

        # ----- Pontuação dentro de uma caixa -----
        escrever(tela, "PONTUAÇÃO", fonte_texto, CINZA, 264)
        pygame.draw.rect(tela, (20, 20, 25), caixa_pontos, border_radius=12)
        pygame.draw.rect(tela, AMARELO, caixa_pontos, 2, border_radius=12)
        escrever(tela, str(pontos_mostrados), fonte_pontos, AMARELO, caixa_pontos.centery + 3)

        # ----- Recorde (só aparece quando a contagem termina) -----
        if pontos_mostrados == pontuacao:
            if novo_recorde:
                # Faixa amarela que "pulsa" crescendo e diminuindo.
                largura = 230 + int(10 * math.sin(tempo / 120))
                faixa = pygame.Rect(0, 0, largura, 34)
                faixa.center = (LARGURA // 2, 392)
                pygame.draw.rect(tela, AMARELO, faixa, border_radius=8)
                escrever(tela, "NOVO RECORDE!", fonte_texto, PRETO, 392, sombra=False)
            else:
                escrever(tela, f"Recorde: {recorde}", fonte_texto, BRANCO, 392)
        pygame.draw.line(tela, CINZA, (90, 425), (390, 425))

        # ----- Opções -----
        # O ENTER pisca para chamar a atenção.
        if tempo // 500 % 2 == 0:
            desenhar_tecla(tela, fonte_tecla, "ENTER", "jogar novamente", AMARELO, 462)
        desenhar_tecla(tela, fonte_tecla, "M", "voltar ao menu", BRANCO, 508)
        desenhar_xadrez(tela, 70, 566, 340)

        pygame.display.update()
