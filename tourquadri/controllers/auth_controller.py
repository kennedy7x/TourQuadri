from flask import render_template, request, redirect, url_for, session, flash
from tourquadri import ADMIN_EMAIL
from tourquadri.services import UsuarioService, MaquinaService


class AuthController:
    def __init__(self):
        self.usuario_service = UsuarioService()

    def landing(self):
        maquinas = MaquinaService().listar_como_dict()
        return render_template(
            "geral/landing.html",
            TOTAL_MAQUINAS=len(maquinas),
            maquinas_especificacoes=maquinas
        )

    def login(self):
        return render_template("geral/login.html")

    def register(self):
        return render_template("geral/register.html")

    def autenticar(self):
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")

        if not email:
            flash("E-mail é obrigatório.", "danger")
            return render_template("geral/login.html", email=email)

        if not senha:
            flash("Senha é obrigatória.", "danger")
            return render_template("geral/login.html", email=email)

        resultado = self.usuario_service.autenticar(email, senha)

        if resultado['sucesso']:
            usuario = resultado['usuario']
            session.permanent = True
            session["usuario"] = usuario.email
            session["nome"] = usuario.nome
            session["usuario_id"] = usuario.id

            if usuario.admin:
                from tourquadri.services import LogService
                log_service = LogService()
                log_service.registrar(
                    admin_email=usuario.email,
                    acao="Login",
                    detalhes="Login realizado com sucesso",
                    ip=log_service._get_ip(request)
                )

            flash(f"Bem-vindo(a), {usuario.nome}!", "success")
            if usuario.admin:
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("dashboard"))

        flash(resultado['mensagem'], "danger")
        return render_template("geral/login.html", email=email)

    def salvar_usuario(self):
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "").strip()
        confirmar_senha = request.form.get("confirmar_senha", "").strip()

        resultado = self.usuario_service.iniciar_cadastro(nome, telefone, email, senha, confirmar_senha)

        if resultado['sucesso']:
            if resultado.get('email_enviado', True):
                flash("Enviamos um código para seu email. Confirme para ativar sua conta.", "success")
            else:
                flash("Não foi possível enviar o email. Verifique se o endereço está correto ou tente novamente mais tarde.", "danger")
            return render_template("geral/verificar_cadastro.html", email=email)

        return render_template(
            "geral/register.html",
            erros=resultado.get('erros', {}),
            nome=nome,
            telefone=telefone,
            email=email
        )

    def verificar_cadastro(self):
        email = request.args.get("email", "")
        if not email:
            flash("Email não informado.", "danger")
            return redirect(url_for("register"))
        return render_template("geral/verificar_cadastro.html", email=email)

    def confirmar_cadastro(self):
        email = request.form.get("email", "").strip()
        codigo = request.form.get("codigo", "").strip()

        if not codigo or len(codigo) != 6:
            flash("Código deve ter 6 dígitos.", "danger")
            return render_template("geral/verificar_cadastro.html", email=email)

        resultado = self.usuario_service.confirmar_cadastro(email, codigo)

        if resultado['sucesso']:
            usuario = resultado['usuario']
            session.permanent = True
            session["usuario"] = usuario.email
            session["nome"] = usuario.nome
            session["usuario_id"] = usuario.id
            flash(f"Conta criada com sucesso! Bem-vindo(a), {usuario.nome}!", "success")
            return redirect(url_for("dashboard"))

        flash(resultado['mensagem'], "danger")
        return render_template("geral/verificar_cadastro.html", email=email)

    def reenviar_codigo_cadastro(self):
        from tourquadri import db
        from tourquadri.models import CodigoVerificacao
        from tourquadri.services import gerar_codigo
        from datetime import datetime, timedelta
        import json

        email = request.form.get("email", "").strip()

        if not email:
            flash("Email não informado.", "danger")
            return redirect(url_for("register"))

        codigo_db = CodigoVerificacao.query.filter_by(email=email, tipo='cadastro').first()

        if not codigo_db:
            flash("Cadastro expirado. Faça o cadastro novamente.", "danger")
            return redirect(url_for("register"))

        novo_codigo = gerar_codigo()
        codigo_db.codigo = novo_codigo
        codigo_db.expiracao = (datetime.now() + timedelta(minutes=15)).isoformat()
        db.session.commit()

        dados = json.loads(codigo_db.dados_cadastro_json)
        email_enviado = self.usuario_service.email_service.enviar_codigo_cadastro(email, novo_codigo, dados['nome'])

        if email_enviado:
            flash("Novo código enviado para seu email!", "success")
        else:
            flash("Não foi possível enviar o email. Tente novamente mais tarde.", "danger")

        return render_template("geral/verificar_cadastro.html", email=email)

    def logout(self):
        email_logado = session.get('usuario')
        usuario_id = session.get('usuario_id')

        if email_logado and usuario_id:
            from tourquadri.services import UsuarioService, LogService
            usuario = UsuarioService().buscar_por_id(usuario_id)
            if usuario and usuario.admin:
                log_service = LogService()
                log_service.registrar(
                    admin_email=email_logado,
                    acao="Logout",
                    detalhes="Logout realizado",
                    ip=log_service._get_ip(request)
                )

        session.clear()
        flash("Você foi desconectado!", "warning")
        return redirect(url_for("landing"))

    def esqueci_senha(self):
        return render_template("geral/esqueci_senha.html")

    def solicitar_codigo(self):
        email = request.form.get("email", "").strip()

        if not email:
            flash("E-mail é obrigatório.", "danger")
            return render_template("geral/esqueci_senha.html")

        resultado = self.usuario_service.solicitar_recuperacao(email)

        if resultado['sucesso']:
            if resultado.get('email_enviado', True):
                flash("Código enviado para seu email!", "success")
            else:
                flash("Não foi possível enviar o email. Verifique se o endereço está correto ou tente novamente mais tarde.", "danger")
            return render_template("geral/verificar_codigo.html", email=email)

        flash(resultado['mensagem'], "danger")
        return render_template("geral/esqueci_senha.html", email=email)

    def verificar_codigo(self):
        email = request.form.get("email", "").strip()
        codigo = request.form.get("codigo", "").strip()

        if not codigo or len(codigo) != 6:
            flash("Código deve ter 6 dígitos.", "danger")
            return render_template("geral/verificar_codigo.html", email=email)

        resultado = self.usuario_service.verificar_codigo(email, codigo)

        if resultado['sucesso']:
            session["reset_email"] = email
            flash("Código verificado com sucesso!", "success")
            return redirect(url_for("redefinir_senha"))

        flash(resultado['mensagem'], "danger")
        return render_template("geral/verificar_codigo.html", email=email)

    def redefinir_senha(self):
        if "reset_email" not in session:
            flash("Acesso não autorizado.", "danger")
            return redirect(url_for("login"))
        return render_template("geral/redefinir_senha.html")

    def salvar_nova_senha(self):
        if "reset_email" not in session:
            flash("Acesso não autorizado.", "danger")
            return redirect(url_for("login"))

        email = session["reset_email"]
        nova_senha = request.form.get("nova_senha", "").strip()
        confirmar_senha = request.form.get("confirmar_senha", "").strip()

        resultado = self.usuario_service.redefinir_senha(email, nova_senha, confirmar_senha)

        if resultado['sucesso']:
            session.pop("reset_email", None)
            flash("Senha redefinida com sucesso! Faça login.", "success")
            return redirect(url_for("login"))

        flash(resultado['mensagem'], "danger")
        return render_template("geral/redefinir_senha.html")