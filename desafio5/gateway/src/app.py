import os

import requests
from flask import Flask, jsonify

app = Flask(__name__)

USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL", "http://usuarios:6000/users")
ORDERS_SERVICE_URL = os.getenv("ORDERS_SERVICE_URL", "http://pedidos:6001/orders")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "3"))


def proxy_request(url: str):
    resposta = requests.get(url, timeout=REQUEST_TIMEOUT)
    resposta.raise_for_status()
    return resposta.json()


@app.get("/users")
def gateway_users():
    payload = proxy_request(USERS_SERVICE_URL)
    return jsonify({"source": USERS_SERVICE_URL, **payload})


@app.get("/orders")
def gateway_orders():
    payload = proxy_request(ORDERS_SERVICE_URL)
    return jsonify({"source": ORDERS_SERVICE_URL, **payload})


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "routes": {
                "users": USERS_SERVICE_URL,
                "orders": ORDERS_SERVICE_URL,
            },
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


