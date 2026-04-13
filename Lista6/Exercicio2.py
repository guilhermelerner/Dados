import firebase_admin
from firebase_admin import credentials, auth

# 1. Inicialização (ajuste o caminho do seu JSON)
cred = credentials.Certificate(r"C:\Users\guiev\OneDrive\Documentos\CienciadeDados\Lista6\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

try:
    # 2. Criar novo usuário
    novo_usuario = auth.create_user(
        email='teste@exemplo.com',
        password='senhaSegura123'
    )
    print(f"Usuário criado com sucesso! UID: {novo_usuario.uid}")

    # 3. Buscar o usuário pelo UID
    usuario_buscado = auth.get_user(novo_usuario.uid)
    
    # 4. Imprimir informações
    print("--- Informações do Usuário ---")
    print(f"E-mail: {usuario_buscado.email}")
    print(f"UID: {usuario_buscado.uid}")
    print(f"Conta criada em: {usuario_buscado.user_metadata.creation_timestamp}")

except Exception as e:
    print(f"Erro: {e}")