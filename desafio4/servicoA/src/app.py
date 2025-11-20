from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {
        "id": 1,
        "nome": "Alice",
        "email": "alice@example.com",
        "ativo_desde": "2020-03-12",
    },
    {
        "id": 2,
        "nome": "Bruno",
        "email": "bruno@example.com",
        "ativo_desde": "2019-08-04",
    },
    {
        "id": 3,
        "nome": "Carla",
        "email": "carla@example.com",
        "ativo_desde": "2021-11-23",
    },
]


@app.get("/usuarios")
def listar_usuarios():
    return jsonify({"usuarios": USERS})


@app.get("/health")
def healthcheck():
    return jsonify({"status": "ok", "total": len(USERS)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

