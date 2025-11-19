#!/usr/bin/env python3

import os
import psycopg2
import redis
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "desafio3")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

REDIS_HOST = os.getenv("REDIS_HOST", "cache")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        return None


def get_redis_connection():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
        return r
    except Exception as e:
        return None


def init_database():
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS acessos (
                id SERIAL PRIMARY KEY,
                endpoint TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
        return False


@app.route("/")
def index():
    resultado = {
        "servico": "web",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "servicos": {}
    }
    
    db_conn = get_db_connection()
    if db_conn:
        resultado["servicos"]["database"] = {
            "status": "conectado",
            "host": DB_HOST,
            "port": DB_PORT
        }
        db_conn.close()
    else:
        resultado["servicos"]["database"] = {
            "status": "desconectado",
            "erro": "Não foi possível conectar ao PostgreSQL"
        }
    
    redis_conn = get_redis_connection()
    if redis_conn:
        resultado["servicos"]["cache"] = {
            "status": "conectado",
            "host": REDIS_HOST,
            "port": REDIS_PORT
        }
        redis_conn.close()
    else:
        resultado["servicos"]["cache"] = {
            "status": "desconectado",
            "erro": "Não foi possível conectar ao Redis"
        }
    
    return jsonify(resultado)


@app.route("/db/test")
def db_test():
    conn = get_db_connection()
    if not conn:
        return jsonify({"erro": "Não foi possível conectar ao banco de dados"}), 500
    
    try:
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO acessos (endpoint, timestamp) VALUES (%s, %s) RETURNING id",
            ("/db/test", datetime.now())
        )
        acesso_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM acessos")
        total = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({
            "status": "sucesso",
            "acesso_id": acesso_id,
            "total_acessos": total,
            "mensagem": "Dados inseridos e consultados com sucesso"
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/cache/test")
def cache_test():
    redis_conn = get_redis_connection()
    if not redis_conn:
        return jsonify({"erro": "Não foi possível conectar ao Redis"}), 500
    
    try:
        contador = redis_conn.incr("contador_acessos")
        
        timestamp = datetime.now().isoformat()
        redis_conn.set("ultimo_acesso", timestamp)
        
        ultimo_acesso = redis_conn.get("ultimo_acesso")
        
        return jsonify({
            "status": "sucesso",
            "contador": contador,
            "ultimo_acesso": ultimo_acesso,
            "mensagem": "Cache funcionando corretamente"
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/integracao")
def integracao():
    resultado = {
        "status": "sucesso",
        "operacoes": []
    }
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO acessos (endpoint, timestamp) VALUES (%s, %s) RETURNING id",
                ("/integracao", datetime.now())
            )
            acesso_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            resultado["operacoes"].append({
                "servico": "database",
                "acao": "inserir",
                "status": "sucesso",
                "acesso_id": acesso_id
            })
        except Exception as e:
            resultado["operacoes"].append({
                "servico": "database",
                "acao": "inserir",
                "status": "erro",
                "erro": str(e)
            })
    
    redis_conn = get_redis_connection()
    if redis_conn:
        try:
            contador = redis_conn.incr("integracao_contador")
            redis_conn.set("integracao_timestamp", datetime.now().isoformat())
            resultado["operacoes"].append({
                "servico": "cache",
                "acao": "incrementar_contador",
                "status": "sucesso",
                "contador": contador
            })
        except Exception as e:
            resultado["operacoes"].append({
                "servico": "cache",
                "acao": "incrementar_contador",
                "status": "erro",
                "erro": str(e)
            })
    
    return jsonify(resultado)


if __name__ == "__main__":
    print("=" * 50)
    print("Serviço WEB - Desafio 3")
    print("=" * 50)
    print(f"Conectando ao banco: {DB_HOST}:{DB_PORT}")
    print(f"Conectando ao cache: {REDIS_HOST}:{REDIS_PORT}")
    
    if init_database():
        print("Banco de dados inicializado com sucesso!")
    else:
        print("Aviso: Não foi possível inicializar o banco de dados")
    
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=False)

