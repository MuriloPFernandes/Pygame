import pygame

from config import ALTURA, FPS, LARGURA, PRETO, TITULO


def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    relogio = pygame.time.Clock()

    executando = True
    while executando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False

        tela.fill(PRETO)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
