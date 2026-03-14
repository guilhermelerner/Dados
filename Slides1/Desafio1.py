import json
from datetime import datetime, timedelta

class Livro:
    def __init__(self, titulo, autor, isbn, disponivel=True):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponivel = disponivel

    def to_dict(self):
        return self.__dict__

class Usuario:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.livros_emprestados = [] 

    def to_dict(self):
        return self.__dict__

class Biblioteca:
    def __init__(self):
        self.livros = []
        self.usuarios = []
        self.carregar_dados()

    def adicionar_livro(self, livro):
        self.livros.append(livro)
        self.salvar_dados()

    def cadastrar_usuario(self, usuario):
        self.usuarios.append(usuario)
        self.salvar_dados()

    def buscar_livro(self, termo):
        return [l for l in self.livros if termo.lower() in l.titulo.lower() or termo == l.isbn]

    def emprestar_livro(self, isbn, cpf_usuario):
        try:
            livro = next((l for l in self.livros if l.isbn == isbn and l.disponivel), None)
            usuario = next((u for u in self.usuarios if u.cpf == cpf_usuario), None)

            if not livro:
                raise Exception("Livro não encontrado ou indisponível.")
            if not usuario:
                raise Exception("Usuário não cadastrado.")

            livro.disponivel = False
            prazo = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
            usuario.livros_emprestados.append({"isbn": isbn, "prazo": prazo})
            
            self.salvar_dados()
            print(f"Sucesso! Devolução até: {prazo}")
        except Exception as e:
            print(f"Erro: {e}")

    def salvar_dados(self):
        dados = {
            "livros": [l.to_dict() for l in self.livros],
            "usuarios": [u.to_dict() for u in self.usuarios]
        }
        with open("biblioteca.json", "w") as f:
            json.dump(dados, f, indent=4)

    def carregar_dados(self):
        try:
            with open("biblioteca.json", "r") as f:
                dados = json.load(f)
                self.livros = [Livro(**l) for l in dados["livros"]]
                for u_dados in dados["usuarios"]:
                    u = Usuario(u_dados["nome"], u_dados["cpf"])
                    u.livros_emprestados = u_dados["livros_emprestados"]
                    self.usuarios.append(u)
        except FileNotFoundError:
            pass

def menu():
    bib = Biblioteca()
    while True:
        print("\n--- SISTEMA DE BIBLIOTECA ---")
        print("1. Adicionar Livro\n2. Cadastrar Usuário\n3. Emprestar Livro\n4. Buscar Livro\n5. Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            t = input("Título: "); a = input("Autor: "); i = input("ISBN: ")
            bib.adicionar_livro(Livro(t, a, i))
        elif opcao == "2":
            n = input("Nome: "); c = input("CPF: ")
            bib.cadastrar_usuario(Usuario(n, c))
        elif opcao == "3":
            i = input("ISBN do Livro: "); c = input("CPF do Usuário: ")
            bib.emprestar_livro(i, c)
        elif opcao == "4":
            t = input("Termo de busca: ")
            resultados = bib.buscar_livro(t)
            for r in resultados:
                status = "Disponível" if r.disponivel else "Emprestado"
                print(f"[{status}] {r.titulo} - {r.autor} (ISBN: {r.isbn})")
        elif opcao == "5":
            break

if __name__ == "__main__":
    menu()