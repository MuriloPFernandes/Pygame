
#Constantes de configuração do jogo.

#Centralizar os valores aqui facilita ajustar a dificuldade e o visual
#sem precisar procurar números "mágicos" espalhados pelo código.


# Janela 
LARGURA = 960
ALTURA = 540
FPS = 60
TITULO = "Corrida Infinita"

# --- Mundo ---
CHAO_Y = 440            # coordenada y da superfície do chão
GRAVIDADE = 0.8         # aceleração vertical somada a cada frame
FORCA_PULO = -16        # velocidade vertical inicial do pulo (negativa = para cima)

# Velocidade / dificuldade 
VELOCIDADE_INICIAL = 6.0    # pixels por frame
VELOCIDADE_MAXIMA = 16.0
ACELERACAO = 0.002          # quanto a velocidade aumenta a cada frame

# Intervalo (em frames) entre o surgimento de obstáculos
INTERVALO_MIN_OBSTACULO = 50
INTERVALO_MAX_OBSTACULO = 110

# --- Cores (R, G, B) ---
BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)
CEU = (135, 200, 235)
CHAO = (90, 160, 70)
TERRA = (120, 85, 50)
JOGADOR_COR = (230, 90, 60)
OBSTACULO_COR = (60, 60, 70)
AMARELO = (250, 210, 60)