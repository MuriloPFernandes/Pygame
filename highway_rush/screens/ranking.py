"""Desenho da tabela e consulta de todas as partidas do ranking geral."""

import pygame

from config import AMARELO, BRANCO, CINZA, FPS, PRETO
from screens.estilo import escrever


def desenhar_ranking(tela, ranking, y, pagina=0, quantidade=5, destaque=None):
    fonte = pygame.font.Font(None, 23)
    pequena = pygame.font.Font(None, 20)
    for texto, x in (("Pos.", 34), ("Nome", 76), ("Pontos", 266), ("Dificuldade", 350)):
        tela.blit(pequena.render(texto, True, CINZA), (x, y))
    if not ranking:
        escrever(tela, "Nenhuma partida registrada ainda", pequena, CINZA, y + 46)
    inicio = pagina * quantidade
    for posicao in range(inicio, min(inicio + quantidade, len(ranking))):
        indice, resultado = ranking[posicao]
        linha_y = y + 28 + (posicao - inicio) * 29
        cor = AMARELO if indice == destaque else BRANCO
        nome = resultado["nome"][:16]
        while fonte.size(nome)[0] > 165:
            nome = nome[:-1]
        tela.blit(fonte.render(str(posicao + 1), True, cor), (34, linha_y))
        tela.blit(fonte.render(nome, True, cor), (76, linha_y))
        pontos = pequena.render(str(resultado["pontos"]), True, cor)
        tela.blit(pontos, pontos.get_rect(topright=(334, linha_y)))
        tela.blit(pequena.render(resultado["dificuldade"], True, cor), (350, linha_y))


def tela_ranking(tela, clock, ranking):
    pagina = 0
    paginas = max(1, (len(ranking) + 14) // 15)
    fonte = pygame.font.Font(None, 38)
    pequena = pygame.font.Font(None, 23)
    while True:
        clock.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_r, pygame.K_RETURN):
                    return "menu"
                if evento.key == pygame.K_RIGHT:
                    pagina = min(pagina + 1, paginas - 1)
                if evento.key == pygame.K_LEFT:
                    pagina = max(0, pagina - 1)
        tela.fill(PRETO)
        escrever(tela, "RANKING GERAL", fonte, AMARELO, 54)
        desenhar_ranking(tela, ranking, 104, pagina, 15)
        escrever(tela, f"Página {pagina + 1}/{paginas}  |  Setas: navegar", pequena, CINZA, 624)
        escrever(tela, "ESC / ENTER: voltar ao menu", pequena, BRANCO, 663)
        pygame.display.update()
