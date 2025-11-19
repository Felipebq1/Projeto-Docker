#!/usr/bin/env python3

import sqlite3
import os
from datetime import datetime

DB_PATH = "/data/desafio2.db"

def criar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            criado_em TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"[ESCRITOR] Banco de dados criado/verificado em {DB_PATH}")

def inserir_dados():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    usuarios = [
        ("João Silva", "joao@example.com"),
        ("Maria Santos", "maria@example.com"),
        ("Pedro Oliveira", "pedro@example.com"),
    ]
    
    agora = datetime.now().isoformat()
    
    for nome, email in usuarios:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, criado_em) VALUES (?, ?, ?)",
            (nome, email, agora)
        )
        print(f"[ESCRITOR] Inserido: {nome} ({email})")
    
    conn.commit()
    conn.close()
    print(f"[ESCRITOR] Total de registros inseridos: {len(usuarios)}")

def listar_dados():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT id, nome, email, criado_em FROM usuarios")
    registros = cursor.fetchall()
    
    print(f"\n[ESCRITOR] Total de registros no banco: {total}")
    for reg in registros:
        print(f"  ID: {reg[0]}, Nome: {reg[1]}, Email: {reg[2]}, Criado: {reg[3]}")
    
    conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Container ESCRITOR - Desafio 2")
    print("=" * 50)
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    criar_banco()
    inserir_dados()
    listar_dados()
    
    print("\n[ESCRITOR] Dados persistidos com sucesso no volume Docker!")
    print("=" * 50)

