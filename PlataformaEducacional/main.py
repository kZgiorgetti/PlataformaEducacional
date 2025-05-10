import json
import os
import hashlib
import platform
from statistics import mean

USERS_FILE = "usuarios.json"

QUESTOES = [
    {"pergunta": "Quantos números pares há entre 1 e 10?", "resposta": "5"},
    {"pergunta": "Qual é o resultado de 2 + 2 * 2?", "resposta": "6"},
    {"pergunta": "Qual é a capital do Brasil?", "resposta": "Brasília"},
    {"pergunta": "Qual linguagem usamos neste programa?", "resposta": "Python"},
    {"pergunta": "Qual é o número binário de 2?", "resposta": "10"},
    {"pergunta": "Quanto é 10 dividido por 2?", "resposta": "5"},
    {"pergunta": "Qual operador usamos para comparar igualdade em Python?", "resposta": "=="},
    {"pergunta": "Qual é o valor booleano de 0 em Python?", "resposta": "False"},
    {"pergunta": "Quantos bits tem 1 byte?", "resposta": "8"},
    {"pergunta": "Qual comando usamos para imprimir algo na tela em Python?", "resposta": "print"},
]

def carregar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(USERS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def cadastrar_usuario():
    nome = input("Nome completo: ")
    email = input("Email: ")
    senha = input("Senha: ")
    senha_hash = hash_senha(senha)
    usuarios = carregar_usuarios()
    usuarios.append({
        "nome": nome,
        "email": email,
        "senha": senha_hash,
        "desempenho": []
    })
    salvar_usuarios(usuarios)
    print("Cadastro realizado com sucesso!")

def login():
    email = input("Email: ")
    senha = input("Senha: ")
    senha_hash = hash_senha(senha)
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha_hash:
            print(f"\nBem-vindo(a), {usuario['nome']}!")
            return usuario
    print("Login inválido.")
    return None

def acessar_conteudo():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(base_dir, "conteudos", "logica_basica.txt")

    while True:
        print("\n=== Acessar Conteúdo Educacional ===")
        print("1. Abrir 'Lógica Básica'")
        print("2. Voltar ao menu")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            if not os.path.exists(caminho_arquivo):
                print(f"Arquivo não encontrado no caminho: {caminho_arquivo}")
                continue
            try:
                sistema = platform.system()
                if sistema == "Windows":
                    os.startfile(caminho_arquivo)
                elif sistema == "Darwin":
                    os.system(f"open '{caminho_arquivo}'")
                elif sistema == "Linux":
                    os.system(f"xdg-open '{caminho_arquivo}'")
                else:
                    print("Sistema não suportado.")
            except Exception as e:
                print(f"Erro ao abrir o arquivo: {e}")
        elif opcao == "2":
            break
        else:
            print("Opção inválida. Tente novamente.")

def atualizar_usuario(usuario_atualizado):
    usuarios = carregar_usuarios()
    for i, usuario in enumerate(usuarios):
        if usuario["email"] == usuario_atualizado["email"]:
            usuarios[i] = usuario_atualizado
            break
    salvar_usuarios(usuarios)

def avaliar_usuario(usuario):
    print("\n📊 Exercício de lógica:")
    perguntas = [
        ("Quantos números pares há entre 1 e 10?", "5"),
        ("Qual o resultado de 3 + 4?", "7"),
        ("Se um número é par e menor que 5, qual pode ser?", "2"),
        ("Qual é o valor de 2 * 3?", "6"),
        ("Se hoje é segunda, que dia será depois de dois dias?", "quarta"),
        ("Quanto é 10 dividido por 2?", "5"),
        ("Qual o número ímpar entre 4, 6, 7 e 8?", "7"),
        ("Quanto é 9 - 3?", "6"),
        ("Qual o resultado de 2 elevado ao quadrado?", "4"),
        ("Quantos lados tem um triângulo?", "3")
    ]

    acertos = 0
    for i, (pergunta, resposta_correta) in enumerate(perguntas, 1):
        resposta = input(f"{i}. {pergunta} ").strip().lower()
        if resposta == resposta_correta:
            print("✔️ Correto!")
            acertos += 1
        else:
            print(f"❌ Incorreto. Resposta correta: {resposta_correta}")

    print(f"\nVocê acertou {acertos} de {len(perguntas)} questões.")
    usuario["desempenho"].append(acertos)

    # Atualiza a média no próprio JSON
    usuario["media"] = round(mean(usuario["desempenho"]), 2)
    atualizar_usuario(usuario)

def gerar_relatorio():
    usuarios = carregar_usuarios()
    print("\n📈 Relatório de Desempenho:")
    for usuario in usuarios:
        notas = usuario.get("desempenho", [])
        media = mean(notas) if notas else 0
        print(f"- {usuario['nome']}: {len(notas)} avaliações | Média: {media:.2f}")

def menu_principal():
    while True:
        print("\n=== Plataforma Educacional Segura ===")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("3. Relatório geral")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            usuario = login()
            if usuario:
                menu_usuario(usuario)
        elif opcao == "3":
            gerar_relatorio()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_usuario(usuario):
    while True:
        print("\n=== Menu do Usuário ===")
        print("1. Acessar conteúdo")
        print("2. Fazer avaliação")
        print("0. Logout")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            acessar_conteudo()
        elif opcao == "2":
            avaliar_usuario(usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
