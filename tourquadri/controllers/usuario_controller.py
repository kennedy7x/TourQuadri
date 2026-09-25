from flask import render_template, request, redirect, url_for, session, flash, jsonify
from tourquadri import db, ADMIN_EMAIL
from tourquadri.services import UsuarioService, AgendamentoService
from tourquadri.models import Agendamento, ROTEIROS
from datetime import datetime, timedelta
from sqlalchemy import func
import re


class UsuarioController:
    def __init__(self):
        self.usuario_service = UsuarioService()
        self.agendamento_service = AgendamentoService()

    def conta(self):
        usuario = self.usuario_service.buscar_por_email(session.get('usuario'))
        return render_template("geral/conta.html", usuario=usuario)

    def alterar_senha(self):
        if request.method == 'POST':
            usuario = self.usuario_service.buscar_por_email(session.get('usuario'))
            senha_atual = request.form.get("senha_atual", "").strip()
            nova_senha = request.form.get("nova_senha", "").strip()
            confirmar_senha = request.form.get("confirmar_senha", "").strip()

            if not usuario:
                flash("Usuário não encontrado.", "danger")
                return redirect(url_for("conta"))

            if not usuario.verificar_senha(senha_atual):
                flash("Senha atual incorreta.", "danger")
                return render_template("geral/alterar_senha.html")

            # ============================================================
            # VALIDAÇÃO DE SENHA FORTE
            # ============================================================
            def validar_senha_forte(senha):
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

            valido, mensagem = validar_senha_forte(nova_senha)
            if not valido:
                flash(mensagem, "danger")
                return render_template("geral/alterar_senha.html")

            if nova_senha != confirmar_senha:
                flash("As senhas não coincidem.", "danger")
                return render_template("geral/alterar_senha.html")

            usuario.senha_criptografada = nova_senha
            db.session.commit()

            flash("Senha alterada com sucesso!", "success")
            return render_template("geral/alterar_senha.html")

        return render_template("geral/alterar_senha.html")

    def meus_agendamentos(self):
        agendamentos = self.agendamento_service.listar_por_usuario(session.get('usuario'))

        # Ordem de prioridade dos status
        prioridade = {
            'agendado': 0,
            'em_andamento': 1,
            'finalizado': 2,
            'cancelado': 3
        }

        agendamentos.sort(
            key=lambda x: (
                prioridade.get(x.status or 'agendado', 99),
                x.data or '',
                x.horario or ''
            ),
            reverse=False
        )
        # Inverte dentro de cada grupo de status (data mais recente primeiro)
        agendamentos_ordenados = []
        for status_nome in ['agendado', 'em_andamento', 'finalizado', 'cancelado']:
            grupo = [a for a in agendamentos if (a.status or 'agendado') == status_nome]
            grupo.sort(key=lambda x: (x.data or '', x.horario or ''), reverse=True)
            agendamentos_ordenados.extend(grupo)

        agendamentos = agendamentos_ordenados

        return render_template(
            "geral/meus_agendamentos.html",
            agendamentos=agendamentos,
            admin=session.get("usuario") == ADMIN_EMAIL
        )

    # ============================================================
    # API — DASHBOARD DO CLIENTE
    # ============================================================
    def api_dashboard_cliente(self):
        """Retorna dados agregados dos agendamentos do cliente logado."""
        email = session.get('usuario')
        if not email:
            return jsonify({"erro": "não autenticado"}), 401

        agendamentos = Agendamento.query.filter_by(usuario=email).all()

        # ---------------------------------------------
        # 1. Total por status
        # ---------------------------------------------
        total_agendado = sum(1 for a in agendamentos if a.status == 'agendado')
        total_em_andamento = sum(1 for a in agendamentos if a.status == 'em_andamento')
        total_finalizado = sum(1 for a in agendamentos if a.status == 'finalizado')
        total_cancelado = sum(1 for a in agendamentos if a.status == 'cancelado')

        # ---------------------------------------------
        # 2. Passeios por mês (últimos 6 meses)
        # ---------------------------------------------
        hoje = datetime.now()
        meses_labels = []
        meses_dados = []
        for i in range(5, -1, -1):
            # Calcula o primeiro dia do mês i meses atrás
            ano = hoje.year
            mes = hoje.month - i
            while mes <= 0:
                mes += 12
                ano -= 1
            prefixo = f"{ano:04d}-{mes:02d}"
            meses_labels.append(f"{mes:02d}/{ano}")

            # Conta agendamentos que começam com esse prefixo de data
            count = sum(1 for a in agendamentos if a.data.startswith(prefixo))
            meses_dados.append(count)

        # ---------------------------------------------
        # 3. Roteiros mais feitos (donut)
        # ---------------------------------------------
        roteiros_count = {}
        for a in agendamentos:
            nome = ROTEIROS.get(a.roteiro, {}).get('nome', 'Não definido')
            roteiros_count[nome] = roteiros_count.get(nome, 0) + 1

        # ---------------------------------------------
        # 4. Total de passeios (contagem geral)
        # ---------------------------------------------
        total_passeios = len([a for a in agendamentos if a.status != 'cancelado'])

        return jsonify({
            "total_agendado": total_agendado,
            "total_em_andamento": total_em_andamento,
            "total_finalizado": total_finalizado,
            "total_cancelado": total_cancelado,
            "total_passeios": total_passeios,
            "meses_labels": meses_labels,
            "meses_dados": meses_dados,
            "roteiros_labels": list(roteiros_count.keys()),
            "roteiros_dados": list(roteiros_count.values())
        })

    def minhas_estatisticas(self):
        """Renderiza a página de estatísticas do cliente."""
        return render_template("geral/minhas_estatisticas.html")