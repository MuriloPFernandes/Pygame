"""Desenho da tabela e consulta de todas as partidas do ranking geral."""

import pygame

from config import AMARELO, BRANCO, CINZA, FPS, PRETO
from screens.estilo import escrever


def desenhar_ranking(tela, ranking, y, pagina=0, quantidade=5, destaque=None,
                     posicoes=None, mensagem_vazia="Nenhuma partida registrada ainda"):
    # "posicoes" é usado na pesquisa: guarda a posição real de cada partida no ranking
    # completo, para o número não mudar quando a lista está filtrada.
    fonte = pygame.font.Font(None, 23)
    pequena = pygame.font.Font(None, 20)
    for texto, x in (("Pos.", 34), ("Nome", 76), ("Pontos", 266), ("Dificuldade", 350)):
        tela.blit(pequena.render(texto, True, CINZA), (x, y))
    if not ranking:
        escrever(tela, mensagem_vazia, pequena, CINZA, y + 46)
    inicio = pagina * quantidade
    for posicao in range(inicio, min(inicio + quantidade, len(ranking))):
        indice, resultado = ranking[posicao]
        linha_y = y + 28 + (posicao - inicio) * 29
        cor = AMARELO if indice == destaque else BRANCO
        nome = resultado["nome"][:16]
        while fonte.size(nome)[0] > 165:
            nome = nome[:-1]
        if posicoes is None:
            numero = posicao + 1
        else:
            numero = posicoes[indice]
        tela.blit(fonte.render(str(numero), True, cor), (34, linha_y))
        tela.blit(fonte.render(nome, True, cor), (76, linha_y))
        pontos = pequena.render(str(resultado["pontos"]), True, cor)
        tela.blit(pontos, pontos.get_rect(topright=(334, linha_y)))
        tela.blit(pequena.render(resultado["dificuldade"], True, cor), (350, linha_y))


def tela_ranking(tela, clock, ranking, dificuldade):
    # Mostra o ranking completo de uma dificuldade, com pesquisa por nome.
    pagina = 0
    pesquisa = ""
    fonte = pygame.font.Font(None, 38)
    pequena = pygame.font.Font(None, 23)

    # Posição real de cada partida no ranking completo (índice da partida -> posição).
    posicoes = {}
    for posicao, (indice, resultado) in enumerate(ranking):
        posicoes[indice] = posicao + 1

    pygame.key.start_text_input()
    # Descarta letras que ficaram na fila (por exemplo, o "R" usado para abrir esta tela).
    pygame.event.clear(pygame.TEXTINPUT)
    try:
        while True:
            clock.tick(FPS)

            # Pesquisa: só ficam as partidas cujo nome contém o texto digitado.
            filtrado = []
            for indice, resultado in ranking:
                if pesquisa.strip().lower() in resultado["nome"].lower():
                    filtrado.append((indice, resultado))
            paginas = max(1, (len(filtrado) + 14) // 15)
            pagina = min(pagina, paginas - 1)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.TEXTINPUT:
                    pesquisa += "".join(letra for letra in evento.text if letra.isprintable())
                    pesquisa = pesquisa[:16]
                    pagina = 0
                if evento.type == pygame.KEYDOWN:
                    if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        return "menu"
                    if evento.key == pygame.K_BACKSPACE:
                        pesquisa = pesquisa[:-1]
                        pagina = 0
                    if evento.key == pygame.K_RIGHT:
                        pagina = min(pagina + 1, paginas - 1)
                    if evento.key == pygame.K_LEFT:
                        pagina = max(0, pagina - 1)

            tela.fill(PRETO)
            escrever(tela, f"RANKING · {dificuldade.upper()}", fonte, AMARELO, 40)

            # Linha de pesquisa.
            pygame.draw.rect(tela, BRANCO, (30, 66, 420, 36), 2, border_radius=8)
            if pesquisa:
                escrever(tela, pesquisa + "|", pequena, BRANCO, 84)
            else:
                escrever(tela, "Pesquisar nome: digite aqui|", pequena, CINZA, 84)

            if ranking:
                mensagem = "Nenhum jogador com esse nome"
            else:
                mensagem = f"Ninguém jogou no {dificuldade} ainda"
            desenhar_ranking(tela, filtrado, 118, pagina, 15, posicoes=posicoes,
                             mensagem_vazia=mensagem)
            if pesquisa:
                escrever(tela, f"{len(filtrado)} partida(s) encontrada(s)", pequena, AMARELO, 600)
            escrever(tela, f"Página {pagina + 1}/{paginas}  |  Setas: navegar", pequena, CINZA, 630)
            escrever(tela, "ESC / ENTER: voltar ao menu", pequena, BRANCO, 663)
            pygame.display.update()
    finally:
        pygame.key.stop_text_input()
