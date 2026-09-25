import json
import os
import re
import uuid
from datetime import datetime, timedelta

from flask_mail import Message

from tourquadri import db, mail
from tourquadri.models import (
    Usuario, Maquina, Agendamento, Bloqueio,
    EstatisticaMaquina, CodigoVerificacao, ROTEIROS, LogAdmin
)

# Programa de fidelidade
PASSEIOS_PARA_DESCONTO = 5
PERCENTUAL_DESCONTO = 20


# ==========================
# FUNÇÕES AUXILIARES
# ==========================

def validar_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None


def validar_telefone(telefone):
    return len(re.sub(r'[^\d]', '', telefone)) in [10, 11]


def validar_senha_forte(senha):
    """Valida se a senha é forte"""
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"
    if not re.search(r'[A-Z]', senha):
        return False, "A senha deve ter pelo menos uma letra maiúscula"
    if not re.search(r'[a-z]', senha):
        return False, "A senha deve ter pelo menos uma letra minúscula"
    if not re.search(r'[0-9]', senha):
        return False, "A senha deve ter pelo menos um número"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return False, "A senha deve ter pelo menos um caractere especial (!@#$%^&*()...)"
    return True, ""


def hora_para_minutos(hora_str):
    h, m = map(int, hora_str.split(':'))
    return h * 60 + m


