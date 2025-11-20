from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = [
    {"id": 101, "user_id": 1, "valor": 250.0, "status": "enviado"},
    {"id": 102, "user_id": 2, "valor": 90.5, "status": "processando"},
    {"id": 103, "user_id": 1, "valor": 120.0, "status": "entregue"},
]


@app.get("/orders")
def listar_pedidos():
    return jsonify({"orders": ORDERS})


@app.get("/health")
def health():
    return jsonify({"status": "ok", "total": len(ORDERS)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)


