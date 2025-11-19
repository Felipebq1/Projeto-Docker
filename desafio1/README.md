# Desafio 1 

## Visão geral
Dois containers Docker se comunicam dentro de uma rede bridge customizada:

- `web`: API Flask que expõe `GET /` e `GET /health` na porta `8080`.
- `client`: script em Alpine Linux que realiza requisições periódicas via `curl` e registra os resultados no log.

A rede `desafio1_network` garante resolução de nomes (`web`, `client`) e isolamento dos serviços.

## Arquitetura & Fluxo
- O `docker-compose.yml` cria automaticamente a rede nomeada e conecta ambos os serviços.
- O container `web` responde com JSON simples confirmando o estado do servidor.
- O container `client` usa a variável `TARGET_URL` (padrão `http://web:8080/health`) para pingar o servidor a cada `POLL_INTERVAL` segundos (padrão `5`).
- Os logs do `client` evidenciam tanto o envio quanto o recebimento das respostas.

```
[client] --curl--> [rede desafio1_network] --HTTP--> [web Flask]
```

## Pré-requisitos
- Docker 20.10+ e Docker Compose Plugin.

## Passo a passo
1. Acesse a pasta do desafio:
   ```powershell
   cd desafio1
   ```
2. Construa e suba os serviços:
   ```powershell
   docker compose up --build
   ```
3. Em outro terminal, valide manualmente o endpoint:
   ```powershell
   curl http://localhost:8080/health
   ```
4. Acompanhe a troca de mensagens:
   ```powershell
   docker compose logs -f client
   ```
5. Para encerrar:
   ```powershell
   docker compose down
   ```
