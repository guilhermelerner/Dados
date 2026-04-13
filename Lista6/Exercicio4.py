import firebase_admin
from firebase_admin import credentials, firestore
# Importamos o 'FieldFilter' para resolver o aviso do Google
from google.cloud.firestore_v1.base_query import FieldFilter

if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\guiev\OneDrive\Documentos\CienciadeDados\Lista6\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def consultar_produtos_caros(preco_minimo):
    try:
        produtos_ref = db.collection("produtos_mysql")
        
        # Nova forma de fazer o filtro para não dar o aviso (UserWarning)
        query = produtos_ref.where(filter=FieldFilter("preco", ">", preco_minimo))
        
        resultados = query.stream()
        
        print(f"\n--- Produtos com valor acima de {preco_minimo} ---")
        
        for doc in resultados:
            dados = doc.to_dict()
            # .get() ajuda a não dar erro se o campo não existir
            nome = dados.get("nome") or dados.get("Nome") or "Sem nome cadastrado"
            preco = dados.get("preco", 0.0)
            
            print(f"ID: {doc.id} | Nome: {nome} | Preco: {preco}")

    except Exception as e:
        print(f"Erro: {e}")

consultar_produtos_caros(15.00)