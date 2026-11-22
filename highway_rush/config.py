# Configurações do jogo (tamanho da tela, FPS, cores...)

# Janela
LARGURA = 480
ALTURA = 720
FPS = 60
TITULO = "Highway Rush"

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (250, 210, 60)
CINZA = (170, 170, 170)
VERMELHO = (230, 75, 55)
LARANJA = (255, 140, 40)
FUMACA_CLARA = (200, 200, 200)
FUMACA_ESCURA = (70, 70, 70)

# Pista
LARGURA_PISTA = 320
PISTA_X = (LARGURA - LARGURA_PISTA) // 2
COR_ASFALTO = (55, 55, 60)
COR_GRAMA = (55, 125, 65)
COMPRIMENTO_FAIXA = 48
ESPACO_ENTRE_FAIXAS = 36
VELOCIDADE_PISTA = 6

# Carro do jogador
LARGURA_CARRO = 42
ALTURA_CARRO = 76
MARGEM_INFERIOR_CARRO = 24
VELOCIDADE_CARRO = 5
VIDAS_INICIAIS = 3

# Carros adversários
VELOCIDADE_ADVERSARIO = 5

INTERVALO_MIN_ADVERSARIO = 50
INTERVALO_MAX_ADVERSARIO = 90

# Progressão durante a corrida (o tempo acompanha os quadros do jogo).
QUADROS_POR_AUMENTO = FPS * 20
MAX_AUMENTOS_DIFICULDADE = 4
REDUCAO_INTERVALO = 5
# Mantém pelo menos meio segundo entre carros a 60 FPS.
INTERVALO_MIN_SEGURO = 30

# Dificuldades escolhidas no menu.
# velocidade_adversario: quantos pixels os carros descem por quadro
# velocidade_pista: rapidez das faixas (sensação de velocidade)
# intervalo_min / intervalo_max: quadros entre um carro e outro (menor = mais trânsito)
DIFICULDADES = {
    "Fácil": {
        "velocidade_adversario": 4,
        "velocidade_pista": 5,
        "intervalo_min": 70,
        "intervalo_max": 110,
        "descricao": "Trânsito leve, bom para treinar",
    },
    "Médio": {
        "velocidade_adversario": 5,
        "velocidade_pista": 6,
        "intervalo_min": 50,
        "intervalo_max": 90,
        "descricao": "O desafio equilibrado",
    },
    "Difícil": {
        "velocidade_adversario": 7,
        "velocidade_pista": 8,
        "intervalo_min": 35,
        "intervalo_max": 65,
        "descricao": "Hora do rush: reflexos rápidos!",
    },
}
