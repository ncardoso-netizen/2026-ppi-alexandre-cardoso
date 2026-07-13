import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/cadastro", methods=("GET", "POST"))
def cadastro():

    if request.method == "POST":

        nome_usuario = request.form["nome_usuario"]
        senha = request.form["senha"]

        db = get_db()

        erro = None

        if not nome_usuario:
            erro = "Nome de usuário é obrigatório."

        elif not senha:
            erro = "Senha é obrigatória."

        if erro is None:
            try:
                db.execute(
                    "INSERT INTO usuario (nome_usuario, senha)"
                    " VALUES (?, ?)",
                    (
                        nome_usuario,
                        generate_password_hash(senha),
                    ),
                )

                db.commit()

            except db.IntegrityError:
                erro = f"O usuário {nome_usuario} já existe."

            else:
                return redirect(
                    url_for("auth.entrar")
                )

        flash(erro)

    return render_template("auth/cadastro.html")



@bp.route("/entrar", methods=("GET", "POST"))
def entrar():

    if request.method == "POST":

        nome_usuario = request.form["nome_usuario"]
        senha = request.form["senha"]

        db = get_db()

        usuario = db.execute(
            "SELECT * FROM usuario WHERE nome_usuario = ?",
            (nome_usuario,),
        ).fetchone()

        erro = None

        if usuario is None:
            erro = "Usuário incorreto."

        elif not check_password_hash(
            usuario["senha"],
            senha
        ):
            erro = "Senha incorreta."

        if erro is None:
            session.clear()

            session["usuario_id"] = usuario["id"]

            return redirect(
                url_for("index")
            )

        flash(erro)

    return render_template("auth/entrar.html")



@bp.before_app_request
def carregar_usuario_logado():

    usuario_id = session.get("usuario_id")

    if usuario_id is None:
        g.usuario = None

    else:

        g.usuario = get_db().execute(
            "SELECT * FROM usuario WHERE id = ?",
            (usuario_id,),
        ).fetchone()



@bp.route("/sair")
def sair():

    session.clear()

    return redirect(
        url_for("index")
    )



def exigir_login(view):

    @functools.wraps(view)

    def wrapped_view(**kwargs):

        if g.usuario is None:
            return redirect(
                url_for("auth.entrar")
            )

        return view(**kwargs)

    return wrapped_view