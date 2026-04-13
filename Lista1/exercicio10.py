class Veiculo:
    def tipo_habilitacao(self):
        return "Habilitação genérica necessária."

class Carro(Veiculo):
    def tipo_habilitacao(self):
        return "Habilitação necessária: Categoria B"

class Moto(Veiculo):
    def tipo_habilitacao(self):
        return "Habilitação necessária: Categoria A"

veiculos = [Carro(), Moto()]
for v in veiculos:
    print(f"{type(v).__name__}: {v.tipo_habilitacao()}")