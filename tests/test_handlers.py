import pytest

from banco_imobiliario.handlers import JogoHandler
from banco_imobiliario.models import Jogador, Perfil, Propriedade


@pytest.fixture
def jogo():
    jogo = JogoHandler()
    jogo.jogadores = []
    jogo.propriedades = []
    return jogo


@pytest.mark.parametrize(
    "perfil",
    [
        Perfil.IMPULSIVO,
        Perfil.EXIGENTE,
        Perfil.CAUTELOSO,
        Perfil.ALEATORIO,
    ],
)
def test_jogo_metodo_criar_jogador(jogo: JogoHandler, perfil: Perfil):
    jogo.criar_jogador("Jogador", perfil)
    assert len(jogo.jogadores) == 1
    assert jogo.jogadores[0].nome == "Jogador"
    assert jogo.jogadores[0].perfil == perfil


def test_jogo_metodo_criar_propriedade(jogo: JogoHandler):
    jogo.criar_propriedade("Propriedade", 100, 10)
    assert len(jogo.propriedades) == 1
    assert jogo.propriedades[0].nome == "Propriedade"
    assert jogo.propriedades[0].valor == 100
    assert jogo.propriedades[0].aluguel == 10


def test_jogo_metodo_add_propriedades_no_jogo(jogo: JogoHandler):
    for i in range(20):
        jogo.criar_propriedade(f"Propriedade {i}", 100, 10)

    jogo.add_propriedades_no_jogo()
    for i, propriedade in enumerate(jogo.propriedades, start=1):
        assert propriedade.posicao == i


def test_jogo_metodo_comprar_propriedade(jogo: JogoHandler):
    jogo.criar_jogador("Jogador", Perfil.IMPULSIVO)
    jogo.criar_propriedade("Propriedade", 100, 10)
    jogo.add_propriedades_no_jogo()
    jogador = jogo.jogadores[0]
    propriedade = jogo.propriedades[0]
    jogador.saldo = 1000
    jogo.comprar_propriedade(jogador, propriedade)
    assert jogador.saldo == 900
    assert propriedade.dono.__eq__(jogador)
    assert propriedade in jogador.propriedades


@pytest.mark.parametrize(
    "jogador_posicao, saldo, expected",
    [
        (0, 300, False),
        (1, 290, True),
        (2, 290, True),
        (3, 290, True),
    ],
    ids=Perfil._member_map_.keys(),
)
def test_jogo_metodo_pagar_aluguel(
    jogo: JogoHandler,
    jogador_posicao: int,
    saldo: int,
    expected: bool,
):
    [jogo.criar_jogador(f"Jogador {perfil}", perfil) for perfil in Perfil]
    jogo.criar_propriedade("Propriedade", 100, 10)
    propriedade = jogo.propriedades[0]
    propriedade.dono = jogo.jogadores[0]
    jogador = jogo.jogadores[jogador_posicao]
    jogo.pagar_aluguel(jogador, propriedade)

    assert jogador.saldo == saldo


@pytest.mark.parametrize(
    "saldo, expected",
    [
        (1, False),
        (0, False),
        (-1, True),
    ],
)
def test_jogo_metodo_verificar_falencia(jogo: JogoHandler, saldo: int, expected: bool):
    jogo.criar_jogador("Jogador", Perfil.IMPULSIVO)
    jogador = jogo.jogadores[0]
    jogador.saldo = saldo
    jogo.verificar_falencia(jogador)
    assert jogador.falido == expected


@pytest.mark.parametrize(
    "jogadores, expected",
    [
        (
            [
                Jogador(nome="Jogador 1", saldo=100, falido=False),
                Jogador(nome="Jogador 2", saldo=-1, falido=True),
            ],
            Jogador(nome="Jogador 1", saldo=100, falido=False),
        ),
        (
            [
                Jogador(nome="Jogador 1", saldo=100, falido=False),
                Jogador(nome="Jogador 2", saldo=101, falido=False),
            ],
            Jogador(nome="Jogador 2", saldo=101, falido=False),
        ),
        (
            [
                Jogador(nome="Jogador 1", saldo=-1, falido=True),
                Jogador(nome="Jogador 2", saldo=-1, falido=True),
            ],
            None,
        ),
    ],
    ids=["Jogador 1 vence", "Jogador 2 vence", "Todos falidos"],
)
def test_jogo_metodo_verificar_vencedor(jogo: JogoHandler, jogadores: list, expected: Jogador):
    jogo.jogadores = jogadores
    assert jogo.verificar_vencedor() == expected


