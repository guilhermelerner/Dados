import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate(r"C:\Users\guiev\OneDrive\Documentos\CienciadeDados\Lista6\serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

print(f"Sucesso! App inicializado: {app.name}")