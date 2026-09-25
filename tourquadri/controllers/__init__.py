from flask import render_template

# ============================================================
# PÁGINAS DE ERRO
# ============================================================

def registrar_erros(app):
    @app.errorhandler(404)
    def pagina_nao_encontrada(e):
        return render_template('geral/404.html'), 404

    @app.errorhandler(500)
    def erro_servidor(e):
        return render_template('geral/500.html'), 500


# ============================================================
# REGISTRO DAS ROTAS
# ============================================================

from .auth_controller import AuthController
from .usuario_controller import UsuarioController
from .agendamento_controller import AgendamentoController
from .admin_controller import AdminController
from .roteiro_controller import RoteiroController


def registrar_rotas(app):
    registrar_erros(app)

    auth = AuthController()
    usuario = UsuarioController()
    agendamento = AgendamentoController()
    admin = AdminController()
    roteiro = RoteiroController()

    # ============================================================
    # ROTAS PÚBLICAS
    # ============================================================
    app.add_url_rule('/', 'landing', auth.landing)
    app.add_url_rule('/login', 'login', auth.login)
    app.add_url_rule('/register', 'register', auth.register)
    app.add_url_rule('/autenticar', 'autenticar', auth.autenticar, methods=['POST'])
    app.add_url_rule('/salvar_usuario', 'salvar_usuario', auth.salvar_usuario, methods=['POST'])
    app.add_url_rule('/verificar_cadastro', 'verificar_cadastro', auth.verificar_cadastro)
    app.add_url_rule('/confirmar_cadastro', 'confirmar_cadastro', auth.confirmar_cadastro, methods=['POST'])
    app.add_url_rule('/reenviar_codigo_cadastro', 'reenviar_codigo_cadastro', auth.reenviar_codigo_cadastro, methods=['POST'])
    app.add_url_rule('/logout', 'logout', auth.logout)
    app.add_url_rule('/esqueci_senha', 'esqueci_senha', auth.esqueci_senha)
    app.add_url_rule('/solicitar_codigo', 'solicitar_codigo', auth.solicitar_codigo, methods=['POST'])
    app.add_url_rule('/verificar_codigo', 'verificar_codigo', auth.verificar_codigo, methods=['POST'])
    app.add_url_rule('/redefinir_senha', 'redefinir_senha', auth.redefinir_senha)
    app.add_url_rule('/salvar_nova_senha', 'salvar_nova_senha', auth.salvar_nova_senha, methods=['POST'])

    # ============================================================
    # ROTAS USUÁRIO
    # ============================================================
    app.add_url_rule('/dashboard', 'dashboard', agendamento.dashboard)
    app.add_url_rule('/conta', 'conta', usuario.conta)
    app.add_url_rule('/alterar_senha', 'alterar_senha', usuario.alterar_senha, methods=['GET', 'POST'])
    app.add_url_rule('/meus_agendamentos', 'meus_agendamentos', usuario.meus_agendamentos)
    app.add_url_rule('/minhas_estatisticas', 'minhas_estatisticas', usuario.minhas_estatisticas)
    app.add_url_rule('/minha_fidelidade', 'minha_fidelidade', agendamento.minha_fidelidade)
    app.add_url_rule('/agendar_passeio', 'agendar_passeio', agendamento.agendar_passeio, methods=['POST'])
    app.add_url_rule('/cancelar_agendamento/<agendamento_id>', 'cancelar_agendamento', agendamento.cancelar_agendamento)
    app.add_url_rule('/editar_agendamento/<agendamento_id>', 'editar_agendamento', agendamento.editar_agendamento, methods=['GET', 'POST'])

    # ============================================================
    # ROTAS ADMIN
    # ============================================================
    app.add_url_rule('/admin', 'admin_dashboard', admin.dashboard)
    app.add_url_rule('/admin/agendamentos', 'admin_agendamentos', admin.gerenciar_agendamentos)
    app.add_url_rule('/admin/agendamentos/iniciar/<agendamento_id>', 'admin_iniciar_passeio', admin.iniciar_passeio)
    app.add_url_rule('/admin/agendamentos/finalizar/<agendamento_id>', 'admin_finalizar_passeio', admin.finalizar_passeio)
    app.add_url_rule('/admin/cancelar/<agendamento_id>', 'admin_cancelar_agendamento', admin.cancelar_agendamento)
    app.add_url_rule('/admin/editar/<agendamento_id>', 'admin_editar_agendamento', admin.editar_agendamento, methods=['GET', 'POST'])
    app.add_url_rule('/admin/realizar_agendamento', 'admin_realizar_agendamento', admin.realizar_agendamento)
    app.add_url_rule('/admin/enviar_lembrete/<agendamento_id>', 'admin_enviar_lembrete', admin.enviar_lembrete)
    app.add_url_rule('/admin/exportar_pdf', 'admin_exportar_pdf', admin.exportar_pdf)
    app.add_url_rule('/admin/visao_geral', 'admin_visao_geral', admin.visao_geral)
    app.add_url_rule('/admin/logs', 'admin_logs', admin.logs)

    # Máquinas
    app.add_url_rule('/admin/maquinas', 'admin_maquinas', admin.gerenciar_maquinas)
    app.add_url_rule('/admin/maquinas/adicionar', 'admin_adicionar_maquina', admin.adicionar_maquina, methods=['POST'])
    app.add_url_rule('/admin/maquinas/editar/<maquina_id>', 'admin_editar_maquina', admin.editar_maquina, methods=['POST'])
    app.add_url_rule('/admin/maquinas/excluir/<maquina_id>', 'admin_excluir_maquina', admin.excluir_maquina)
    app.add_url_rule('/admin/maquinas_estatisticas', 'admin_maquinas_estatisticas', admin.estatisticas_maquinas)

    # Roteiros
    app.add_url_rule('/admin/roteiros', 'admin_roteiros', admin.gerenciar_roteiros)
    app.add_url_rule('/admin/roteiro/adicionar', 'admin_adicionar_roteiro_view', admin.adicionar_roteiro_view)
    app.add_url_rule('/admin/roteiro/editar/<roteiro_id>', 'admin_editar_roteiro_view', admin.editar_roteiro_admin)
    app.add_url_rule('/admin/roteiros/adicionar', 'admin_adicionar_roteiro', admin.adicionar_roteiro, methods=['POST'])
    app.add_url_rule('/admin/roteiros/editar/<roteiro_id>', 'admin_editar_roteiro', admin.editar_roteiro, methods=['POST'])
    app.add_url_rule('/admin/roteiros/excluir/<roteiro_id>', 'admin_excluir_roteiro', admin.excluir_roteiro)

    # Bloqueios
    app.add_url_rule('/admin/gerenciar_horarios', 'admin_gerenciar_horarios', admin.gerenciar_horarios)
    app.add_url_rule('/admin/bloquear_horario', 'admin_bloquear_horario', admin.bloquear_horario, methods=['POST'])
    app.add_url_rule('/admin/desbloquear_horario', 'admin_desbloquear_horario', admin.desbloquear_horario, methods=['POST'])
    app.add_url_rule('/admin/bloquear_todos_horarios', 'admin_bloquear_todos_horarios', admin.bloquear_todos_horarios, methods=['POST'])
    app.add_url_rule('/admin/desbloquear_todos_horarios', 'admin_desbloquear_todos_horarios', admin.desbloquear_todos_horarios, methods=['POST'])

    # ============================================================
    # ROTAS ROTEIROS
    # ============================================================
    app.add_url_rule('/roteiros', 'roteiros', roteiro.listar_roteiros)
    app.add_url_rule('/roteiro/<roteiro_id>', 'roteiro_detalhe', roteiro.detalhe_roteiro)
    app.add_url_rule('/agendar_roteiro/<roteiro_id>', 'agendar_roteiro', roteiro.agendar_roteiro)
    app.add_url_rule('/maquinas', 'maquinas', roteiro.listar_maquinas)

    # ============================================================
    # API
    # ============================================================
    app.add_url_rule('/api/verificar_maquinas', 'verificar_maquinas', agendamento.verificar_maquinas)
    app.add_url_rule('/api/verificar_bloqueios', 'verificar_bloqueios', admin.verificar_bloqueios)
    app.add_url_rule('/api/dashboard_cliente', 'api_dashboard_cliente', usuario.api_dashboard_cliente)
    app.add_url_rule('/api/dashboard_admin', 'api_dashboard_admin', admin.api_dashboard_admin)