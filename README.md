# Highway Rush

Projeto Pygame de Eduardo Oliveira, Luis Luz e Murilo Fernandes.

## Como executar

Com o Pygame instalado, execute `python highway_rush/main.py` na raiz do projeto.

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
computador: não são sincronizados pelo GitHub. Essa pasta é ignorada pelo Git.
