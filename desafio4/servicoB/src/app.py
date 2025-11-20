import os
from datetime import datetime

import requests
from flask import Flask, jsonify

app = Flask(__name__)

USERS_API_URL = os.getenv("USERS_API_URL", "http://servicoa:5000/usuarios")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "3"))


def humanizar_periodo(data_iso: str) -> str:
    try:
        inicio = datetime.fromisoformat(data_iso)
        anos = max((datetime.utcnow().year - inicio.year), 0)
        if anos == 0:
            return "menos de 1 ano"
        if anos == 1:
            return "1 ano"
        return f"{anos} anos"
    except ValueError:
        return "tempo desconhecido"


@app.get("/relatorio")
def relatorio():
    resposta = requests.get(USERS_API_URL, timeout=REQUEST_TIMEOUT)
    resposta.raise_for_status()
    usuarios = resposta.json().get("usuarios", [])

    relatorio = [
        f"Usuário {usuario['nome']} ativo há {humanizar_periodo(usuario['ativo_desde'])} "
        f"(desde {usuario['ativo_desde']})."
        for usuario in usuarios
    ]

    return jsonify(
        {
            "fonte": USERS_API_URL,
            "total_usuarios": len(usuarios),
            "relatorio": relatorio,
        }
    )


@app.get("/health")
def healthcheck():
    return jsonify({"status": "ok", "origem": USERS_API_URL})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

