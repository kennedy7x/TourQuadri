import json
from datetime import datetime
from tourquadri import db, bcrypt

# ==========================
# ROTEIROS (dicionário fixo)
# ==========================

ROTEIROS = {
    "1": {
        "nome": "Cachoeira Véu da Noiva",
        "duracao": 40,
        "preco": "R$ 200,00",
        "preco_max": "R$ 200,00",
        "tipo": "Fácil",
        "paradas": "1 parada para fotos",
        "descricao_curta": "Passeio de 30 a 40 minutos com 1 parada para fotos",
        "descricao_completa": "Um passeio curto e encantador até a Cachoeira Véu da Noiva. Ideal para quem quer conhecer a região sem passar muito tempo na trilha. Inclui parada para fotos na cachoeira e degustação de chocolates, cachaça e licores.",
        "inclui": [
            "Passeio de quadriciclo",
            "1 parada para fotos na Cachoeira Véu da Noiva",
            "Degustação de chocolates, cachaça e licores",
            "Equipamento de segurança",
            "Guia especializado"
        ],
        "foto_principal": "cachoeira.jpg",
        "galeria": ["cachoeira_1.jpg", "cachoeira_2.jpg", "cachoeira_3.jpg"]
    },
    "2": {
        "nome": "Mirante Pedra do Fogo",
        "duracao": 60,
        "preco": "R$ 260,00",
        "preco_max": "R$ 260,00",
        "tipo": "Fácil",
        "paradas": "1 parada para fotos",
        "descricao_curta": "Passeio de 1 hora com 1 parada para fotos",
        "descricao_completa": "Passeio de 1 hora até o Mirante Pedra do Fogo, um dos pontos mais bonitos da região. Vista de tirar o fôlego e parada garantida para fotos inesquecíveis.",
        "inclui": [
            "Passeio de quadriciclo",
            "1 parada para fotos no Mirante Pedra do Fogo",
            "Equipamento de segurança",
            "Guia especializado"
        ],
        "foto_principal": "mirante.jpg",
        "galeria": ["mirante_1.jpg", "mirante_2.jpg", "mirante_3.jpg"]
    },
    "3": {
        "nome": "Mirante da Ferradura",
        "duracao": 60,
        "preco": "R$ 260,00",
        "preco_max": "R$ 260,00",
        "tipo": "Fácil",
        "paradas": "1 parada para fotos",
        "descricao_curta": "Passeio de 1 hora com 1 parada para fotos",
        "descricao_completa": "Passeio de 1 hora até o Mirante da Ferradura, com vista panorâmica incrível da região. Parada para fotos e contato direto com a natureza.",
        "inclui": [
            "Passeio de quadriciclo",
            "1 parada para fotos no Mirante da Ferradura",
            "Equipamento de segurança",
            "Guia especializado"
        ],
        "foto_principal": "ferradura.jpg",
        "galeria": ["ferradura_1.jpg", "ferradura_2.jpg", "ferradura_3.jpg"]
    },
    "4": {
        "nome": "Mirante + Cachoeira",
        "duracao": 90,
        "preco": "R$ 320,00",
        "preco_max": "R$ 320,00",
        "tipo": "Fácil",
        "paradas": "2 paradas para fotos",
        "descricao_curta": "Passeio de 1h30 com 2 paradas para fotos",
        "descricao_completa": "Combinamos o melhor dos dois mundos em 1h30 de aventura: Mirante Pedra do Fogo + Cachoeira Véu da Noiva. Duas paradas para fotos e paisagens de tirar o fôlego.",
        "inclui": [
            "Passeio de quadriciclo",
            "2 paradas para fotos (Mirante Pedra do Fogo + Cachoeira Véu da Noiva)",
            "Equipamento de segurança",
            "Guia especializado"
        ],
        "foto_principal": "mirante_e_cachoeira.jpg",
        "galeria": ["mirante_e_cachoeira_1.jpg", "mirante_e_cachoeira_2.jpg", "mirante_e_cachoeira_3.jpg"]
    },
    "5": {
        "nome": "Cachoeira + Pico do Imbiri",
        "duracao": 120,
        "preco": "R$ 400,00",
        "preco_max": "R$ 400,00",
        "tipo": "Moderado",
        "paradas": "2 paradas para fotos",
        "descricao_curta": "Passeio de 2 horas com 2 paradas para fotos",
        "descricao_completa": "Uma aventura de 2 horas que combina duas paradas imperdíveis: a Cachoeira Véu da Noiva e o Pico do Imbiri, a 1.890 metros de altitude. Do alto, uma vista incrível da Serra da Mantiqueira que vai marcar sua viagem.",
        "inclui": [
            "Passeio de quadriciclo",
            "Parada na Cachoeira Véu da Noiva",
            "Parada no Pico do Imbiri (1.890m de altitude)",
            "Vista incrível da Serra da Mantiqueira",
            "Equipamento de segurança",
            "Guia especializado"
        ],
        "foto_principal": "cachoeira_e_imbiri.jpg",
        "galeria": ["cachoeira_e_imbiri_1.jpg", "cachoeira_e_imbiri_2.jpg", "cachoeira_e_imbiri_3.jpg"]
    },
    "6": {
        "nome": "Pôr do Sol no Pico do Baú",
        "duracao": 130,
        "preco": "R$ 450,00",
        "preco_max": "R$ 450,00",
        "tipo": "Fácil",
        "paradas": "1 parada para fotos",
        "descricao_curta": "Passeio de 2h a 2h30 com experiência completa ao pôr do sol",
        "descricao_completa": "Nossa experiência mais especial! Duração de 2h a 2h30 com fogueira, balanço para fotos, aperitivos, 1 taça de vinho por casal, água com e sem gás e marshmallow para a fogueira. Um pôr do sol inesquecível no Pico do Baú com todo o conforto e romance.",
        "inclui": [
            "Passeio de quadriciclo (2h a 2h30)",
            "Fogueira",
            "Balanço para fotos",
            "Aperitivos",
            "1 taça de vinho por casal para brindar o momento",
            "Água com e sem gás",
            "Marshmallow para a fogueira",
            "Equipamento de segurança",
            "Guia especializado"
        ],
        "foto_principal": "por_do_sol.jpg",
        "galeria": ["por_do_sol_1.jpg", "por_do_sol_2.jpg", "por_do_sol_3.jpg"]
    },
    "7": {
        "nome": "Almoço na Truticultura",
        "duracao": 180,
        "preco": "R$ 500,00",
        "preco_max": "R$ 500,00",
        "tipo": "Fácil",
        "paradas": "2 paradas para fotos",
        "descricao_curta": "Passeio de 3 horas com 2 paradas e almoço incluso",
        "descricao_completa": "Uma experiência completa que une aventura e gastronomia. Passeio de quadriciclo de 3 horas com 2 paradas para fotos e almoço incluso na truticultura, onde você pode saborear a famosa truta da região preparada de diversas formas.",
        "inclui": [
            "Passeio de quadriciclo (3 horas)",
            "2 paradas para fotos",
            "Almoço incluso na truticultura",
            "Equipamento de segurança",
            "Guia especializado"
        ],
        "foto_principal": "almoco.jpg",
        "galeria": ["almoco_1.jpg", "almoco_2.jpg", "almoco_3.jpg"]
    },
    "8": {
        "nome": "Pico do Itapeva",
        "duracao": 180,
        "preco": "R$ 600,00",
        "preco_max": "R$ 600,00",
        "tipo": "Moderado",
        "paradas": "3 paradas para fotos",
        "descricao_curta": "Passeio de 3 horas com 3 paradas para fotos",
        "descricao_completa": "Uma aventura de 3 horas até um dos mirantes mais altos do Brasil: o Pico do Itapeva. Com 3 paradas para fotos ao longo do caminho, é o passeio perfeito para quem quer explorar a região a fundo e registrar paisagens únicas.",
        "inclui": [
            "Passeio de quadriciclo (3 horas)",
            "3 paradas para fotos",
            "Visita a um dos mirantes mais altos do Brasil",
            "Equipamento de segurança",
            "Guia especializado"
        ],
        "foto_principal": "itapeva.jpg",
        "galeria": ["itapeva_1.jpg", "itapeva_2.jpg", "itapeva_3.jpg"]
    }
}


