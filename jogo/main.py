import runpy
import sys
from pathlib import Path


def main():
    # O atalho antigo abre a versão atual do jogo.
    pasta_jogo = Path(__file__).resolve().parent.parent / "highway_rush"
    sys.path.insert(0, str(pasta_jogo))
    try:
        runpy.run_path(str(pasta_jogo / "main.py"), run_name="__main__")
    finally:
        sys.path.pop(0)


if __name__ == "__main__":
    main()
