"""Resultados locais: uma entrada para cada partida concluída."""

import json
from pathlib import Path

from config import DIFICULDADES

ARQUIVO_RANKING = Path(__file__).resolve().parent / "dados" / "ranking.json"


def carregar_ranking():
    if not ARQUIVO_RANKING.exists():
        return []
    with ARQUIVO_RANKING.open(encoding="utf-8") as arquivo:
        resultados = json.load(arquivo)
    if not isinstance(resultados, list):
        raise ValueError("Ranking inválido")
    for resultado in resultados:
        if (not isinstance(resultado, dict)
                or not isinstance(resultado.get("nome"), str)
                or not resultado["nome"].strip()
                or type(resultado.get("pontos")) is not int
                or resultado["pontos"] < 0
                or not isinstance(resultado.get("dificuldade"), str)
                or resultado.get("dificuldade") not in DIFICULDADES):
            raise ValueError("Resultado inválido")
    return resultados


def salvar_ranking(resultados):
    ARQUIVO_RANKING.parent.mkdir(parents=True, exist_ok=True)
    temporario = ARQUIVO_RANKING.with_suffix(".tmp")
    with temporario.open("w", encoding="utf-8") as arquivo:
        json.dump(resultados, arquivo, ensure_ascii=False, indent=2)
    # Só substitui o arquivo anterior depois de terminar a gravação.
    temporario.replace(ARQUIVO_RANKING)


def nomes_usados(resultados):
    # Lista os nomes de quem já jogou, sem repetir e em ordem alfabética.
    # "Murilo" e "murilo" contam como o mesmo nome (vale a primeira forma escrita).
    nomes = []
    ja_vistos = set()
    for resultado in resultados:
        chave = resultado["nome"].lower()
        if chave not in ja_vistos:
            ja_vistos.add(chave)
            nomes.append(resultado["nome"])
    return sorted(nomes, key=str.lower)


def ordenar_ranking(resultados, dificuldade=None):
    # Cada nome aparece uma vez só, com a sua maior pontuação.
    # O dicionário guarda: nome em minúsculas -> (índice da partida, resultado).
    melhores = {}
    for indice, resultado in enumerate(resultados):
        if dificuldade is not None and resultado["dificuldade"] != dificuldade:
            continue
        chave = resultado["nome"].lower()
        if chave not in melhores or resultado["pontos"] > melhores[chave][1]["pontos"]:
            melhores[chave] = (indice, resultado)
    # Coloca as partidas na ordem em que foram jogadas antes de ordenar pelos pontos.
    # Assim, em empate, a partida registrada primeiro fica na frente.
    selecionados = sorted(melhores.values(), key=lambda item: item[0])
    return sorted(selecionados, key=lambda item: item[1]["pontos"], reverse=True)