# ==========================
# CLASSES DO BANCO DE DADOS
# ==========================

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    email_verificado = db.Column(db.Boolean, default=False)
    # Programa de fidelidade
    passeios_realizados = db.Column(db.Integer, default=0)
    desconto_disponivel = db.Column(db.Boolean, default=False)

    @property
    def senha_criptografada(self):
        raise AttributeError('A senha não pode ser lida diretamente')

    @senha_criptografada.setter
    def senha_criptografada(self, senha_texto):
        self.senha = bcrypt.generate_password_hash(senha_texto).decode('utf-8')

    def verificar_senha(self, senha_texto):
        return bcrypt.check_password_hash(self.senha, senha_texto)


class Maquina(db.Model):
    __tablename__ = 'maquinas'

    id = db.Column(db.Integer, primary_key=True)
    nome_maquina = db.Column(db.String(100), nullable=False, default="Máquina")
    modelo = db.Column(db.String(50), nullable=False)
    cc = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome_maquina': self.nome_maquina,
            'modelo': self.modelo,
            'cc': self.cc
        }


class Agendamento(db.Model):
    __tablename__ = 'agendamentos'

    id = db.Column(db.String(36), primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    usuario_admin = db.Column(db.String(100), nullable=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    nome_cliente = db.Column(db.String(100), nullable=False)
    telefone_cliente = db.Column(db.String(20), nullable=False)
    email_cliente = db.Column(db.String(100), nullable=False)
    maquinas_json = db.Column(db.Text, nullable=False)
    data = db.Column(db.String(10), nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    roteiro = db.Column(db.String(10), nullable=False)
    duracao = db.Column(db.Integer, default=60)
    data_criacao = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(20), default='agendado')
    criado_por_admin = db.Column(db.Boolean, default=False)
    data_inicio = db.Column(db.String(30), nullable=True)
    data_finalizacao = db.Column(db.String(30), nullable=True)
    cancelado_por = db.Column(db.String(20), nullable=True)
    data_cancelamento = db.Column(db.String(30), nullable=True)
    email_avaliacao_agendado = db.Column(db.Boolean, default=False)
    email_avaliacao_enviado = db.Column(db.Boolean, default=False)
    data_agendada_envio = db.Column(db.String(30), nullable=True)
    # Programa de fidelidade
    desconto_aplicado = db.Column(db.Boolean, default=False)

    @property
    def maquinas(self):
        try:
            return json.loads(self.maquinas_json)
        except:
            return []

    @maquinas.setter
    def maquinas(self, valor):
        self.maquinas_json = json.dumps(valor)


class Bloqueio(db.Model):
    __tablename__ = 'bloqueios'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), nullable=False)
    horario = db.Column(db.String(5), nullable=False)
    __table_args__ = (db.UniqueConstraint('data', 'horario', name='_data_horario_uc'),)


