import firebase_admin
from firebase_admin import credentials, firestore

# 1. Inicialização (Use o 'r' antes das aspas para evitar aquele erro de novo)
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\guiev\OneDrive\Documentos\CienciadeDados\Lista6\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# 2. Instanciar o cliente do Firestore
db = firestore.client()

def atualizar_preco_produto(produto_id, novo_preco):
    try:
        # Referência para o documento na coleção 'produtos_mysql'
        doc_ref = db.collection("produtos_mysql").document(produto_id)
        
        # 3. Atualizar o campo 'preco'
        doc_ref.update({
            "preco": novo_preco
        })
        
        print(f"Sucesso! O produto {produto_id} agora custa R$ {novo_preco}")
        
    except Exception as e:
        print(f"Erro ao atualizar: {e}")

# --- TESTE DA FUNÇÃO ---
# Substitua 'ID_DO_PRODUTO' por um ID que você sabe que existe no seu Firestore
atualizar_preco_produto("T9driy8laU4AdLmKQLvO", 99.90)