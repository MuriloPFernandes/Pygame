# Tela da corrida: o jogador desvia dos carros até perder todas as vidas.

from pathlib import Path
from random import randint

import pygame

from config import (
    AMARELO,
    AZUL,
    BRANCO,
    DIFICULDADES,
    DURACAO_POWERUP,
    FATOR_CAMERA_LENTA,
    FPS,
    INTERVALO_MAX_POWERUP,
    INTERVALO_MIN_POWERUP,
    INTERVALO_MIN_SEGURO,
    LARGURA,
    MAX_AUMENTOS_DIFICULDADE,
    PRETO,
    QUADROS_POR_AUMENTO,
    REDUCAO_INTERVALO,
    VIDAS_INICIAIS,
)
from sprites.effects import (
    atualizar_particulas,
    criar_chama,
    criar_explosao,
    criar_fumaca,
    criar_fumaca_destruido,
    desenhar_particulas,
    queimar_imagem,
)
from sprites.enemy import (
    carregar_imagens_adversarios,
    criar_adversario,
    desenhar_adversarios,
    mover_adversarios,
    remover_adversarios_colididos,
)
from sprites.powerup import coletar_powerups, criar_powerup, desenhar_powerups, mover_powerups
from sprites.player import carregar_imagem_carro, criar_carro, desenhar_carro, mover_carro
from sprites.road import desenhar_pista, atualizar_faixas

PASTA_SONS = Path(__file__).resolve().parents[1] / "assets" / "sounds"
DURACAO_EXPLOSAO = 120  # quadros (2 segundos) mostrando a explosão antes do Game Over
DURACAO_TREMOR = 20     # quadros em que a tela treme logo após a explosão


