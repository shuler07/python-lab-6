from random import seed

from src.cli import app
from src.constants import SEED


seed(SEED)

if __name__ == '__main__':
    "Entrypoint"
    app()
