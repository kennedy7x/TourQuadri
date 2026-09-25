from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_file
from datetime import datetime, timedelta
from io import BytesIO
from math import ceil
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from tourquadri import db, ADMIN_EMAIL
from tourquadri.models import ROTEIROS
from tourquadri.services import (
    AgendamentoService, MaquinaService, BloqueioService, EmailService, UsuarioService, LogService
)


class AdminController:
    def __init__(self):
        self.agendamento_service = AgendamentoService()
        self.maquina_service = MaquinaService()
        self.bloqueio_service = BloqueioService()
        self.email_service = EmailService()
        self.usuario_service = UsuarioService()
        self.log_service = LogService()

    def _log(self, acao, detalhes=None):
        """Atalho pra registrar log com o admin logado + IP"""
        from flask import request
        self.log_service.registrar(
            admin_email=session.get('usuario'),
            acao=acao,
            detalhes=detalhes,
            ip=self.log_service._get_ip(request)
        )

    def dashboard(self):
        todos = self.agendamento_service.listar_todos()
        hoje = datetime.now().date().isoformat()

        return render_template(
            "adm/admin.html",
            total_agendamentos=len(todos),
            total_agendados=len([a for a in todos if a.status == "agendado"]),
            total_em_andamento=len([a for a in todos if a.status == "em_andamento"]),
            total_finalizados=len([a for a in todos if a.status == "finalizado"]),
            total_cancelados=len([a for a in todos if a.status == "cancelado"]),
            agendamentos_hoje=len([a for a in todos if a.data == hoje and a.status == "agendado"]),
            ultimos=sorted(todos, key=lambda x: x.data_criacao if x.data_criacao else "", reverse=True)[:5]
        )

    def gerenciar_agendamentos(self):
        pagina = request.args.get('pagina', 1, type=int)
        itens_por_pagina = 10

        todos = self.agendamento_service.listar_todos()

        filtro_data = request.args.get("data", "")
        filtro_horario = request.args.get("horario", "")
        filtro_cliente = request.args.get("cliente", "")
        filtro_status = request.args.get("status", "")

        agendamentos = todos.copy()

        if filtro_data:
            agendamentos = [a for a in agendamentos if a.data == filtro_data]
        if filtro_horario:
            agendamentos = [a for a in agendamentos if a.horario == filtro_horario]
        if filtro_cliente:
            agendamentos = [
                a for a in agendamentos
                if filtro_cliente.lower() in a.nome_cliente.lower()
                or filtro_cliente.lower() in a.email_cliente.lower()
            ]
        if filtro_status:
            agendamentos = [a for a in agendamentos if a.status == filtro_status]

        agendamentos.sort(key=lambda x: (x.data, x.horario))

        total_itens = len(agendamentos)
        total_paginas = ceil(total_itens / itens_por_pagina)

        inicio = (pagina - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina
        agendamentos_paginados = agendamentos[inicio:fim]

        paginas = list(range(1, total_paginas + 1))

        labels = {
            "agendado": "Agendados",
            "em_andamento": "Em Andamento",
            "finalizado": "Finalizados",
            "cancelado": "Cancelados"
        }

        total = len([a for a in todos if a.status == filtro_status]) if filtro_status else len(todos)
        label = labels.get(filtro_status, "Agendamentos") if filtro_status else "Agendamentos"

        return render_template(
            "adm/admin_agendamentos.html",
            agendamentos=agendamentos_paginados,
            total_exibido=total,
            label_exibido=f"Total de Passeios {label}",
            filtro_data=filtro_data,
            filtro_horario=filtro_horario,
            filtro_cliente=filtro_cliente,
            filtro_status=filtro_status,
            pagina_atual=pagina,
            total_paginas=total_paginas,
            paginas=paginas,
            agora=datetime.now()
        )

    def iniciar_passeio(self, agendamento_id):
        # Busca dados antes de iniciar (pra logar)
        agendamentos = self.agendamento_service.listar_todos()
        ag = next((a for a in agendamentos if a.id == agendamento_id), None)

        resultado = self.agendamento_service.iniciar(agendamento_id)

        if resultado['sucesso']:
            if ag:
                self._log(
                    "Iniciou passeio",
                    f"Cliente: {ag.nome_cliente} | Data: {ag.data} {ag.horario} | Roteiro: {ag.roteiro}"
                )
            flash("Passeio iniciado com sucesso!", "success")
        else:
            flash(resultado['mensagem'], "danger")

        return redirect(url_for("admin_agendamentos", status="em_andamento"))

    def finalizar_passeio(self, agendamento_id):
        agendamentos = self.agendamento_service.listar_todos()
        ag = next((a for a in agendamentos if a.id == agendamento_id), None)

        resultado = self.agendamento_service.finalizar(agendamento_id)

        if resultado['sucesso']:
            if ag:
                self._log(
                    "Finalizou passeio",
                    f"Cliente: {ag.nome_cliente} | Data: {ag.data} {ag.horario}"
                )
            flash("Passeio finalizado com sucesso!", "success")
        else:
            flash(resultado['mensagem'], "danger")

        return redirect(url_for("admin_agendamentos", status="finalizado"))

    def cancelar_agendamento(self, agendamento_id):
        agendamentos = self.agendamento_service.listar_todos()
        ag = next((a for a in agendamentos if a.id == agendamento_id), None)

        resultado = self.agendamento_service.cancelar(agendamento_id, 'admin')

        if resultado['sucesso']:
            if ag:
                self._log(
                    "Cancelou agendamento",
                    f"Cliente: {ag.nome_cliente} | Data: {ag.data} {ag.horario}"
                )
            flash("Agendamento cancelado com sucesso!", "success")
        else:
            flash(resultado['mensagem'], "danger")

        return redirect(url_for("admin_agendamentos", status="cancelado"))

    def editar_agendamento(self, agendamento_id):
        agendamentos = self.agendamento_service.listar_todos()
        agendamento = next((a for a in agendamentos if a.id == agendamento_id), None)

        if not agendamento:
            flash("Agendamento não encontrado.", "danger")
            return redirect(url_for("admin_agendamentos"))

        hoje = datetime.now().date()
        agora = datetime.now()

        if agora.hour >= 17:
            data_minima = (hoje + timedelta(days=1)).isoformat()
        else:
            data_minima = hoje.isoformat()

        data_limite = (hoje + timedelta(days=30)).isoformat()
        maquinas = self.maquina_service.listar_como_dict()

        if request.method == 'POST':
            status = request.form.get("status", "agendado")

            # ============================================================
            # SE FOR CANCELADO
            # ============================================================
            if status == "cancelado":
                agendamento.status = "cancelado"
                agendamento.cancelado_por = "admin"
                agendamento.data_cancelamento = datetime.now().isoformat()
                db.session.commit()
                flash("Agendamento cancelado com sucesso!", "success")
                return redirect(url_for("admin_agendamentos", status="cancelado"))

            # ============================================================
            # SE FOR AGENDADO (REATIVAR)
            # ============================================================
            if status == "agendado":
                agendamento.status = "agendado"
                agendamento.cancelado_por = None
                agendamento.data_cancelamento = None
                db.session.commit()
                flash("Agendamento reativado com sucesso!", "success")
                return redirect(url_for("admin_agendamentos", status="agendado"))

            # ============================================================
            # ATUALIZAR DADOS DO AGENDAMENTO
            # ============================================================
            nome_cliente = request.form.get("nome_cliente")
            telefone_cliente = request.form.get("telefone_cliente")
            email_cliente = request.form.get("email_cliente")
            data = request.form.get("data")
            horario = request.form.get("horario")
            roteiro = request.form.get("roteiro", "1")
            maquinas_selecionadas = [int(m) for m in request.form.getlist("maquinas")]

            if not maquinas_selecionadas:
                flash("Selecione pelo menos uma máquina.", "danger")
                return render_template(
                    "adm/admin_editar.html",
                    agendamento=agendamento,
                    maquinas_especificacoes=maquinas,
                    data_minima=data_minima,
                    data_limite=data_limite
                )

            dados = {
                'nome_cliente': nome_cliente,
                'telefone_cliente': telefone_cliente,
                'email_cliente': email_cliente,
                'data': data,
                'horario': horario,
                'roteiro': roteiro,
                'maquinas': maquinas_selecionadas
            }

            resultado = self.agendamento_service.atualizar(agendamento_id, dados)

            if resultado['sucesso']:
                flash("Agendamento atualizado com sucesso!", "success")
                return redirect(url_for("admin_agendamentos", status="agendado"))

            flash(resultado['mensagem'], "danger")

        return render_template(
            "adm/admin_editar.html",
            agendamento=agendamento,
            maquinas_especificacoes=maquinas,
            data_minima=data_minima,
            data_limite=data_limite
        )

    def realizar_agendamento(self):
        hoje = datetime.now().date()
        agora = datetime.now()

        if agora.hour >= 17:
            data_minima = (hoje + timedelta(days=1)).isoformat()
        else:
            data_minima = hoje.isoformat()

        maquinas = self.maquina_service.listar_como_dict()
        bloqueios = self.bloqueio_service.listar_bloqueios()

        return render_template(
            "adm/admin_realizar_agendamento.html",
            agendamento=None,
            hoje=hoje.isoformat(),
            data_minima=data_minima,
            data_limite=(hoje + timedelta(days=30)).isoformat(),
            TOTAL_MAQUINAS=len(maquinas),
            maquinas_especificacoes=maquinas,
            bloqueios=bloqueios
        )

    def enviar_lembrete(self, agendamento_id):
        agendamentos = self.agendamento_service.listar_todos()
        agendamento = next((a for a in agendamentos if a.id == agendamento_id), None)

        if not agendamento:
            flash("Agendamento não encontrado.", "danger")
            return redirect(url_for("admin_agendamentos"))

        email_cliente = agendamento.email_cliente
        nome_cliente = agendamento.nome_cliente
        data_formatada = self._formatar_data(agendamento.data)
        roteiro = ROTEIROS.get(agendamento.roteiro, {}).get('nome', 'Roteiro não definido')

        if self.email_service.enviar_lembrete(
            email_cliente,
            nome_cliente,
            data_formatada,
            agendamento.horario,
            roteiro,
            agendamento.maquinas
        ):
            flash(f"Lembrete enviado com sucesso para {email_cliente}", "success")
        else:
            flash(f"Erro ao enviar lembrete para {email_cliente}", "danger")

        return redirect(url_for("admin_agendamentos"))

    def _formatar_data(self, data_str):
        try:
            data = datetime.strptime(data_str, '%Y-%m-%d')
            return data.strftime('%d/%m/%Y')
        except:
            return data_str

    def gerenciar_horarios(self):
        bloqueios = self.bloqueio_service.listar_bloqueios()
        hoje = datetime.now().date().isoformat()

        return render_template(
            "adm/admin_gerenciar_horarios.html",
            bloqueios=bloqueios,
            hoje=hoje
        )

    def bloquear_horario(self):
        data = request.form.get("data")
        horario = request.form.get("horario")

        resultado = self.bloqueio_service.bloquear(data, horario)

        if resultado['sucesso']:
            self._log("Bloqueou horário", f"Data: {data} | Horário: {horario}")
            flash(f"Horário {horario} do dia {data} bloqueado!", "success")
        else:
            flash(resultado['mensagem'], "danger")

        return redirect(url_for("admin_gerenciar_horarios"))

    def desbloquear_horario(self):
        data = request.form.get("data")
        horario = request.form.get("horario")

        resultado = self.bloqueio_service.desbloquear(data, horario)

        if resultado['sucesso']:
            self._log("Desbloqueou horário", f"Data: {data} | Horário: {horario}")
            flash(f"Horário {horario} do dia {data} desbloqueado!", "success")
        else:
            flash(resultado['mensagem'], "danger")

        return redirect(url_for("admin_gerenciar_horarios"))

    def bloquear_todos_horarios(self):
        data = request.form.get("data")

        resultado = self.bloqueio_service.bloquear_todos(data)

        if resultado['sucesso']:
            self._log("Bloqueou todos os horários", f"Data: {data}")
            flash(f"Todos os horários do dia {data} bloqueados!", "success")
        else:
            flash(resultado.get('mensagem', 'Erro ao bloquear horários'), "danger")

        return redirect(url_for("admin_gerenciar_horarios"))

    def desbloquear_todos_horarios(self):
        data = request.form.get("data")

        resultado = self.bloqueio_service.desbloquear_todos(data)

        if resultado['sucesso']:
            self._log("Desbloqueou todos os horários", f"Data: {data}")
            flash(f"Todos os bloqueios do dia {data} removidos!", "success")
        else:
            flash(resultado.get('mensagem', 'Erro ao desbloquear horários'), "danger")

        return redirect(url_for("admin_gerenciar_horarios"))

    def verificar_bloqueios(self):
        data = request.args.get("data")

        if not data:
            return jsonify({"erro": "Data é obrigatória"})

        horarios = self.bloqueio_service.listar_por_data(data)

        todos = [f"{h:02d}:{m:02d}" for h in range(9, 18) for m in range(0, 60, 10) if not (h == 17 and m > 0)]

        return jsonify({
            "bloqueados": horarios,
            "todos_bloqueados": all(h in horarios for h in todos)
        })

    # ============================================================
    # GERENCIAR MÁQUINAS
    # ============================================================

    def gerenciar_maquinas(self):
        """Lista todas as máquinas (ordenadas por ID)"""
        todas_maquinas = self.maquina_service.listar_todas()
        
        maquinas_dict = {}
        for m in todas_maquinas:
            maquinas_dict[str(m.id)] = {
                'nome_maquina': m.nome_maquina,
                'modelo': m.modelo,
                'cc': m.cc
            }

        return render_template(
            "adm/admin_maquinas.html",
            maquinas=maquinas_dict
        )

    def adicionar_maquina(self):
        nome_maquina = request.form.get("nome_maquina", "").strip()
        modelo = request.form.get("modelo", "").strip()
        cc = request.form.get("cc", "").strip()

        if not nome_maquina or not modelo or not cc:
            flash("Todos os campos são obrigatórios.", "danger")
            return redirect(url_for("admin_maquinas"))

        try:
            self.maquina_service.criar(nome_maquina, modelo, cc)
            self._log(f"Adicionou máquina '{nome_maquina}'", f"Modelo: {modelo}, CC: {cc}")
            flash(f"Máquina '{nome_maquina}' adicionada com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao adicionar máquina: {str(e)}", "danger")

        return redirect(url_for("admin_maquinas"))

    def editar_maquina(self, maquina_id):
        nome_maquina = request.form.get("nome_maquina", "").strip()
        modelo = request.form.get("modelo", "").strip()
        cc = request.form.get("cc", "").strip()

        if not nome_maquina or not modelo or not cc:
            flash("Todos os campos são obrigatórios.", "danger")
            return redirect(url_for("admin_maquinas"))

        resultado = self.maquina_service.atualizar(maquina_id, nome_maquina, modelo, cc)

        if resultado:
            self._log(f"Editou máquina '{nome_maquina}' (ID: {maquina_id})", f"Modelo: {modelo}, CC: {cc}")
            flash(f"Máquina '{nome_maquina}' atualizada com sucesso!", "success")
        else:
            flash("Máquina não encontrada.", "danger")

        return redirect(url_for("admin_maquinas"))

    def excluir_maquina(self, maquina_id):
        maquina = self.maquina_service.buscar_por_id(maquina_id)
        nome_maquina = maquina.nome_maquina if maquina else maquina_id

        resultado = self.maquina_service.excluir(maquina_id)

        if resultado['sucesso']:
            self._log(f"Excluiu máquina '{nome_maquina}' (ID: {maquina_id})")
            flash(resultado['mensagem'], "success")
        else:
            flash(resultado['mensagem'], "danger")

        return redirect(url_for("admin_maquinas"))

    def estatisticas_maquinas(self):
        stats = self.maquina_service.get_estatisticas()
        return render_template("adm/admin_maquinas_estatisticas.html", stats=stats)

    # ============================================================
    # GERENCIAR ROTEIROS
    # ============================================================

    def gerenciar_roteiros(self):
        return render_template("adm/admin_roteiros.html", ROTEIROS=ROTEIROS)

    def adicionar_roteiro_view(self):
        return render_template("adm/admin_roteiro_editar.html", roteiro=None, id=None)

    def editar_roteiro_admin(self, roteiro_id):
        roteiro = ROTEIROS.get(roteiro_id)
        if not roteiro:
            flash("Roteiro não encontrado.", "danger")
            return redirect(url_for("admin_roteiros"))
        return render_template("adm/admin_roteiro_editar.html", roteiro=roteiro, id=roteiro_id)

    def adicionar_roteiro(self):
        try:
            novo_id = str(max([int(k) for k in ROTEIROS.keys()], default=0) + 1)

            ROTEIROS[novo_id] = {
                "nome": request.form.get("nome"),
                "duracao": int(request.form.get("duracao")),
                "preco": request.form.get("preco"),
                "preco_max": request.form.get("preco"),
                "tipo": request.form.get("tipo"),
                "paradas": request.form.get("paradas", "1 parada para fotos"),
                "descricao_curta": request.form.get("descricao")[:100],
                "descricao_completa": request.form.get("descricao"),
                "inclui": [i.strip() for i in request.form.get("inclui", "").split(',') if i.strip()] or ["Passeio de quadriciclo", "Equipamento de segurança", "Guia especializado"],
                "foto_principal": request.form.get("foto_principal", "default.jpg"),
                "galeria": [g.strip() for g in request.form.get("galeria", "").split(',') if g.strip()]
            }

            self._log(f"Adicionou roteiro '{request.form.get('nome')}'")

            import json
            with open("roteiros.json", "w", encoding="utf-8") as f:
                json.dump(ROTEIROS, f, indent=4, ensure_ascii=False)

            flash("Roteiro adicionado com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao adicionar roteiro: {str(e)}", "danger")

        return redirect(url_for("admin_roteiros"))

    def editar_roteiro(self, roteiro_id):
        try:
            if roteiro_id not in ROTEIROS:
                flash("Roteiro não encontrado.", "danger")
                return redirect(url_for("admin_roteiros"))

            inclui = [i.strip() for i in request.form.get("inclui", "").split(',') if i.strip()]
            galeria = [g.strip() for g in request.form.get("galeria", "").split(',') if g.strip()]

            ROTEIROS[roteiro_id].update({
                "nome": request.form.get("nome"),
                "duracao": int(request.form.get("duracao")),
                "preco": request.form.get("preco"),
                "preco_max": request.form.get("preco"),
                "tipo": request.form.get("tipo"),
                "paradas": request.form.get("paradas", "1 parada para fotos"),
                "descricao_curta": request.form.get("descricao")[:100],
                "descricao_completa": request.form.get("descricao"),
                "inclui": inclui if inclui else ["Passeio de quadriciclo", "Equipamento de segurança", "Guia especializado"],
                "galeria": galeria,
                "foto_principal": request.form.get("foto_principal", "default.jpg")
            })

            self._log(f"Editou roteiro '{request.form.get('nome')}' (ID: {roteiro_id})")

            import json
            with open("roteiros.json", "w", encoding="utf-8") as f:
                json.dump(ROTEIROS, f, indent=4, ensure_ascii=False)

            flash("Roteiro atualizado com sucesso!", "success")
        except Exception as e:
            flash(f"Erro ao editar roteiro: {str(e)}", "danger")

        return redirect(url_for("admin_roteiros"))

    def excluir_roteiro(self, roteiro_id):
        try:
            if roteiro_id in ROTEIROS:
                nome_roteiro = ROTEIROS[roteiro_id]['nome']
                del ROTEIROS[roteiro_id]

                self._log(f"Excluiu roteiro '{nome_roteiro}' (ID: {roteiro_id})")

                import json
                with open("roteiros.json", "w", encoding="utf-8") as f:
                    json.dump(ROTEIROS, f, indent=4, ensure_ascii=False)

                flash("Roteiro excluído com sucesso!", "success")
            else:
                flash("Roteiro não encontrado.", "danger")
        except Exception as e:
            flash(f"Erro ao excluir roteiro: {str(e)}", "danger")

        return redirect(url_for("admin_roteiros"))

    def exportar_pdf(self):
        agendamentos = self.agendamento_service.listar_todos()
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(
            "TourQuadri - Relatório de Agendamentos",
            ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, alignment=TA_CENTER, spaceAfter=30)
        ))
        elements.append(Spacer(1, 20))

        data = [['Data', 'Horário', 'Cliente', 'Telefone', 'Email', 'Máquinas', 'Roteiro', 'Duração', 'Status']]

        for a in agendamentos:
            roteiro = ROTEIROS.get(a.roteiro, {})
            maqs_str = ', '.join(map(str, a.maquinas))
            status_display = {
                'agendado': 'AGENDADO',
                'em_andamento': 'EM ANDAMENTO',
                'finalizado': 'FINALIZADO',
                'cancelado': 'CANCELADO'
            }.get(a.status, a.status.upper())

            data.append([
                self._formatar_data(a.data),
                a.horario,
                a.nome_cliente,
                a.telefone_cliente,
                a.email_cliente,
                maqs_str,
                roteiro.get('nome', 'Roteiro não definido'),
                f"{roteiro.get('duracao', 0)} min",
                status_display
            ])

        table = Table(data, colWidths=[70, 55, 90, 80, 110, 70, 110, 55, 90])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        elements.append(table)
        doc.build(elements)
        buffer.seek(0)

        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='agendamentos.pdf')

    def visao_geral(self):
        """Renderiza a página de visão geral com gráficos."""
        return render_template("adm/admin_visao_geral.html")

    # ============================================================
    # API — DASHBOARD DO ADMIN
    # ============================================================
    def api_dashboard_admin(self):
        """Retorna dados agregados para os gráficos do dashboard admin."""
        agendamentos = self.agendamento_service.listar_todos()

        # ---------------------------------------------
        # 1. Agendamentos por dia (últimos 30 dias)
        # ---------------------------------------------
        hoje = datetime.now().date()
        dias_labels = []
        dias_dados = []
        for i in range(29, -1, -1):
            dia = hoje - timedelta(days=i)
            prefixo = dia.isoformat()
            dias_labels.append(dia.strftime('%d/%m'))
            count = sum(1 for a in agendamentos if a.data == prefixo)
            dias_dados.append(count)

        # ---------------------------------------------
        # 2. Roteiros mais procurados (donut)
        # ---------------------------------------------
        roteiros_count = {}
        for a in agendamentos:
            if a.status == 'cancelado':
                continue
            nome = ROTEIROS.get(a.roteiro, {}).get('nome', 'Não definido')
            roteiros_count[nome] = roteiros_count.get(nome, 0) + 1

        # ---------------------------------------------
        # 3. Máquinas — TODAS, em ordem de ID (0 a 14)
        # ---------------------------------------------
        from tourquadri.models import Maquina, EstatisticaMaquina
        todas_maquinas = Maquina.query.order_by(Maquina.id).all()
        stats_dict = {e.maquina_id: e.uso for e in EstatisticaMaquina.query.all()}

        maquinas_labels = [m.nome_maquina for m in todas_maquinas]
        maquinas_dados = [stats_dict.get(m.id, 0) for m in todas_maquinas]

        # ---------------------------------------------
        # 4. Agendamentos por horário (barras)
        # ---------------------------------------------
        horarios_count = {}
        for a in agendamentos:
            if a.status == 'cancelado':
                continue
            horarios_count[a.horario] = horarios_count.get(a.horario, 0) + 1

        horarios_ordenados = sorted(horarios_count.keys())
        horarios_dados_ordenados = [horarios_count[h] for h in horarios_ordenados]

        return jsonify({
            "dias_labels": dias_labels,
            "dias_dados": dias_dados,
            "roteiros_labels": list(roteiros_count.keys()),
            "roteiros_dados": list(roteiros_count.values()),
            "maquinas_labels": maquinas_labels,
            "maquinas_dados": maquinas_dados,
            "horarios_labels": horarios_ordenados,
            "horarios_dados": horarios_dados_ordenados
        })

    def logs(self):
        """Página de visualização dos logs do admin"""
        pagina = request.args.get('pagina', 1, type=int)
        filtro_admin = request.args.get('admin', '').strip()
        filtro_categoria = request.args.get('categoria', '').strip()
        filtro_data = request.args.get('data', '').strip()
        filtro_busca = request.args.get('busca', '').strip()

        resultado = self.log_service.listar_paginado(
            pagina=pagina,
            itens_por_pagina=20,
            filtro_admin=filtro_admin or None,
            filtro_categoria=filtro_categoria or None,
            filtro_data=filtro_data or None,
            filtro_busca=filtro_busca or None
        )

        return render_template(
            "adm/admin_logs.html",
            logs=resultado['logs'],
            total=resultado['total'],
            pagina_atual=resultado['pagina_atual'],
            total_paginas=resultado['total_paginas'],
            paginas=resultado['paginas'],
            filtro_admin=filtro_admin,
            filtro_categoria=filtro_categoria,
            filtro_data=filtro_data,
            filtro_busca=filtro_busca,
            admins_unicos=self.log_service.listar_admins_unicos(),
            categorias=self.log_service.get_categorias()
        )