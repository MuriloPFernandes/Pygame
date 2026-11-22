"""Entrada do nome antes de cada corrida, incluindo as partidas repetidas."""

import pygame

from config import AMARELO, BRANCO, CINZA, FPS, PRETO
from screens.estilo import escrever


def tela_nome(tela, clock, dificuldade):
    nome = ""
    fonte = pygame.font.Font(None, 38)
    pequena = pygame.font.Font(None, 25)
    pygame.key.start_text_input()
    try:
        while True:
            clock.tick(FPS)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                if evento.type == pygame.TEXTINPUT:
                    nome += "".join(letra for letra in evento.text if letra.isprintable())
                    nome = nome[:16]
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    elif evento.key == pygame.K_ESCAPE:
                        return ""
                    elif evento.key == pygame.K_RETURN and nome.strip():
                        return nome.strip()
            tela.fill(PRETO)
            escrever(tela, "QUAL É O SEU NOME?", fonte, AMARELO, 200)
            escrever(tela, f"Dificuldade: {dificuldade}", pequena, CINZA, 250)
            pygame.draw.rect(tela, BRANCO, (30, 300, 420, 58), 2, border_radius=8)
            escrever(tela, nome + "|", pequena, BRANCO, 330)
            escrever(tela, "Até 16 caracteres", pequena, CINZA, 390)
            escrever(tela, "ENTER: começar   |   ESC: menu", pequena, BRANCO, 450)
            pygame.display.update()
    finally:
        pygame.key.stop_text_input()
