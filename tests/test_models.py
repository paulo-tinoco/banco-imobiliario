import pytest

from banco_imobiliario.models import Jogador, Perfil, Propriedade


@pytest.mark.parametrize(
    "perfil",
    [
        Perfil.IMPULSIVO,
        Perfil.EXIGENTE,
        Perfil.CAUTELOSO,
        Perfil.ALEATORIO,
    ],
)
def test_jogador_model(perfil: Perfil):
    jogador = Jogador(nome="Jogador", perfil=perfil)
    assert str(jogador) == "Jogador"
    assert jogador.nome == "Jogador"
    assert jogador.perfil == perfil
    assert jogador.saldo == 300
    assert jogador.posicao == 0
    assert jogador.propriedades == []
    assert jogador.falido is False


def test_propriedade_model():
    propriedade = Propriedade(nome="Propriedade")
    assert str(propriedade) == "Propriedade"
    assert propriedade.nome == "Propriedade"
    assert propriedade.valor >= 100
    assert propriedade.valor <= 200
    assert propriedade.aluguel >= 10
    assert propriedade.aluguel <= 20
    assert propriedade.posicao == 0
    assert propriedade.dono is None
