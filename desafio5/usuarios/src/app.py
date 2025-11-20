from flask import Flask, jsonify

app = Flask(__name__)

USERS = [
    {"id": 1, "nome": "Ana Souza", "email": "ana@example.com", "status": "ativo"},
    {"id": 2, "nome": "Carlos Lima", "email": "carlos@example.com", "status": "ativo"},
    {"id": 3, "nome": "Fernanda Dias", "email": "fernanda@example.com", "status": "inativo"},
]


@app.get("/users")
def listar_usuarios():
    return jsonify({"users": USERS})


@app.get("/health")
def health():
    return jsonify({"status": "ok", "total": len(USERS)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)


