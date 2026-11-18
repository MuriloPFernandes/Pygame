# Highway Rush - arquivo principal
# Abre a janela e roda o loop do jogo.

from pathlib import Path
from random import randint

import pygame
from config import (
    ALTURA,
    BRANCO,
    FPS,
    INTERVALO_MAX_ADVERSARIO,
    INTERVALO_MIN_ADVERSARIO,
    LARGURA,
    PRETO,
    TITULO,
    VIDAS_INICIAIS,
)
from sprites.enemy import (
    carregar_imagens_adversarios,
    criar_adversario,
    desenhar_adversarios,
    mover_adversarios,
    remover_adversarios_colididos,
)
from sprites.player import carregar_imagem_carro, criar_carro, desenhar_carro, mover_carro
from sprites.road import desenhar_pista, atualizar_faixas

pygame.init()

window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

clock = pygame.time.Clock()
fonte_vidas = pygame.font.Font(None, 32)
vidas = VIDAS_INICIAIS
deslocamento_faixas = 0
carro = criar_carro()
imagem_carro = carregar_imagem_carro(carro)
imagens_adversarios = carregar_imagens_adversarios()
adversarios = []
quadros_ate_adversario = INTERVALO_MIN_ADVERSARIO
teclas_pressionadas = set()

# Carrega a música uma única vez e repete durante toda a corrida.
# O caminho parte deste arquivo, independentemente da pasta de execução.
caminho_musica = Path(__file__).resolve().parent / "assets" / "sounds" / "music" / "jogo.wav"
if pygame.mixer.get_init():
    pygame.mixer.music.load(str(caminho_musica))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

# Loop principal
game = True
while game:
    clock.tick(FPS)  # mantém o jogo em 60 quadros por segundo

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # clicou no X da janela
            game = False
        elif event.type == pygame.KEYDOWN:
            teclas_pressionadas.add(event.key)
        elif event.type == pygame.KEYUP:
            teclas_pressionadas.discard(event.key)
        elif event.type == pygame.WINDOWFOCUSLOST:
            # Evita que uma tecla fique presa ao alternar de janela.
            teclas_pressionadas.clear()
    if not game:
        break

    mover_carro(carro, teclas_pressionadas)

    # Depois de cada chegada, sorteia quantos quadros faltam para a próxima.
    quadros_ate_adversario -= 1
    if quadros_ate_adversario == 0:
        adversarios.append(criar_adversario(imagens_adversarios))
        quadros_ate_adversario = randint(INTERVALO_MIN_ADVERSARIO, INTERVALO_MAX_ADVERSARIO)

    adversarios = mover_adversarios(adversarios)
    restantes = remover_adversarios_colididos(carro, adversarios)
    if len(restantes) < len(adversarios):
        # Desconta uma vida pelo impacto. Os carros atingidos saem da pista.
        vidas -= 1
    adversarios = restantes

    # A pista é desenhada antes do carro para ele aparecer por cima.
    desenhar_pista(window, deslocamento_faixas)
    desenhar_adversarios(window, adversarios)
    desenhar_carro(window, carro, imagem_carro)
    texto_vidas = fonte_vidas.render(f"Vidas: {vidas}", True, BRANCO, PRETO)
    window.blit(texto_vidas, (12, 12))
    pygame.display.update()
    deslocamento_faixas = atualizar_faixas(deslocamento_faixas)
    if vidas == 0:
        game = False

# Encerra a música ao fechar a janela ou perder todas as vidas.
if pygame.mixer.get_init():
    pygame.mixer.music.stop()
pygame.quit()
