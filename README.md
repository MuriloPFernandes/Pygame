# Highway Rush

Highway Rush é um jogo de corrida desenvolvido em Python com Pygame. Desvie dos carros e dos obstáculos, colete power-ups e tente alcançar a maior pontuação enquanto a corrida fica mais difícil.

## Integrantes

- Eduardo Oliveira
- Luis Luz
- Murilo Fernandes

## Instalação e execução

Com o Python 3 instalado, abra um terminal na raiz do repositório. Instale o Pygame e execute o jogo com os comandos abaixo.

```bash
python -m pip install pygame
python highway_rush/main.py
```

## Como jogar

Escolha a dificuldade no menu, informe seu nome e pressione Enter para começar. Use as setas do teclado ou W, A, S e D para mover o carro durante a corrida e desviar dos obstáculos.

## Vídeo de apresentação
https://youtu.be/5vOL7e3tD7M?si=8LU6L2STBJ4gjJzC


## Ranking

No menu, escolha a dificuldade com as setas ou W/S e pressione Enter.
Informe seu nome (até 16 caracteres) e pressione Enter para iniciar a corrida.
Backspace apaga letras; Esc volta ao menu.

O menu mostra as cinco melhores partidas, com nome, pontos e dificuldade.
Pressione R para consultar o ranking geral completo e use as setas esquerda/direita
para mudar de página. Enter ou Esc volta ao menu.

Ao perder, aparece o ranking apenas da dificuldade jogada, com sua partida em
amarelo e sua posição. Use as setas para consultar as outras páginas, Enter para
informar um nome e jogar novamente, ou M para voltar ao menu.

Cada partida concluída gera uma entrada; em empate, a mais antiga fica na frente.
Fechar a janela durante a corrida não registra pontuação. Os resultados ficam em
`highway_rush/dados/ranking.json`, persistem ao fechar o jogo e são locais ao
computador: não são sincronizados pelo GitHub.


## Uso de IA
Pedimos auxílio do Claude e do ChatGPT para nos ajudar a programar o jogo. Usamos eles para gerar alguns sprites, como o pneu, a poça de óleo, e os power ups. Como não foi ensinado muito sobre programar um jogo foi necessário a ajuda das IAs para realizar algumas ações, como programar o impacto do carro com os obstáculos. Pedimos ajuda também para criar algumas funções, fomos pedindo o passo a passo de como fazer e também pedimos para fazer algumas delas. Além disso, precisamos de ajuda para organizar o nosso código, para não deixar tudo em um único file, então ele nos guiou para organizar.
Link do pneu e da poça: https://claude.ai/code/session_01BdwEwBvt9Hb9QKF6PJjgZN
