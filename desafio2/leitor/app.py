#!/usr/bin/env python3

import sqlite3
import os
import sys

DB_PATH = "/data/desafio2.db"

def verificar_banco():
    if not os.path.exists(DB_PATH):
        print(f"[LEITOR] ERRO: Banco de dados não encontrado em {DB_PATH}")
        print("[LEITOR] Certifique-se de que o container escritor foi executado primeiro.")
        sys.exit(1)
    
    print(f"[LEITOR] Banco de dados encontrado em {DB_PATH}")

def ler_dados():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]
        
        if total == 0:
            print("[LEITOR] O banco existe mas está vazio.")
            return
        
        cursor.execute("SELECT id, nome, email, criado_em FROM usuarios ORDER BY id")
        registros = cursor.fetchall()
        
        print("\n" + "=" * 50)
        print("Container LEITOR - Desafio 2")
        print("=" * 50)
        print(f"\n[LEITOR] Total de registros encontrados: {total}\n")
        
        for reg in registros:
            print(f"  ID: {reg[0]}")
            print(f"  Nome: {reg[1]}")
            print(f"  Email: {reg[2]}")
            print(f"  Criado em: {reg[3]}")
            print("-" * 50)
        
        print("\n[LEITOR] ✓ Dados persistidos foram lidos com sucesso!")
        print("[LEITOR] Isso comprova que o volume Docker manteve os dados")
        print("[LEITOR] mesmo após a remoção do container escritor.")
        print("=" * 50)
        
    except sqlite3.OperationalError as e:
        print(f"[LEITOR] ERRO ao ler dados: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    verificar_banco()
    ler_dados()

