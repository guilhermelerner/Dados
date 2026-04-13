import firebase_admin
from firebase_admin import credentials, auth, exceptions # Importamos o módulo de exceções

# 1. Inicialização segura
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(r"C:\Users\guiev\OneDrive\Documentos\CienciadeDados\Lista6\serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Erro crítico ao carregar credenciais: {e}")
    exit() # Encerra o script se não conseguir conectar

def gerenciar_usuario_seguro(email, senha):
    try:
        print(f"Tentando criar o usuário: {email}...")
        user = auth.create_user(email=email, password=senha)
        print(f"Usuário criado com sucesso! UID: {user.uid}")

    except exceptions.AlreadyExistsError:
        print(f"Erro: O e-mail '{email}' já está sendo usado por outra conta.")
        
    except exceptions.InvalidArgumentError:
        print("Erro: Os dados fornecidos são inválidos (ex: senha muito curta).")
        
    except exceptions.FirebaseError as e:
        # Captura qualquer outro erro específico do Firebase
        print(f"Erro geral do Firebase: {e.code} - {e.message}")
        
    except Exception as e:
        # Captura erros comuns do Python 
        print(f"Erro inesperado no Python: {e}")

# Tente rodar o mesmo e-mail duas vezes para ver o "AlreadyExistsError" em ação!
gerenciar_usuario_seguro("aluno_teste@unicentro.br", "senhaForte123")