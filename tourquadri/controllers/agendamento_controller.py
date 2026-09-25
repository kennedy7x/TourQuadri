from flask import render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
from tourquadri import ADMIN_EMAIL
from tourquadri.services import AgendamentoService, MaquinaService, BloqueioService, UsuarioService
from tourquadri.models import ROTEIROS


class AgendamentoController:
    def __init__(self):
        self.agendamento_service = AgendamentoService()
        self.maquina_service = MaquinaService()
        self.bloqueio_service = BloqueioService()
        self.usuario_service = UsuarioService()

    def dashboard(self):
        if session.get("usuario") == ADMIN_EMAIL:
            return redirect(url_for("admin_dashboard"))

        hoje = datetime.now().date()
        agora = datetime.now()
        roteiro_selecionado = request.args.get("roteiro_selecionado", "")
        aplicar_desconto_auto = request.args.get("aplicar_desconto", "") == "1"

        if agora.hour >= 17:
            data_minima = (hoje + timedelta(days=1)).isoformat()
        else:
            data_minima = hoje.isoformat()

        maquinas = self.maquina_service.listar_como_dict()
        bloqueios = self.bloqueio_service.listar_bloqueios()

        # Progresso de fidelidade
        usuario = self.usuario_service.buscar_por_id(session.get('usuario_id'))
        progresso = self.usuario_service.get_progresso_fidelidade(usuario)

        return render_template(
            "geral/dashboard.html",
            usuario=session.get("usuario"),
            nome=session.get("nome"),
            admin=False,
            hoje=hoje.isoformat(),
            data_minima=data_minima,
            data_limite=(hoje + timedelta(days=30)).isoformat(),
            TOTAL_MAQUINAS=len(maquinas),
            roteiro_selecionado=roteiro_selecionado,
            maquinas_especificacoes=maquinas,
            bloqueios=bloqueios,
            progresso=progresso,
            aplicar_desconto_auto=aplicar_desconto_auto
        )

    def agendar_passeio(self):
        try:
            maquinas = [int(m) for m in request.form.getlist("maquinas")]
            data = request.form.get("data")
            horario = request.form.get("horario")
            roteiro = request.form.get("roteiro", "1")
            aplicar_desconto = request.form.get("aplicar_desconto") == "on"

            hoje = datetime.now().date()
            agora = datetime.now()
            data_esc = datetime.strptime(data, "%Y-%m-%d").date()

            if data_esc == hoje and agora.hour >= 17:
                flash("Não é possível agendar para hoje após as 17h.", "danger")
                return redirect(url_for("dashboard"))

            if data_esc < hoje:
                flash("Selecione uma data válida (futura).", "danger")
                return redirect(url_for("dashboard"))

            if data_esc > hoje + timedelta(days=30):
                flash("Só é possível agendar até 30 dias no futuro.", "danger")
                return redirect(url_for("dashboard"))

            if self.bloqueio_service.verificar_horario_bloqueado(data, horario):
                flash("Este horário está bloqueado para agendamentos.", "danger")
                return redirect(url_for("dashboard"))

            is_admin = session.get("usuario") == ADMIN_EMAIL

            if is_admin:
                nome_cliente = request.form.get("nome_cliente", "").strip()
                telefone_cliente = request.form.get("telefone_cliente", "").strip()
                email_cliente = request.form.get("email_cliente", "").strip()

                if not nome_cliente:
                    nome_cliente = session.get("nome", "Administrador")
                if not email_cliente:
                    email_cliente = session["usuario"]

                dados = {
                    'usuario': session["usuario"],
                    'usuario_admin': session["usuario"],
                    'nome_usuario': session.get("nome", "Administrador"),
                    'nome_cliente': nome_cliente,
                    'telefone_cliente': telefone_cliente if telefone_cliente else "(11) 99999-9999",
                    'email_cliente': email_cliente,
                    'maquinas': maquinas,
                    'data': data,
                    'horario': horario,
                    'roteiro': roteiro,
                    'criado_por_admin': True
                }
            else:
                usuario = self.usuario_service.buscar_por_id(session.get('usuario_id'))
                telefone = usuario.telefone if usuario else ""

                dados = {
                    'usuario': session["usuario"],
                    'usuario_admin': None,
                    'nome_usuario': session.get("nome", "Usuário"),
                    'nome_cliente': session.get("nome", "Usuário"),
                    'telefone_cliente': telefone,
                    'email_cliente': session["usuario"],
                    'maquinas': maquinas,
                    'data': data,
                    'horario': horario,
                    'roteiro': roteiro,
                    'criado_por_admin': False,
                    'aplicar_desconto': aplicar_desconto
                }

            resultado = self.agendamento_service.criar(dados)

            if resultado['sucesso']:
                flash("Passeio agendado com sucesso! Caso precise editar, acesse Meus Agendamentos.", "success")
            else:
                # Não mostra flash pra erro de máquinas — o frontend já avisa
                if "indisponíveis" not in resultado['mensagem'].lower() and "indisponiveis" not in resultado['mensagem'].lower():
                    flash(resultado['mensagem'], "danger")

            return redirect(url_for("dashboard"))

        except Exception as e:
            flash(f"Erro ao agendar: {str(e)}", "danger")
            return redirect(url_for("dashboard"))

    def cancelar_agendamento(self, agendamento_id):
        resultado = self.agendamento_service.cancelar(agendamento_id, 'usuario')

        if resultado['sucesso']:
            flash("Agendamento cancelado com sucesso!", "success")
        else:
            flash(resultado['mensagem'], "danger")

        return redirect(url_for("meus_agendamentos"))

    def editar_agendamento(self, agendamento_id):
        agendamentos = self.agendamento_service.listar_todos()
        agendamento = next((a for a in agendamentos if a.id == agendamento_id and a.usuario == session.get('usuario')), None)

        if not agendamento:
            flash("Agendamento não encontrado.", "danger")
            return redirect(url_for("meus_agendamentos"))

        if agendamento.status in ['em_andamento', 'finalizado']:
            flash("Não é possível editar um passeio em andamento ou finalizado.", "danger")
            return redirect(url_for("meus_agendamentos"))

        hoje = datetime.now().date()
        agora = datetime.now()

        if agora.hour >= 17:
            data_minima = (hoje + timedelta(days=1)).isoformat()
        else:
            data_minima = hoje.isoformat()

        data_limite = (hoje + timedelta(days=30)).isoformat()
        maquinas = self.maquina_service.listar_como_dict()

        if request.method == 'POST':
            data = request.form.get("data")
            horario = request.form.get("horario")
            roteiro = request.form.get("roteiro", "1")
            maquinas_selecionadas = [int(m) for m in request.form.getlist("maquinas")]

            if not maquinas_selecionadas:
                flash("Selecione pelo menos uma máquina.", "danger")
                return render_template(
                    "geral/editar_agendamento.html",
                    agendamento=agendamento,
                    maquinas_especificacoes=maquinas,
                    data_minima=data_minima,
                    data_limite=data_limite
                )

            dados = {
                'data': data,
                'horario': horario,
                'roteiro': roteiro,
                'maquinas': maquinas_selecionadas
            }

            resultado = self.agendamento_service.atualizar(agendamento_id, dados)

            if resultado['sucesso']:
                flash("Agendamento atualizado com sucesso!", "success")
                return redirect(url_for("meus_agendamentos"))

            flash(resultado['mensagem'], "danger")

        return render_template(
            "geral/editar_agendamento.html",
            agendamento=agendamento,
            maquinas_especificacoes=maquinas,
            data_minima=data_minima,
            data_limite=data_limite
        )

    def minha_fidelidade(self):
        """Página de fidelidade do cliente"""
        usuario = self.usuario_service.buscar_por_id(session.get('usuario_id'))
        progresso = self.usuario_service.get_progresso_fidelidade(usuario)
        return render_template("geral/fidelidade.html", progresso=progresso, usuario=usuario)
    
    def verificar_maquinas(self):
        """Retorna quais máquinas estão disponíveis para data/horário/roteiro."""
        data = request.args.get("data")
        horario = request.args.get("horario")
        roteiro = request.args.get("roteiro", "")
        agendamento_id = request.args.get("agendamento_id")

        # Basta data e horário. Roteiro é opcional (padrão: 60 min).
        if not data or not horario:
            from tourquadri.models import Maquina
            todas = [m.id for m in Maquina.query.order_by(Maquina.id).all()]
            return jsonify({"disponiveis": todas, "ocupadas": []})

        disponiveis, ocupadas = self.maquina_service.verificar_disponibilidade(
            data, horario, roteiro, agendamento_id
        )

        return jsonify({"disponiveis": disponiveis, "ocupadas": ocupadas})