@pytest.mark.parametrize(
    "jogadores, expected",
    [
        (
            [
                Jogador(nome="Jogador 1", saldo=100, falido=False),
                Jogador(nome="Jogador 2", saldo=-1, falido=True),
            ],
            [Jogador(nome="Jogador 2", saldo=-1, falido=True)],
        ),
        (
            [
                Jogador(nome="Jogador 1", saldo=100, falido=False),
                Jogador(nome="Jogador 2", saldo=101, falido=False),
            ],
            [Jogador(nome="Jogador 1", saldo=100, falido=False)],
        ),
        (
            [
                Jogador(nome="Jogador 1", saldo=-1, falido=True),
                Jogador(nome="Jogador 2", saldo=-1, falido=True),
            ],
            [],
        ),
    ],
    ids=["Jogador 1 vence", "Jogador 2 vence", "Todos falidos"],
)
def test_jogo_metodo_lista_perdedores(jogo: JogoHandler, jogadores: list, expected: Jogador):
    jogo.jogadores = jogadores
    assert jogo.lista_perdedores() == expected


@pytest.mark.parametrize(
    "jogadores, expected",
    [
        (
            [
                Jogador(nome="Jogador 1", saldo=100, falido=False),
                Jogador(nome="Jogador 2", saldo=-1, falido=True),
            ],
            False,
        ),
        (
            [
                Jogador(nome="Jogador 1", saldo=100, falido=False),
                Jogador(nome="Jogador 2", saldo=100, falido=False),
            ],
            True,
        ),
        (
            [
                Jogador(nome="Jogador 1", saldo=-1, falido=True),
                Jogador(nome="Jogador 2", saldo=-1, falido=True),
            ],
            True,
        ),
    ],
    ids=["Nao houve empate", "Jogadores Empatados", "Todos falidos"],
)
def test_jogo_metodo_verificar_empate(jogo: JogoHandler, jogadores: list, expected: Jogador):
    jogo.jogadores = jogadores
    assert jogo.verificar_empate() == expected


@pytest.mark.parametrize(
    "jogadores, expected",
    [
        (
            [
                Jogador(nome="Jogador 1", saldo=100, falido=False),
                Jogador(nome="Jogador 2", saldo=-1, falido=True),
            ],
            False,
        ),
        (
            [
                Jogador(nome="Jogador 1", saldo=100, falido=False),
                Jogador(nome="Jogador 2", saldo=100, falido=False),
            ],
            False,
        ),
        (
            [
                Jogador(nome="Jogador 1", saldo=-1, falido=True),
                Jogador(nome="Jogador 2", saldo=-1, falido=True),
            ],
            True,
        ),
    ],
    ids=["Um falido", "Nenhum falido", "Todos falidos"],
)
def test_jogo_metodo_todos_jogadores_falidos(jogo: JogoHandler, jogadores: list, expected: Jogador):
    jogo.jogadores = jogadores
    assert jogo.todos_jogadores_falidos() == expected


@pytest.mark.parametrize(
    "propriedades, expected",
    [
        (
            [
                Propriedade(
                    nome="Propriedade 1",
                    preco=100,
                    aluguel=10,
                    dono=Jogador(nome="Jogador 1", saldo=100, falido=False),
                ),
                Propriedade(
                    nome="Propriedade 2",
                    preco=100,
                    aluguel=10,
                    dono=Jogador(nome="Jogador 1", saldo=100, falido=False),
                ),
            ],
            True,
        ),
        (
            [
                Propriedade(
                    nome="Propriedade 1",
                    preco=100,
                    aluguel=10,
                    dono=None,
                ),
                Propriedade(
                    nome="Propriedade 2",
                    preco=100,
                    aluguel=10,
                    dono=Jogador(nome="Jogador 1", saldo=100, falido=False),
                ),
            ],
            False,
        ),
        (
            [
                Propriedade(
                    nome="Propriedade 1",
                    preco=100,
                    aluguel=10,
                    dono=Jogador(nome="Jogador 1", saldo=100, falido=False),
                ),
                Propriedade(
                    nome="Propriedade 2",
                    preco=100,
                    aluguel=10,
                    dono=None,
                ),
            ],
            False,
        ),
        (
            [
                Propriedade(
                    nome="Propriedade 1",
                    preco=100,
                    aluguel=10,
                    dono=None,
                ),
                Propriedade(
                    nome="Propriedade 2",
                    preco=100,
                    aluguel=10,
                    dono=None,
                ),
            ],
            False,
        ),
    ],
    ids=[
        "Propriedades com dono",
        "Propriedade 1 sem dono",
        "Propriedade 2 sem dono",
        "Propriedades sem dono",
    ],
)
def test_jogo_metodo_todas_propriedades_compradas(jogo: JogoHandler, propriedades: list, expected: Jogador):
    jogo.propriedades = propriedades
    assert jogo.todas_propriedades_compradas() == expected


@pytest.mark.parametrize(
    "todos_jogadores_falidos, todas_propriedades_compradas, expected",
    [
        (False, False, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    ],
)
def test_jogo_metodo_verificar_fim_de_jogo(
    jogo: JogoHandler,
    todos_jogadores_falidos: bool,
    todas_propriedades_compradas: bool,
    expected: bool,
):
    jogo.todos_jogadores_falidos = lambda: todos_jogadores_falidos
    jogo.todas_propriedades_compradas = lambda: todas_propriedades_compradas
    assert jogo.verificar_fim_de_jogo() == expected
