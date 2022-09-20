import random
from enum import Enum

from pydantic import BaseModel


class Perfil(Enum):
    IMPULSIVO = "Impulsivo"
    EXIGENTE = "Exigente"
    CAUTELOSO = "Cauteloso"
    ALEATORIO = "Aleatório"


class Jogador(BaseModel):
    nome: str
    perfil: Perfil = random.choice(list(Perfil))
    saldo: int = 300
    posicao: int = 0
    propriedades: list = []
    falido = False

    def __str__(self):
        return self.nome

    def __eq__(self, other):
        return (
            self.nome == other.nome
            and self.perfil == other.perfil
            and self.saldo == other.saldo
            and self.posicao == other.posicao
            and self.propriedades == other.propriedades
            and self.falido == other.falido
        )


class Propriedade(BaseModel):
    nome: str
    valor: int = random.randint(100, 200)
    aluguel: int = random.randint(10, 20)
    posicao: int = 0
    dono: Jogador = None

    def __str__(self):
        return self.nome
