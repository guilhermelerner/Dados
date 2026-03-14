agenda = {
    "Ana": "(10) 99999-1111",
    "Guilherme": "(10) 98888-2222",
    "Bento": "(10) 97777-3333",
    "Aurora": "(10) 98989-3333"
}

nome_busca = input("Digite o nome que deseja buscar: ").capitalize()

telefone = agenda.get(nome_busca, "Contato não encontrado.")

print(f"Resultado: {telefone}")
