import collections

frase = "o computador é uma ferramenta mas o computador precisa de um programador"
palavras = frase.lower().split()
contagem = collections.Counter(palavras)

mais_comuns = contagem.most_common(3)

print("Contagem total:", dict(contagem))
print("As 3 mais frequentes:", mais_comuns)