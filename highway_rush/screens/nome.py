"""Entrada do nome antes de cada corrida, incluindo as partidas repetidas.

O jogador pode digitar um nome novo ou clicar no próprio nome, se já jogou antes.
O texto digitado também funciona como busca na lista de nomes.
"""

import pygame

from config import AMARELO, BRANCO, CINZA, FPS, PRETO, VERMELHO
from ranking import nomes_usados
from screens.estilo import escrever

# Lista de nomes: 2 colunas x 6 linhas = 12 nomes por página.
COLUNAS = 2
LINHAS = 6
LARGURA_BOTAO = 200
ALTURA_BOTAO = 40


def criar_botoes(nomes, pagina):
    # Devolve uma lista de (retângulo, nome) para os nomes da página atual.
    botoes = []
    por_pagina = COLUNAS * LINHAS
    inicio = pagina * por_pagina
    for i, nome in enumerate(nomes[inicio:inicio + por_pagina]):
        coluna = i % COLUNAS
        linha = i // COLUNAS
        x = 30 + coluna * (LARGURA_BOTAO + 20)
        y = 300 + linha * (ALTURA_BOTAO + 10)
        botoes.append((pygame.Rect(x, y, LARGURA_BOTAO, ALTURA_BOTAO), nome))
    return botoes


def tela_nome(tela, clock, dificuldade, resultados):
    # Devolve o nome escolhido, "" para voltar ao menu ou None se a janela for fechada.
    nome = ""
    pagina = 0
    fonte = pygame.font.Font(None, 38)
    media = pygame.font.Font(None, 28)
    pequena = pygame.font.Font(None, 23)

    todos_os_nomes = nomes_usados(resultados)
    nomes_minusculos = []
    for usado in todos_os_nomes:
        nomes_minusculos.append(usado.lower())

    pygame.key.start_text_input()
    try:
        while True:
            clock.tick(FPS)

            # Filtra a lista: só aparecem os nomes que contêm o que foi digitado.
            busca = nome.strip().lower()
            filtrados = []
            for usado in todos_os_nomes:
                if busca in usado.lower():
                    filtrados.append(usado)
            por_pagina = COLUNAS * LINHAS
            paginas = max(1, (len(filtrados) + por_pagina - 1) // por_pagina)
            pagina = min(pagina, paginas - 1)
            botoes = criar_botoes(filtrados, pagina)

            # O nome digitado só pode ser usado se ninguém tiver usado antes.
            nome_repetido = busca in nomes_minusculos

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                if evento.type == pygame.TEXTINPUT:
                    nome += "".join(letra for letra in evento.text if letra.isprintable())
                    nome = nome[:16]
                    pagina = 0
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                        pagina = 0
                    elif evento.key == pygame.K_ESCAPE:
                        return ""
                    elif evento.key == pygame.K_RETURN and nome.strip() and not nome_repetido:
                        return nome.strip()
                    elif evento.key == pygame.K_RIGHT:
                        pagina = min(pagina + 1, paginas - 1)
                    elif evento.key == pygame.K_LEFT:
                        pagina = max(0, pagina - 1)
                # Clique com o botão esquerdo em um nome da lista: joga com esse nome.
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    for retangulo, nome_botao in botoes:
                        if retangulo.collidepoint(evento.pos):
                            return nome_botao

            # ----- Desenho -----
            tela.fill(PRETO)
            escrever(tela, "QUAL É O SEU NOME?", fonte, AMARELO, 60)
            escrever(tela, f"Dificuldade: {dificuldade}", pequena, CINZA, 95)

            # Caixa de texto (a barrinha "|" mostra onde o texto vai aparecer).
            cor_caixa = VERMELHO if nome_repetido else BRANCO
            pygame.draw.rect(tela, cor_caixa, (30, 120, 420, 50), 2, border_radius=8)
            escrever(tela, nome + "|", media, BRANCO, 145)

            # Mensagem que explica o que o jogador pode fazer.
            if nome_repetido:
                escrever(tela, "Esse nome já foi usado!", pequena, VERMELHO, 190)
                escrever(tela, "Se for você, clique nele abaixo. Se não, escolha outro.",
                         pequena, VERMELHO, 212)
            elif busca:
                escrever(tela, "Nome livre! Aperte ENTER para começar.", pequena, AMARELO, 190)
            else:
                escrever(tela, "Digite um nome novo (até 16 caracteres)", pequena, CINZA, 190)
            pygame.draw.line(tela, CINZA, (30, 232), (450, 232))

            # ----- Lista de nomes já usados -----
            escrever(tela, "JÁ JOGOU? CLIQUE NO SEU NOME", media, AMARELO, 256)
            if busca:
                escrever(tela, "Mostrando nomes parecidos com o que você digitou", pequena, CINZA, 280)
            else:
                escrever(tela, "Digite acima para procurar o seu nome", pequena, CINZA, 280)

            if not todos_os_nomes:
                escrever(tela, "Ninguém jogou ainda. Seja o primeiro!", pequena, CINZA, 330)
            elif not filtrados:
                escrever(tela, "Nenhum nome encontrado", pequena, CINZA, 330)

            mouse = pygame.mouse.get_pos()
            for retangulo, nome_botao in botoes:
                # O botão embaixo do mouse fica amarelo, mostrando que dá para clicar.
                if retangulo.collidepoint(mouse):
                    pygame.draw.rect(tela, AMARELO, retangulo, border_radius=8)
                    cor_texto = PRETO
                else:
                    pygame.draw.rect(tela, (40, 40, 45), retangulo, border_radius=8)
                    pygame.draw.rect(tela, CINZA, retangulo, 1, border_radius=8)
                    cor_texto = BRANCO
                # Nomes muito compridos são cortados para caber no botão.
                texto_botao = nome_botao
                while media.size(texto_botao)[0] > LARGURA_BOTAO - 14:
                    texto_botao = texto_botao[:-1]
                texto = media.render(texto_botao, True, cor_texto)
                tela.blit(texto, texto.get_rect(center=retangulo.center))

            if paginas > 1:
                escrever(tela, f"Página {pagina + 1}/{paginas}  |  Setas: trocar página",
                         pequena, CINZA, 612)

            escrever(tela, "ENTER: começar com nome novo   |   ESC: menu", pequena, BRANCO, 660)
            pygame.display.update()
    finally:
        pygame.key.stop_text_input()