def gerar_codigo():
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def formatar_data_br(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        return data.strftime('%d/%m/%Y')
    except:
        return data_str


# ==========================
# 1. EMAIL SERVICE
# ==========================

class EmailService:
    """Serviço para envio de emails"""

    def enviar(self, destinatario, assunto, corpo):
        try:
            msg = Message(assunto, recipients=[destinatario])
            msg.body = corpo
            mail.send(msg)
            print(f"✅ Email enviado para {destinatario}")
            return True
        except Exception as e:
            print(f"❌ ERRO ao enviar email para {destinatario}:")
            print(f"   Tipo: {type(e).__name__}")
            print(f"   Mensagem: {e}")
            return False

    def enviar_codigo_cadastro(self, email, codigo, nome):
        assunto = "Confirme seu cadastro - TourQuadri"
        corpo = f"""Olá, {nome}!

Bem-vindo(a) à TourQuadri!

Para confirmar seu cadastro, use o código abaixo:

{codigo}

Este código é válido por 15 minutos.

Se você não solicitou este cadastro, ignore este email.

Atenciosamente,
Equipe TourQuadri"""
        return self.enviar(email, assunto, corpo)
    
    def enviar_codigo_recuperacao(self, email, codigo):
        corpo = f"""Olá!

Você solicitou a recuperação de senha no TourQuadri.

Seu código de verificação é: {codigo}

Este código é válido por 15 minutos.

Atenciosamente,
Equipe TourQuadri"""
        return self.enviar(email, "Recuperação de Senha - TourQuadri", corpo)

    def enviar_lembrete(self, email, nome, data, horario, roteiro_nome, maquinas):
        assunto = f"TourQuadri - Lembrete do seu passeio: {roteiro_nome}"
        corpo = f"""Olá {nome}!

Este é um lembrete do seu passeio agendado com a TourQuadri.

📅 Data: {data}
⏰ Horário: {horario}
📍 Roteiro: {roteiro_nome}
🚜 Máquinas: {', '.join(map(str, maquinas))}

Dicas para o passeio:
• Chegue com 15 minutos de antecedência
• Use roupas confortáveis
• Não se esqueça de levar água

Aguardamos você para uma aventura inesquecível!

Atenciosamente,
Equipe TourQuadri"""
        return self.enviar(email, assunto, corpo)

    def enviar_pedido_avaliacao(self, email, nome, roteiro_nome, link_avaliacao):
        assunto = f"Como foi seu passeio, {nome}?"
        corpo = f"""Olá, {nome}!

Esperamos que seu passeio "{roteiro_nome}" tenha sido incrível!

Se você gostou da experiência, poderia compartilhar sua opinião no Google? Leva menos de 1 minuto e ajuda muito nossa equipe.

👉 {link_avaliacao}

Se algo não saiu como esperado, responda este email diretamente — queremos ouvir você.

Obrigado por escolher a TourQuadri!"""
        return self.enviar(email, assunto, corpo)
    
    def enviar_notificacao_exclusao(self, email, nome, data, horario, roteiro_nome):
        assunto = f"TourQuadri - ATENÇÃO: Alteração no seu passeio"
        corpo = f"""Olá {nome}!

Infelizmente, a máquina que você reservou para o seu passeio ({roteiro_nome}) no dia {data} às {horario} está indisponível.

A TourQuadri está trabalhando para resolver o problema e entrará em contato em breve para remarcar seu passeio ou oferecer uma alternativa.

Pedimos desculpas pelo inconveniente.

Atenciosamente,
Equipe TourQuadri"""
        return self.enviar(email, assunto, corpo)


# ==========================
# 2. USUARIO SERVICE
# ==========================

class UsuarioService:
    """Serviço para gerenciamento de usuários"""

    def __init__(self):
        self.email_service = EmailService()

    def autenticar(self, email, senha):
        """Autentica um usuário"""
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return {'sucesso': False, 'mensagem': 'Email não cadastrado'}

        if not usuario.verificar_senha(senha):
            return {'sucesso': False, 'mensagem': 'Senha incorreta'}

        if not usuario.admin and not usuario.email_verificado:
            return {'sucesso': False, 'mensagem': 'Confirme seu email antes de fazer login.'}

        return {'sucesso': True, 'usuario': usuario}

    def iniciar_cadastro(self, nome, telefone, email, senha, confirmar_senha):
        """Inicia o cadastro: valida, gera código e envia email. Não cria usuário ainda."""
        erros = {}

        if not nome or len(nome.strip()) < 3:
            erros['nome'] = 'Nome é obrigatório (mínimo 3 caracteres)'

        if not validar_telefone(telefone):
            erros['telefone'] = 'Telefone inválido'

        if not validar_email(email):
            erros['email'] = 'Email inválido'
        elif Usuario.query.filter_by(email=email).first():
            erros['email'] = 'Email já cadastrado'

        valido, mensagem = validar_senha_forte(senha)
        if not valido:
            erros['senha'] = mensagem

        if senha != confirmar_senha:
            erros['confirmar_senha'] = 'As senhas não coincidem'

        if erros:
            return {'sucesso': False, 'erros': erros}

        codigo = gerar_codigo()
        expiracao = datetime.now() + timedelta(minutes=15)

        CodigoVerificacao.query.filter_by(email=email, tipo='cadastro').delete()

        codigo_db = CodigoVerificacao(
            email=email,
            codigo=codigo,
            expiracao=expiracao.isoformat(),
            tipo='cadastro',
            dados_cadastro_json=json.dumps({
                'nome': nome.strip(),
                'telefone': telefone.strip(),
                'email': email.strip(),
                'senha': senha
            })
        )
        db.session.add(codigo_db)
        db.session.commit()

        email_enviado = self.email_service.enviar_codigo_cadastro(email, codigo, nome)

        return {'sucesso': True, 'email': email, 'email_enviado': email_enviado}

    def confirmar_cadastro(self, email, codigo):
        """Verifica o código e cria o usuário de verdade."""
        codigo_db = CodigoVerificacao.query.filter_by(email=email, tipo='cadastro').first()

        if not codigo_db:
            return {'sucesso': False, 'mensagem': 'Código expirado. Solicite um novo.'}

        if datetime.now() > datetime.fromisoformat(codigo_db.expiracao):
            db.session.delete(codigo_db)
            db.session.commit()
            return {'sucesso': False, 'mensagem': 'Código expirado. Solicite um novo.'}

        if codigo_db.codigo != codigo:
            return {'sucesso': False, 'mensagem': 'Código inválido. Tente novamente.'}

        dados = json.loads(codigo_db.dados_cadastro_json)

        usuario = Usuario(
            nome=dados['nome'],
            telefone=dados['telefone'],
            email=dados['email'],
            admin=False,
            email_verificado=True
        )
        usuario.senha_criptografada = dados['senha']

        db.session.add(usuario)
        db.session.delete(codigo_db)
        db.session.commit()

        return {'sucesso': True, 'usuario': usuario}

    
    def criar(self, nome, telefone, email, senha, confirmar_senha):
        """Cria um novo usuário"""
        erros = {}

        if not nome or len(nome.strip()) < 3:
            erros['nome'] = 'Nome é obrigatório (mínimo 3 caracteres)'

        if not validar_telefone(telefone):
            erros['telefone'] = 'Telefone inválido'

        if not validar_email(email):
            erros['email'] = 'Email inválido'
        elif Usuario.query.filter_by(email=email).first():
            erros['email'] = 'Email já cadastrado'

        # ============================================================
        # VALIDAÇÃO DE SENHA FORTE
        # ============================================================
        valido, mensagem = validar_senha_forte(senha)
        if not valido:
            erros['senha'] = mensagem

        if senha != confirmar_senha:
            erros['confirmar_senha'] = 'As senhas não coincidem'

        if erros:
            return {'sucesso': False, 'erros': erros}

        usuario = Usuario(
            nome=nome.strip(),
            telefone=telefone.strip(),
            email=email.strip(),
            admin=False
        )
        usuario.senha_criptografada = senha

        db.session.add(usuario)
        db.session.commit()

        return {'sucesso': True, 'usuario': usuario}

    def buscar_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def buscar_por_id(self, usuario_id):
        return Usuario.query.get(usuario_id)

    def get_progresso_fidelidade(self, usuario):
        """Retorna o progresso do programa de fidelidade"""
        if not usuario or usuario.admin:
            return None

        realizados = usuario.passeios_realizados or 0
        desconto_disponivel = usuario.desconto_disponivel or False

        faltam = max(0, PASSEIOS_PARA_DESCONTO - realizados)
        percentual_progresso = min(100, int((realizados / PASSEIOS_PARA_DESCONTO) * 100))

        return {
            'passeios_realizados': realizados,
            'passeios_necessarios': PASSEIOS_PARA_DESCONTO,
            'faltam': faltam,
            'percentual': percentual_progresso,
            'desconto_disponivel': desconto_disponivel,
            'percentual_desconto': PERCENTUAL_DESCONTO
        }

    def alterar_senha(self, usuario, senha_atual, nova_senha, confirmar_senha):
        """Altera a senha do usuário"""
        if not usuario.verificar_senha(senha_atual):
            return {'sucesso': False, 'mensagem': 'Senha atual incorreta'}

        # ============================================================
        # VALIDAÇÃO DE SENHA FORTE
        # ============================================================
        valido, mensagem = validar_senha_forte(nova_senha)
        if not valido:
            return {'sucesso': False, 'mensagem': mensagem}

        if nova_senha != confirmar_senha:
            return {'sucesso': False, 'mensagem': 'As senhas não coincidem'}

        usuario.senha_criptografada = nova_senha
        db.session.commit()

        return {'sucesso': True}

    def solicitar_recuperacao(self, email):
        """Solicita recuperação de senha"""
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return {'sucesso': False, 'mensagem': 'Email não encontrado'}

        codigo = gerar_codigo()
        expiracao = datetime.now() + timedelta(minutes=15)

        CodigoVerificacao.query.filter_by(email=email).delete()

        codigo_db = CodigoVerificacao(
            email=email,
            codigo=codigo,
            expiracao=expiracao.isoformat()
        )
        db.session.add(codigo_db)
        db.session.commit()

        email_enviado = self.email_service.enviar_codigo_recuperacao(email, codigo)

        return {'sucesso': True, 'email_enviado': email_enviado}

    def verificar_codigo(self, email, codigo):
        """Verifica o código de recuperação"""
        codigo_db = CodigoVerificacao.query.filter_by(email=email).first()

        if not codigo_db:
            return {'sucesso': False, 'mensagem': 'Código expirado. Solicite um novo.'}

        if datetime.now() > datetime.fromisoformat(codigo_db.expiracao):
            db.session.delete(codigo_db)
            db.session.commit()
            return {'sucesso': False, 'mensagem': 'Código expirado. Solicite um novo.'}

        if codigo_db.codigo != codigo:
            return {'sucesso': False, 'mensagem': 'Código inválido. Tente novamente.'}

        return {'sucesso': True}

    def redefinir_senha(self, email, nova_senha, confirmar_senha):
        """Redefine a senha do usuário"""
        # ============================================================
        # VALIDAÇÃO DE SENHA FORTE
        # ============================================================
        valido, mensagem = validar_senha_forte(nova_senha)
        if not valido:
            return {'sucesso': False, 'mensagem': mensagem}

        if nova_senha != confirmar_senha:
            return {'sucesso': False, 'mensagem': 'As senhas não coincidem'}

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            usuario.senha_criptografada = nova_senha
            db.session.commit()

        CodigoVerificacao.query.filter_by(email=email).delete()
        db.session.commit()

        return {'sucesso': True}


# ==========================
# 3. MAQUINA SERVICE
# ==========================

class MaquinaService:
    """Serviço para gerenciamento de máquinas"""

    def listar_todas(self):
        """Lista todas as máquinas ordenadas por ID (0 a 14)"""
        return Maquina.query.order_by(Maquina.id).all()

    def listar_como_dict(self):
        """Lista máquinas como dicionário {id: {nome_maquina, modelo, cc}} ordenado por ID"""
        maquinas = Maquina.query.order_by(Maquina.id).all()
        return {str(m.id): {
            'nome_maquina': m.nome_maquina,
            'modelo': m.modelo,
            'cc': m.cc
        } for m in maquinas}

    def criar(self, nome_maquina, modelo, cc):
        """Cria uma nova máquina"""
        maquina = Maquina(
            nome_maquina=nome_maquina,
            modelo=modelo,
            cc=cc
        )
        db.session.add(maquina)
        db.session.commit()
        return maquina

    def buscar_por_id(self, maquina_id):
        return Maquina.query.get(maquina_id)

    def atualizar(self, maquina_id, nome_maquina, modelo, cc):
        """Atualiza uma máquina"""
        maquina = Maquina.query.get(maquina_id)
        if maquina:
            maquina.nome_maquina = nome_maquina
            maquina.modelo = modelo
            maquina.cc = cc
            db.session.commit()
            return maquina
        return None

    def excluir(self, maquina_id):
        """Exclui uma máquina e notifica clientes afetados"""
        maquina = Maquina.query.get(maquina_id)

        if not maquina:
            return {'sucesso': False, 'mensagem': 'Máquina não encontrada'}

        # Verifica agendamentos afetados
        agendamentos = Agendamento.query.filter(
            Agendamento.status.notin_(['cancelado', 'finalizado'])
        ).all()

        agendamentos_afetados = []
        for a in agendamentos:
            if int(maquina_id) in a.maquinas:
                agendamentos_afetados.append(a)

        # Envia emails
        email_service = EmailService()
        emails_enviados = 0

        for a in agendamentos_afetados:
            roteiro = ROTEIROS.get(a.roteiro, {})
            data_formatada = formatar_data_br(a.data)

            email_service.enviar_notificacao_exclusao(
                a.email_cliente,
                a.nome_cliente,
                data_formatada,
                a.horario,
                roteiro.get('nome', 'Roteiro não definido')
            )
            emails_enviados += 1

        # Exclui a máquina
        db.session.delete(maquina)
        db.session.commit()

        mensagem = f"Máquina '{maquina.nome_maquina}' excluída com sucesso!"
        if emails_enviados > 0:
            mensagem += f" {emails_enviados} clientes foram notificados."

        return {'sucesso': True, 'mensagem': mensagem}

    def verificar_disponibilidade(self, data, horario, roteiro_id, agendamento_id=None):
        """
        Retorna (disponiveis, ocupadas) para um dado data/horário/roteiro.

        Regra de sobreposição: uma máquina está ocupada se o intervalo
        [inicio_novo, fim_novo) tiver QUALQUER sobreposição com
        [inicio_existente, fim_existente).

        A duração do novo passeio é a do roteiro escolhido (padrão: 60 min).
        A duração de cada agendamento existente é a do roteiro daquele agendamento.
        """
        ids_maquinas = [m.id for m in Maquina.query.all()]

        # Precisa de data e horário
        if not data or not horario:
            return ids_maquinas, []

        # Duração do novo passeio (padrão 60 min se roteiro não escolhido)
        if roteiro_id and roteiro_id in ROTEIROS:
            duracao_novo = ROTEIROS[roteiro_id].get('duracao', 60)
        else:
            duracao_novo = 60

        try:
            inicio_min = hora_para_minutos(horario)
        except Exception:
            return ids_maquinas, []

        fim_min = inicio_min + duracao_novo

        agendamentos = Agendamento.query.filter_by(data=data).all()
        bloqueios = Bloqueio.query.filter_by(data=data).all()
        ocupadas = set()

        # Bloqueios (bloqueia todas)
        for b in bloqueios:
            try:
                h_min = hora_para_minutos(b.horario)
            except Exception:
                continue
            if inicio_min < h_min + 60 and fim_min > h_min:
                return [], ids_maquinas

        # Agendamentos existentes
        for a in agendamentos:
            if a.status in ['cancelado', 'finalizado']:
                continue
            if agendamento_id and a.id == agendamento_id:
                continue

            duracao_a = ROTEIROS.get(a.roteiro, {}).get('duracao', 60)

            try:
                inicio_a = hora_para_minutos(a.horario)
            except Exception:
                continue

            fim_a = inicio_a + duracao_a

            # ⚠️ SOBREPOSIÇÃO REAL: considera a duração do novo passeio
            if inicio_min < fim_a and fim_min > inicio_a:
                maquinas_do_agendamento = a.maquinas  # property já faz json.loads
                if isinstance(maquinas_do_agendamento, list):
                    for m in maquinas_do_agendamento:
                        try:
                            ocupadas.add(int(m))
                        except (ValueError, TypeError):
                            pass

        disponiveis = [i for i in ids_maquinas if i not in ocupadas]
        return disponiveis, list(ocupadas)

    def incrementar_uso(self, maquinas_list):
        """Incrementa o contador de uso das máquinas"""
        for m in maquinas_list:
            estatistica = EstatisticaMaquina.query.filter_by(maquina_id=m).first()
            if estatistica:
                estatistica.uso += 1
            else:
                estatistica = EstatisticaMaquina(maquina_id=m, uso=1)
                db.session.add(estatistica)
        db.session.commit()

    def get_estatisticas(self):
        """Retorna estatísticas de uso das máquinas"""
        stats = EstatisticaMaquina.query.all()
        maquinas = Maquina.query.all()
        maquinas_dict = {m.id: m for m in maquinas}

        result = []
        for s in stats:
            if s.maquina_id in maquinas_dict:
                result.append({
                    'id': s.maquina_id,
                    'nome_maquina': maquinas_dict[s.maquina_id].nome_maquina,
                    'modelo': maquinas_dict[s.maquina_id].modelo,
                    'cc': maquinas_dict[s.maquina_id].cc,
                    'uso': s.uso
                })

        return sorted(result, key=lambda x: x['uso'], reverse=True)


# ==========================
# 4. AGENDAMENTO SERVICE
# ==========================

class AgendamentoService:
    """Serviço para gerenciamento de agendamentos"""

    def __init__(self):
        self.maquina_service = MaquinaService()
        self.email_service = EmailService()

    def listar_todos(self):
        return Agendamento.query.all()

    def listar_por_usuario(self, email):
        return Agendamento.query.filter_by(usuario=email).all()

    def criar(self, dados):
        """Cria um novo agendamento"""
        maquinas = dados.get('maquinas', [])
        data = dados.get('data')
        horario = dados.get('horario')
        roteiro = dados.get('roteiro', '1')
        aplicar_desconto = dados.get('aplicar_desconto', False)

        if not maquinas:
            return {'sucesso': False, 'mensagem': 'Selecione pelo menos uma máquina'}

        # Verifica disponibilidade
        disponiveis, _ = self.maquina_service.verificar_disponibilidade(data, horario, roteiro)
        indisponiveis = [m for m in maquinas if m not in disponiveis]

        if indisponiveis:
            return {
                'sucesso': False,
                'mensagem': f'Máquinas indisponíveis: {", ".join(map(str, indisponiveis))}'
            }

        # Verifica se pode aplicar desconto
        desconto_aplicado = False
        if aplicar_desconto:
            usuario = Usuario.query.filter_by(email=dados.get('usuario')).first()
            if usuario and usuario.desconto_disponivel and not usuario.admin:
                desconto_aplicado = True
                # ⚠️ Trava o desconto IMEDIATAMENTE (só libera se cancelar)
                usuario.desconto_disponivel = False

        # Cria agendamento
        agendamento = Agendamento(
            id=str(uuid.uuid4()),
            usuario=dados.get('usuario'),
            usuario_admin=dados.get('usuario_admin'),
            nome_usuario=dados.get('nome_usuario'),
            nome_cliente=dados.get('nome_cliente'),
            telefone_cliente=dados.get('telefone_cliente'),
            email_cliente=dados.get('email_cliente'),
            data=data,
            horario=horario,
            roteiro=roteiro,
            duracao=ROTEIROS.get(roteiro, {}).get('duracao', 60),
            data_criacao=datetime.now().isoformat(),
            status='agendado',
            criado_por_admin=dados.get('criado_por_admin', False),
            desconto_aplicado=desconto_aplicado
        )
        agendamento.maquinas = maquinas

        db.session.add(agendamento)
        db.session.commit()

        return {'sucesso': True, 'agendamento': agendamento}

        if not maquinas:
            return {'sucesso': False, 'mensagem': 'Selecione pelo menos uma máquina'}

        # Verifica disponibilidade
        disponiveis, _ = self.maquina_service.verificar_disponibilidade(data, horario, roteiro)
        indisponiveis = [m for m in maquinas if m not in disponiveis]

        if indisponiveis:
            return {
                'sucesso': False,
                'mensagem': f'Máquinas indisponíveis: {", ".join(map(str, indisponiveis))}'
            }

        # Cria agendamento
        agendamento = Agendamento(
            id=str(uuid.uuid4()),
            usuario=dados.get('usuario'),
            usuario_admin=dados.get('usuario_admin'),
            nome_usuario=dados.get('nome_usuario'),
            nome_cliente=dados.get('nome_cliente'),
            telefone_cliente=dados.get('telefone_cliente'),
            email_cliente=dados.get('email_cliente'),
            data=data,
            horario=horario,
            roteiro=roteiro,
            duracao=ROTEIROS.get(roteiro, {}).get('duracao', 60),
            data_criacao=datetime.now().isoformat(),
            status='agendado',
            criado_por_admin=dados.get('criado_por_admin', False)
        )
        agendamento.maquinas = maquinas

        db.session.add(agendamento)
        db.session.commit()

        return {'sucesso': True, 'agendamento': agendamento}

    def cancelar(self, agendamento_id, cancelado_por='usuario'):
        """Cancela um agendamento"""
        agendamento = Agendamento.query.filter_by(id=agendamento_id).first()

        if not agendamento:
            return {'sucesso': False, 'mensagem': 'Agendamento não encontrado'}

        if agendamento.status != 'agendado':
            return {'sucesso': False, 'mensagem': 'Agendamento não pode ser cancelado'}

        agendamento.status = 'cancelado'
        agendamento.cancelado_por = cancelado_por
        agendamento.data_cancelamento = datetime.now().isoformat()

        # Se tinha desconto aplicado, devolve pro cliente
        if agendamento.desconto_aplicado:
            usuario = Usuario.query.filter_by(email=agendamento.usuario).first()
            if usuario and not usuario.admin:
                usuario.desconto_disponivel = True
            agendamento.desconto_aplicado = False

        db.session.commit()
        return {'sucesso': True}

    def iniciar(self, agendamento_id):
        """Inicia um passeio"""
        agendamento = Agendamento.query.filter_by(id=agendamento_id).first()

        if not agendamento:
            return {'sucesso': False, 'mensagem': 'Agendamento não encontrado'}

        if agendamento.status != 'agendado':
            return {'sucesso': False, 'mensagem': 'Agendamento não pode ser iniciado'}

        agendamento.status = 'em_andamento'
        agendamento.data_inicio = datetime.now().isoformat()
        db.session.commit()

        # Incrementa uso das máquinas
        self.maquina_service.incrementar_uso(agendamento.maquinas)

        return {'sucesso': True}

    def finalizar(self, agendamento_id):
        """Finaliza um passeio, agenda email de avaliação e atualiza fidelidade."""
        agendamento = Agendamento.query.filter_by(id=agendamento_id).first()

        if not agendamento:
            return {'sucesso': False, 'mensagem': 'Agendamento não encontrado'}

        if agendamento.status != 'em_andamento':
            return {'sucesso': False, 'mensagem': 'Agendamento não está em andamento'}

        agendamento.status = 'finalizado'
        agendamento.data_finalizacao = datetime.now().isoformat()

        # Agenda email de avaliação
        if not agendamento.email_avaliacao_enviado:
            data_envio = datetime.now() + timedelta(minutes=30)
            agendamento.email_avaliacao_agendado = True
            agendamento.data_agendada_envio = data_envio.isoformat()

        # ============================================================
        # PROGRAMA DE FIDELIDADE
        # ============================================================
        usuario = Usuario.query.filter_by(email=agendamento.usuario).first()

        if usuario and not usuario.admin:
            if agendamento.desconto_aplicado:
                # Usou desconto → reseta contador
                usuario.passeios_realizados = 0
                usuario.desconto_disponivel = False
            else:
                # Passeio normal → incrementa contador
                usuario.passeios_realizados = (usuario.passeios_realizados or 0) + 1

                # Atingiu o limite → libera desconto
                if usuario.passeios_realizados >= PASSEIOS_PARA_DESCONTO:
                    usuario.desconto_disponivel = True

        db.session.commit()
        return {'sucesso': True}

    def processar_emails_pendentes(self):
        """Verifica se algum email de avaliação precisa ser enviado agora."""
        agora = datetime.now()
        pendentes = Agendamento.query.filter_by(
            email_avaliacao_agendado=True,
            email_avaliacao_enviado=False
        ).all()

        enviados = 0
        for agendamento in pendentes:
            if not agendamento.data_agendada_envio:
                continue

            try:
                data_agendada = datetime.fromisoformat(agendamento.data_agendada_envio)
            except:
                continue

            if agora >= data_agendada:
                roteiro_nome = ROTEIROS.get(agendamento.roteiro, {}).get('nome', 'seu passeio')
                link_avaliacao = os.getenv('GOOGLE_REVIEW_LINK', 'https://g.page/r/SEU_PLACE_ID/review')

                self.email_service.enviar_pedido_avaliacao(
                    agendamento.email_cliente,
                    agendamento.nome_cliente,
                    roteiro_nome,
                    link_avaliacao
                )

                agendamento.email_avaliacao_enviado = True
                enviados += 1

        if enviados > 0:
            db.session.commit()
            print(f"✅ {enviados} email(s) de avaliação enviados")

        return enviados
    
    def atualizar(self, agendamento_id, dados):
        """Atualiza um agendamento"""
        agendamento = Agendamento.query.filter_by(id=agendamento_id).first()

        if not agendamento:
            return {'sucesso': False, 'mensagem': 'Agendamento não encontrado'}

        if agendamento.status in ['em_andamento', 'finalizado']:
            return {'sucesso': False, 'mensagem': 'Não é possível editar um passeio em andamento ou finalizado'}

        data = dados.get('data')
        horario = dados.get('horario')
        roteiro = dados.get('roteiro', '1')
        maquinas = dados.get('maquinas', [])

        if not maquinas:
            return {'sucesso': False, 'mensagem': 'Selecione pelo menos uma máquina'}

        # Verifica disponibilidade
        disponiveis, _ = self.maquina_service.verificar_disponibilidade(
            data, horario, roteiro, agendamento_id
        )
        indisponiveis = [m for m in maquinas if m not in disponiveis]

        if indisponiveis:
            return {
                'sucesso': False,
                'mensagem': f'Máquinas indisponíveis: {", ".join(map(str, indisponiveis))}'
            }

        # Atualiza dados
        agendamento.data = data
        agendamento.horario = horario
        agendamento.roteiro = roteiro
        agendamento.maquinas = maquinas
        agendamento.duracao = ROTEIROS.get(roteiro, {}).get('duracao', 60)

        if dados.get('nome_cliente'):
            agendamento.nome_cliente = dados.get('nome_cliente')
        if dados.get('telefone_cliente'):
            agendamento.telefone_cliente = dados.get('telefone_cliente')
        if dados.get('email_cliente'):
            agendamento.email_cliente = dados.get('email_cliente')

        db.session.commit()

        return {'sucesso': True}


# ==========================
# 5. BLOQUEIO SERVICE
# ==========================

class BloqueioService:
    """Serviço para gerenciamento de bloqueios de horário"""

    def bloquear(self, data, horario):
        """Bloqueia um horário"""
        if not data or not horario:
            return {'sucesso': False, 'mensagem': 'Data e horário são obrigatórios'}

        # Verifica se já existe
        existente = Bloqueio.query.filter_by(data=data, horario=horario).first()
        if existente:
            return {'sucesso': False, 'mensagem': 'Horário já está bloqueado'}

        bloqueio = Bloqueio(data=data, horario=horario)
        db.session.add(bloqueio)
        db.session.commit()

        return {'sucesso': True}

    def desbloquear(self, data, horario):
        """Desbloqueia um horário"""
        bloqueio = Bloqueio.query.filter_by(data=data, horario=horario).first()

        if not bloqueio:
            return {'sucesso': False, 'mensagem': 'Horário não está bloqueado'}

        db.session.delete(bloqueio)
        db.session.commit()

        return {'sucesso': True}

    def bloquear_todos(self, data):
        """Bloqueia todos os horários de um dia"""
        todos_horarios = [
            f"{h:02d}:{m:02d}"
            for h in range(9, 18)
            for m in range(0, 60, 10)
            if not (h == 17 and m > 0)
        ]

        for horario in todos_horarios:
            existente = Bloqueio.query.filter_by(data=data, horario=horario).first()
            if not existente:
                bloqueio = Bloqueio(data=data, horario=horario)
                db.session.add(bloqueio)

        db.session.commit()
        return {'sucesso': True}

    def desbloquear_todos(self, data):
        """Desbloqueia todos os horários de um dia"""
        Bloqueio.query.filter_by(data=data).delete()
        db.session.commit()
        return {'sucesso': True}

    def listar_bloqueios(self):
        """Lista todos os bloqueios agrupados por data"""
        bloqueios = Bloqueio.query.all()
        resultado = {}

        for b in bloqueios:
            if b.data not in resultado:
                resultado[b.data] = []
            resultado[b.data].append(b.horario)

        return resultado

    def listar_por_data(self, data):
        """Lista bloqueios de uma data específica"""
        bloqueios = Bloqueio.query.filter_by(data=data).all()
        return [b.horario for b in bloqueios]

    def verificar_horario_bloqueado(self, data, horario):
        """Verifica se um horário específico está bloqueado"""
        return Bloqueio.query.filter_by(data=data, horario=horario).first() is not None


# ==========================
# 6. LOG SERVICE
# ==========================

class LogService:
    """Serviço para gerenciamento de logs"""

    # Categorias de ações — usadas pra colorir/agrupar na tela
    CATEGORIAS = {
        'auth': ['Login', 'Logout', 'Alterou senha'],
        'agendamento': ['Cancelou agendamento', 'Editou agendamento', 'Iniciou passeio',
                        'Finalizou passeio', 'Realizou agendamento', 'Enviou lembrete'],
        'maquina': ['Adicionou máquina', 'Editou máquina', 'Excluiu máquina'],
        'roteiro': ['Adicionou roteiro', 'Editou roteiro', 'Excluiu roteiro'],
        'horario': ['Bloqueou horário', 'Desbloqueou horário',
                    'Bloqueou todos os horários', 'Desbloqueou todos os horários'],
    }

    def registrar(self, admin_email, acao, detalhes=None, ip=None):
        """Registra uma ação do administrador"""
        try:
            log = LogAdmin(
                admin_email=admin_email,
                acao=acao,
                detalhes=detalhes,
                ip=ip,
                data_hora=datetime.now()
            )
            db.session.add(log)
            db.session.commit()
            return log
        except Exception as e:
            print(f"⚠️ Erro ao registrar log: {e}")
            db.session.rollback()
            return None

    def _get_ip(self, request_obj):
        """Extrai o IP real do cliente (considera proxy reverso)"""
        if not request_obj:
            return None
        # Tenta pegar do header X-Forwarded-For (proxy) ou direto
        forwarded = request_obj.headers.get('X-Forwarded-For')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request_obj.remote_addr

    def listar_paginado(self, pagina=1, itens_por_pagina=20,
                        filtro_admin=None, filtro_categoria=None,
                        filtro_data=None, filtro_busca=None):
        """Lista logs com paginação e filtros"""
        query = LogAdmin.query

        if filtro_admin:
            query = query.filter(LogAdmin.admin_email == filtro_admin)

        if filtro_categoria:
            acoes = self.CATEGORIAS.get(filtro_categoria, [])
            if acoes:
                query = query.filter(LogAdmin.acao.in_(acoes))

        if filtro_data:
            try:
                data_inicio = datetime.strptime(filtro_data, '%Y-%m-%d')
                data_fim = data_inicio.replace(hour=23, minute=59, second=59)
                query = query.filter(
                    LogAdmin.data_hora >= data_inicio,
                    LogAdmin.data_hora <= data_fim
                )
            except:
                pass

        if filtro_busca:
            busca = f"%{filtro_busca}%"
            query = query.filter(
                (LogAdmin.acao.ilike(busca)) |
                (LogAdmin.detalhes.ilike(busca)) |
                (LogAdmin.admin_email.ilike(busca))
            )

        query = query.order_by(LogAdmin.id.desc())

        # Paginação manual
        total = query.count()
        total_paginas = max(1, (total + itens_por_pagina - 1) // itens_por_pagina)
        pagina = max(1, min(pagina, total_paginas))

        inicio = (pagina - 1) * itens_por_pagina
        logs = query.offset(inicio).limit(itens_por_pagina).all()

        return {
            'logs': logs,
            'total': total,
            'pagina_atual': pagina,
            'total_paginas': total_paginas,
            'paginas': list(range(1, total_paginas + 1))
        }

    def listar_ultimos(self, limite=50):
        """Lista os últimos logs (usado em widgets)"""
        return LogAdmin.query.order_by(LogAdmin.id.desc()).limit(limite).all()

    def listar_admins_unicos(self):
        """Lista emails únicos de admins que já fizeram ações"""
        resultado = db.session.query(LogAdmin.admin_email).distinct().all()
        return sorted([r[0] for r in resultado if r[0]])

    def get_categorias(self):
        """Retorna as categorias disponíveis"""
        return list(self.CATEGORIAS.keys())

    def limpar_antigos(self, dias=180):
        """Remove logs mais antigos que X dias (padrão: 180 dias = 6 meses)"""
        data_limite = datetime.now() - timedelta(days=dias)
        removidos = LogAdmin.query.filter(LogAdmin.data_hora < data_limite).delete()
        db.session.commit()
        return removidos