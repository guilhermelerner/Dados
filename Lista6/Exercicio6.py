import firebase_admin
from firebase_admin import credentials, messaging

# 1. Inicialização 
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\guiev\OneDrive\Documentos\CienciadeDados\Lista6\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def enviar_notificacao_topico():
    try:
        # 2. Configurar a mensagem
        # Vamos enviar para um 'topic' em vez de um token específico
        topic = 'avisos'

        mensagem = messaging.Message(
            notification=messaging.Notification(
                title='Olá Guilherme!',
                body='Sua integração com Firebase Messaging funcionou! 🚀',
            ),
            topic=topic,
        )

        # 3. Enviar a mensagem
        response = messaging.send(mensagem)
        
        # Se imprimir o ID da mensagem, significa que o Firebase aceitou o envio
        print(f"Sucesso! Notificação enviada. ID da mensagem: {response}")

    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")

# Executar a simulação
enviar_notificacao_topico()