import random

from .models import Jogador, Perfil, Propriedade


class JogoHandler:
    propriedades: list[Propriedade] = []
    jogadores: list[Jogador] = []
    proximo_jogador = 0
    simulacoes = 300
    timeout = 1000

    def criar_jogador(self, nome: str, perfil: Perfil) -> Jogador:
        jogador = Jogador(nome=nome, perfil=perfil)
        self.jogadores.append(jogador)
        return jogador

    def criar_propriedade(self, nome: str, valor: int, aluguel: int) -> Propriedade:
        propriedade = Propriedade(nome=nome, valor=valor, aluguel=aluguel)
        self.propriedades.append(propriedade)
        return propriedade

    def add_propriedades_no_jogo(self) -> None:
        for i, propriedade in enumerate(self.propriedades, start=1):
            propriedade.posicao = i

    def comprar_propriedade(self, jogador: Jogador, propriedade: Propriedade) -> bool:
        comprou = False
        devo_comprar = {
            Perfil.IMPULSIVO: jogador.saldo >= propriedade.valor,
            Perfil.EXIGENTE: jogador.saldo >= propriedade.valor and propriedade.aluguel > 50,
            Perfil.CAUTELOSO: jogador.saldo >= propriedade.valor and jogador.saldo >= 80,
            Perfil.ALEATORIO: random.randint(0, 1),
        }
        if devo_comprar[jogador.perfil]:
            print(f"{jogador.nome} comprou a propriedade {propriedade.nome}")
            jogador.saldo -= propriedade.valor
            propriedade.dono = jogador
            jogador.propriedades.append(propriedade)
            comprou = True

        return comprou

    def pagar_aluguel(self, jogador: Jogador, propriedade: Propriedade) -> bool:
        pagou_aluguel = False
        if propriedade.dono != jogador:
            print(f"{jogador.nome} pagou aluguel para {propriedade.dono.nome}")
            jogador.saldo -= propriedade.aluguel
            propriedade.dono.saldo += propriedade.aluguel
            pagou_aluguel = True

        return pagou_aluguel

    def verificar_falencia(self, jogador: Jogador) -> None:
        jogador.falido = jogador.saldo < 0

    def verificar_vencedor(self) -> Jogador | None:
        vencedor = None
        saldo_anterior = 0

        for jogador in self.jogadores:
            if jogador.falido:
                continue
            elif vencedor and jogador.saldo > vencedor.saldo:
                vencedor = jogador
            elif vencedor and jogador.saldo == vencedor.saldo:
                vencedor = None
            elif not vencedor and not saldo_anterior:
                vencedor = jogador
            elif not vencedor and jogador.saldo > saldo_anterior:
                vencedor = jogador
            elif saldo_anterior and jogador.saldo == saldo_anterior:
                vencedor = None

        return vencedor

    def lista_perdedores(self) -> list[Jogador]:
        perdedores = []
        vencedor = self.verificar_vencedor()
        if vencedor:
            perdedores = list(filter(lambda jogador: jogador != vencedor, self.jogadores))

        return perdedores

    def verificar_empate(self):
        vencedor = self.verificar_vencedor()
        return True if not vencedor else False

    def todos_jogadores_falidos(self):
        return all(jogador.falido for jogador in self.jogadores)

    def todas_propriedades_compradas(self):
        return all(propriedade.dono for propriedade in self.propriedades)

    def verificar_fim_de_jogo(self):
        if self.todos_jogadores_falidos() or self.todas_propriedades_compradas():
            return True
        return False

    def jogar_dado(self):  # pragma: no cover
        return random.randint(1, 6)

    def selecionar_jogador_da_vez(self):
        if self.proximo_jogador >= len(self.jogadores):
            self.proximo_jogador = 0

        jogador = self.jogadores[self.proximo_jogador]
        self.proximo_jogador += 1
        return jogador

    def jogar(self, simulacao: int = 1) -> None:  # pragma: no cover
        for rodada in range(1, self.timeout + 1):
            jogador = self.selecionar_jogador_da_vez()
            if jogador.falido:
                continue
            dado = self.jogar_dado()
            jogador.posicao += dado
            if jogador.posicao > len(self.propriedades):
                jogador.posicao -= len(self.propriedades)
                jogador.saldo += 100
            propriedade = self.propriedades[jogador.posicao - 1]
            if propriedade.dono:
                self.pagar_aluguel(jogador, propriedade)
            else:
                self.comprar_propriedade(jogador, propriedade)
            self.verificar_falencia(jogador)
            if self.verificar_fim_de_jogo():
                break
        return (self.verificar_vencedor(), self.lista_perdedores(), rodada)