class EstatisticaMaquina(db.Model):
    __tablename__ = 'estatisticas_maquinas'

    id = db.Column(db.Integer, primary_key=True)
    maquina_id = db.Column(db.Integer, nullable=False)
    uso = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('maquina_id', name='_maquina_id_uc'),)


class CodigoVerificacao(db.Model):
    __tablename__ = 'codigos_verificacao'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(6), nullable=False)
    expiracao = db.Column(db.String(30), nullable=False)
    tipo = db.Column(db.String(20), default='recuperacao')
    dados_cadastro_json = db.Column(db.Text, nullable=True)


class LogAdmin(db.Model):
    __tablename__ = 'logs_admin'

    id = db.Column(db.Integer, primary_key=True)
    admin_email = db.Column(db.String(100), nullable=False)
    acao = db.Column(db.String(200), nullable=False)
    detalhes = db.Column(db.Text, nullable=True)
    ip = db.Column(db.String(50), nullable=True)
    data_hora = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'admin_email': self.admin_email,
            'acao': self.acao,
            'detalhes': self.detalhes,
            'ip': self.ip,
            'data_hora': self.data_hora.strftime('%d/%m/%Y %H:%M')
        }


# ============================================================
# ÍNDICES PARA MELHORAR PERFORMANCE
# ============================================================

from sqlalchemy import Index

Index('idx_agendamentos_data', Agendamento.data)
Index('idx_agendamentos_status', Agendamento.status)
Index('idx_agendamentos_usuario', Agendamento.usuario)
Index('idx_agendamentos_data_status', Agendamento.data, Agendamento.status)
Index('idx_bloqueios_data', Bloqueio.data)
Index('idx_codigos_email', CodigoVerificacao.email)