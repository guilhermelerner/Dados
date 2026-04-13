class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def vender(self, quantidade):
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            print(f"Venda de {quantidade} {self.nome}(s) realizada.")
        else:
            print(f"Estoque insuficiente para vender {quantidade} unidades.")

    def repor(self, quantidade):
        self.estoque += quantidade
        print(f"Reposição de {quantidade} unidades feita.")

    def exibir_informacoes(self):
        print(f"Produto: {self.nome} | Preço: R${self.preco:.2f} | Estoque: {self.estoque}")

p = Produto("Mouse Gamer", 150.0, 10)
p.vender(3)
p.exibir_informacoes()