import random

from .handlers import JogoHandler
from .models import Perfil

jogo = JogoHandler()

vitoria_perfis = {
    "IMPULSIVO": 0,
    "EXIGENTE": 0,
    "CAUTELOSO": 0,
    "ALEATORIO": 0,
}
timeout = 0
total_rodadas = 0
perfil_que_mais_venceu = None
for simulacao in range(jogo.simulacoes):
    # Cria propriedades
    for i in range(20):
        jogo.criar_propriedade(f"Propriedade {i}", random.randint(100, 200), random.randint(10, 60))

    # adiciona 4 jogadores ao tabuleiro
    for perfil in Perfil:
        jogo.criar_jogador(f"Jogador {perfil}", perfil)

    # adiciona as propriedades ao tabuleiro
    jogo.add_propriedades_no_jogo()

    # inicia o jogo
    vencedor, perdedor, rodadas = jogo.jogar(simulacao)

    # verifica quem venceu
    if vencedor:
        vitoria_perfis[vencedor.perfil.name] += 1

    total_rodadas += rodadas

    # verifica se houve timeout
    if rodadas == jogo.timeout:
        timeout += 1

print(f"O perfil que mais venceu foi {max(vitoria_perfis, key=vitoria_perfis.get)}")
print(f"O timeout ocorreu {timeout} vezes")
print(f"A média de rodadas foi {round(total_rodadas / jogo.simulacoes)}")
for perfil, vitorias in vitoria_perfis.items():
    print(f"O perfil {perfil} venceu {vitorias / jogo.simulacoes * 100:.2f}%")
