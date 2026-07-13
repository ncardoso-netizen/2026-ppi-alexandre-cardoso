from flask import (
    Blueprint,
    render_template,
)

from .db import get_db


bp = Blueprint("albuns", __name__)


@bp.route("/")
def index():

    db = get_db()

    albuns = db.execute(
        """
        SELECT a.id, titulo, artista, genero, ano, descricao,
        criado, usuario_id, nome_usuario

        FROM album a
        JOIN usuario u
        ON a.usuario_id = u.id

        ORDER BY criado DESC
        """
    ).fetchall()

    return render_template(
        "albuns/index.html",
        albuns=albuns
    )