def tela_jogo(tela, clock, dificuldade):
    # Roda uma corrida inteira.
    # Devolve a pontuação final, ou None se a janela for fechada.
    # Como tudo é criado aqui dentro, cada nova partida começa do zero.

    # Pega as configurações da dificuldade escolhida (ver config.py).
    config_dificuldade = DIFICULDADES[dificuldade]
    velocidade_adversarios = config_dificuldade["velocidade_adversario"]
    velocidade_pista = config_dificuldade["velocidade_pista"]
    intervalo_min = config_dificuldade["intervalo_min"]
    intervalo_max = config_dificuldade["intervalo_max"]

    fonte_placar = pygame.font.Font(None, 32)
    vidas = VIDAS_INICIAIS
    pontos = 0
    deslocamento_faixas = 0
    carro = criar_carro()
    imagem_carro = carregar_imagem_carro(carro)
    imagens_adversarios = carregar_imagens_adversarios()
    adversarios = []
    quadros_ate_adversario = intervalo_min
    teclas_pressionadas = set()
    quadros_corrida = 0
    aumentos_dificuldade = 0

    # Power-ups: itens na pista e quantos quadros de efeito ainda restam.
    fonte_powerup = pygame.font.Font(None, 26)
    powerups = []
    quadros_ate_powerup = randint(INTERVALO_MIN_POWERUP, INTERVALO_MAX_POWERUP)
    quadros_dobro = 0   # pontuação em dobro
    quadros_lento = 0   # câmera lenta

    # Efeitos visuais
    fumaca = []             # partículas de fumaça do carro danificado
    explosao = []           # partículas de fogo da explosão
    quadros_destruido = 0   # quantos quadros se passaram desde a explosão
    contador_quadros = 0

    # Música da corrida, repetindo enquanto o jogo roda.
    if pygame.mixer.get_init():
        pygame.mixer.music.load(str(PASTA_SONS / "music" / "jogo.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    # O efeito usa um canal separado para não interromper a música da corrida.
    som_colisao = None
    canal_colisao = None
    if pygame.mixer.get_init():
        som_colisao = pygame.mixer.Sound(str(PASTA_SONS / "effects" / "colisao.flac"))

    while True:
        clock.tick(FPS)  # mantém o jogo em 60 quadros por segundo
        contador_quadros += 1

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # clicou no X da janela
                pygame.mixer.music.stop()
                return None
            elif event.type == pygame.KEYDOWN:
                teclas_pressionadas.add(event.key)
            elif event.type == pygame.KEYUP:
                teclas_pressionadas.discard(event.key)
            elif event.type == pygame.WINDOWFOCUSLOST:
                # Evita que uma tecla fique presa ao alternar de janela.
                teclas_pressionadas.clear()

        if vidas > 0:
            # ----- Corrida normal -----
            quadros_corrida += 1
            if (quadros_corrida % QUADROS_POR_AUMENTO == 0
                    and aumentos_dificuldade < MAX_AUMENTOS_DIFICULDADE):
                # Aumenta aos poucos, a partir da dificuldade escolhida no menu.
                # Os limites evitam velocidade e frequência sem controle.
                aumentos_dificuldade += 1
                velocidade_adversarios += 1
                velocidade_pista += 1
                intervalo_min = max(INTERVALO_MIN_SEGURO, intervalo_min - REDUCAO_INTERVALO)
                intervalo_max = max(intervalo_min, intervalo_max - REDUCAO_INTERVALO)
                # O carro já agendado mantém seu prazo; os próximos usam o novo intervalo.

            # Na câmera lenta o mundo anda mais devagar, mas o carro do jogador não.
            # Por isso ele consegue desviar com mais facilidade.
            if quadros_lento > 0:
                quadros_lento -= 1
                fator_tempo = FATOR_CAMERA_LENTA
            else:
                fator_tempo = 1
            if quadros_dobro > 0:
                quadros_dobro -= 1
            velocidade_adversarios_atual = max(1, round(velocidade_adversarios * fator_tempo))
            velocidade_pista_atual = max(1, round(velocidade_pista * fator_tempo))

            mover_carro(carro, teclas_pressionadas)

            # Depois de cada chegada, sorteia quantos quadros faltam para a próxima.
            # O relógio também anda mais devagar na câmera lenta, para o trânsito não acumular.
            quadros_ate_adversario -= fator_tempo
            if quadros_ate_adversario <= 0:
                adversarios.append(criar_adversario(imagens_adversarios))
                quadros_ate_adversario = randint(intervalo_min, intervalo_max)

            # Power-ups surgem de tempos em tempos e descem junto com a pista.
            quadros_ate_powerup -= fator_tempo
            if quadros_ate_powerup <= 0:
                powerups.append(criar_powerup())
                quadros_ate_powerup = randint(INTERVALO_MIN_POWERUP, INTERVALO_MAX_POWERUP)
            powerups = mover_powerups(powerups, velocidade_pista_atual)
            powerups, coletados = coletar_powerups(carro, powerups)
            for tipo in coletados:
                # Pegar o mesmo power-up de novo renova os 5 segundos.
                if tipo == "dobro":
                    quadros_dobro = DURACAO_POWERUP
                elif tipo == "lento":
                    quadros_lento = DURACAO_POWERUP

            adversarios = mover_adversarios(adversarios, velocidade_adversarios_atual)
            restantes = remover_adversarios_colididos(carro, adversarios)
            if len(restantes) < len(adversarios):
                # Desconta uma vida pelo impacto. Os carros atingidos saem da pista.
                vidas -= 1
                if som_colisao is not None:
                    canal_colisao = som_colisao.play()
                if vidas == 0:
                    # Última batida: o carro explode e fica carbonizado.
                    explosao = criar_explosao(carro.centerx, carro.centery)
                    imagem_carro = queimar_imagem(imagem_carro)
            adversarios = restantes

            # Pontuação pela distância: quanto mais rápida a pista, mais pontos por quadro.
            # Com o power-up de dobro ativo, cada quadro vale o dobro de pontos.
            ganho = velocidade_pista / 10
            if quadros_dobro > 0:
                ganho *= 2
            pontos += ganho

            # Carro danificado solta fumaça. Com 1 vida, a fumaça sai com mais frequência.
            if vidas == VIDAS_INICIAIS - 1 and contador_quadros % 4 == 0:
                fumaca.append(criar_fumaca(carro, vidas))
            elif 0 < vidas <= VIDAS_INICIAIS - 2 and contador_quadros % 2 == 0:
                fumaca.append(criar_fumaca(carro, vidas))

            # A fumaça fica para trás devagar, formando um rastro atrás do carro.
            fumaca = atualizar_particulas(fumaca, velocidade_pista_atual * 0.3)
            deslocamento_faixas = atualizar_faixas(deslocamento_faixas, velocidade_pista_atual)
        else:
            # ----- Carro destruído: tudo para e a explosão acontece -----
            quadros_destruido += 1

            # O carro queimado continua pegando fogo e soltando fumaça preta.
            if contador_quadros % 3 == 0:
                fumaca.append(criar_fumaca_destruido(carro))
            explosao.append(criar_chama(carro))
            fumaca = atualizar_particulas(fumaca, 0)
            explosao = atualizar_particulas(explosao, 0)

            # Espera a explosão e o som de batida terminarem antes do Game Over.
            som_terminou = canal_colisao is None or not canal_colisao.get_busy()
            if quadros_destruido >= DURACAO_EXPLOSAO and som_terminou:
                pygame.mixer.music.stop()
                return int(pontos)

        # ----- Desenho -----
        # A pista é desenhada antes do carro para ele aparecer por cima.
        desenhar_pista(tela, deslocamento_faixas)
        desenhar_powerups(tela, powerups, fonte_powerup, contador_quadros)
        desenhar_adversarios(tela, adversarios)
        desenhar_carro(tela, carro, imagem_carro)
        desenhar_particulas(tela, explosao)  # fogo
        desenhar_particulas(tela, fumaca)    # fumaça por cima de tudo

        # Placar: vidas no canto esquerdo, pontos no canto direito.
        texto_vidas = fonte_placar.render(f"Vidas: {vidas}", True, BRANCO, PRETO)
        tela.blit(texto_vidas, (12, 12))
        texto_pontos = fonte_placar.render(f"Pontos: {int(pontos)}", True, AMARELO, PRETO)
        tela.blit(texto_pontos, texto_pontos.get_rect(topright=(LARGURA - 12, 12)))

        # Power-ups ativos aparecem embaixo dos pontos, com barra de tempo restante.
        if vidas > 0:
            y_efeito = 48
            for nome, quadros, cor in (("Pontos 2x", quadros_dobro, AMARELO),
                                       ("Câmera lenta", quadros_lento, AZUL)):
                if quadros <= 0:
                    continue
                texto = fonte_powerup.render(nome, True, cor, PRETO)
                tela.blit(texto, texto.get_rect(topright=(LARGURA - 12, y_efeito)))
                largura_barra = int(100 * quadros / DURACAO_POWERUP)
                barra = pygame.Rect(0, 0, largura_barra, 5)
                barra.topright = (LARGURA - 12, y_efeito + 20)
                pygame.draw.rect(tela, cor, barra)
                y_efeito += 32

        # Tremor de tela logo depois da explosão: redesenha a imagem um pouco deslocada.
        if 0 < quadros_destruido <= DURACAO_TREMOR:
            copia = tela.copy()
            tela.fill(PRETO)
            tela.blit(copia, (randint(-8, 8), randint(-8, 8)))

        pygame.display.update()
