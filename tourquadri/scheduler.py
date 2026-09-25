"""
Job em background que roda a cada 5 minutos verificando
se algum email de avaliação precisa ser enviado.
"""
import threading
import time


def iniciar_scheduler(app):
    """
    Inicia uma thread em background que roda o job a cada 5 minutos.
    Deve ser chamada uma única vez, no create_app().
    """
    def run():
        # Espera 30 segundos antes de começar (pra dar tempo do app subir)
        time.sleep(30)

        while True:
            try:
                with app.app_context():
                    from tourquadri.services import AgendamentoService
                    service = AgendamentoService()
                    service.processar_emails_pendentes()
            except Exception as e:
                print(f"⚠️ Erro no scheduler: {e}")

            # Aguarda 5 minutos antes de rodar de novo
            time.sleep(300)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    print("✅ Scheduler de emails iniciado (roda a cada 5 min)")