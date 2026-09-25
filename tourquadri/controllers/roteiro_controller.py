from flask import render_template, redirect, url_for, flash
from tourquadri.models import ROTEIROS
from tourquadri.services import MaquinaService


class RoteiroController:
    def __init__(self):
        self.maquina_service = MaquinaService()

    def listar_roteiros(self):
        return render_template("geral/roteiros.html", ROTEIROS=ROTEIROS)

    def detalhe_roteiro(self, roteiro_id):
        roteiro = ROTEIROS.get(roteiro_id)
        if not roteiro:
            flash("Roteiro não encontrado.", "danger")
            return redirect(url_for("roteiros"))
        return render_template("geral/roteiro_detalhe.html", roteiro=roteiro, id=roteiro_id)

    def agendar_roteiro(self, roteiro_id):
        return redirect(url_for("dashboard", roteiro_selecionado=roteiro_id))

    def listar_maquinas(self):
        maquinas = self.maquina_service.listar_como_dict()
        return render_template(
            "geral/maquinas.html",
            TOTAL_MAQUINAS=len(maquinas),
            maquinas_especificacoes=maquinas
        )