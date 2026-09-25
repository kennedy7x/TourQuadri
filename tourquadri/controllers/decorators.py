from functools import wraps
from flask import session, redirect, url_for, flash
from tourquadri import ADMIN_EMAIL


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario" not in session:
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("usuario") != ADMIN_EMAIL:
            flash("Acesso restrito a administradores.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated


def logout_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario" in session:
            flash("Você já está logado.", "info")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated