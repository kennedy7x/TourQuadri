from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
csrf = CSRFProtect()

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'tourquadri@gmail.com')


def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__, instance_relative_config=True)

    if not os.path.exists(app.instance_path):
        try:
            os.makedirs(app.instance_path)
            print(f"✅ Pasta instance criada em: {app.instance_path}")
        except Exception as e:
            print(f"❌ Erro ao criar pasta instance: {e}")

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tourquadri_secret_v2')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, "tourquadri.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'tourquadri@gmail.com')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME', 'tourquadri@gmail.com')

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from tourquadri.controllers import registrar_rotas
    registrar_rotas(app)

    @app.context_processor
    def inject_globals():
        from tourquadri.models import ROTEIROS
        return {'ROTEIROS': ROTEIROS}

    with app.app_context():
        db.create_all()
        _criar_admin_inicial()
        _criar_maquinas_padrao()

    # ============================================================
    # INICIA O SCHEDULER EM BACKGROUND (apenas se não estiver em modo debug reloader)
    # ============================================================
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        from tourquadri.scheduler import iniciar_scheduler
        iniciar_scheduler(app)

    return app


def _criar_admin_inicial():
    from tourquadri.models import Usuario
    admin = Usuario.query.filter_by(email=ADMIN_EMAIL).first()
    if not admin:
        admin = Usuario(
            nome="Administrador",
            telefone="(11) 99999-9999",
            email=ADMIN_EMAIL,
            admin=True,
            email_verificado=True
        )
        admin.senha_criptografada = "admin123"
        db.session.add(admin)
        db.session.commit()
        print("✅ Administrador criado com sucesso!")


def _criar_maquinas_padrao():
    from tourquadri.models import Maquina
    if Maquina.query.count() == 0:
        maquinas_config = [
            ("Máquina 0", "Buggy 2026", "200cc"),
            ("Máquina 1", "Can-Am 2026", "650cc"),
            ("Máquina 2", "Ventura 500 Pro Max 2026", "500cc"),
            ("Máquina 3", "Ventura 500 Pro Max 2026", "500cc"),
            ("Máquina 4", "Ventura 500 Pro Max 2026", "500cc"),
            ("Máquina 5", "Ventura 500 Pro Max 2026", "500cc"),
            ("Máquina 6", "Can-Am 2014", "400cc"),
            ("Máquina 7", "Can-Am 2014", "400cc"),
            ("Máquina 8", "Can-Am 2014", "400cc"),
            ("Máquina 9", "Can-Am 2014", "400cc"),
            ("Máquina 10", "Can-Am 2014", "400cc"),
            ("Máquina 11", "Can-Am 2014", "400cc"),
            ("Máquina 12", "Can-Am 2014", "400cc"),
            ("Máquina 13", "Can-Am 2014", "400cc"),
            ("Máquina 14", "Can-Am 2014", "400cc"),
        ]

        for nome_maquina, modelo, cc in maquinas_config:
            maquina = Maquina(nome_maquina=nome_maquina, modelo=modelo, cc=cc)
            db.session.add(maquina)

        db.session.commit()
        print(f"✅ {Maquina.query.count()} máquinas padrão criadas (IDs 0 a 14)!")