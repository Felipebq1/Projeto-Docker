# Desafio 5 — Microsserviços com API Gateway

## Visão Geral

Este desafio cria uma arquitetura com três containers:

- **Serviço de Usuários** (`usuarios/`): fornece dados de usuários.
- **Serviço de Pedidos** (`pedidos/`): expõe pedidos associados a usuários.
- **API Gateway** (`gateway/`): ponto único de entrada, roteando `/users` para o serviço de usuários e `/orders` para o serviço de pedidos.

Todos os serviços rodam em Docker, orquestrados por `docker-compose`. O gateway adiciona logging simples (via Flask) e padroniza o payload retornado, contendo a fonte original e os dados agregados.

## Arquitetura

```
              ┌──────────────────────────┐
              │        API Gateway        │
              │  Flask + requests         │
Cliente ─────▶│  /users  /orders /health │────┐
              └────────────┬─────────────┘    │
                           │                  │
            HTTP (rede docker-compose)        │
                           │                  │
         ┌─────────────────▼──────┐   ┌───────▼────────────────┐
         │ Serviço de Usuários    │   │ Serviço de Pedidos     │
         │ Flask /users /health   │   │ Flask /orders /health  │
         └────────────────────────┘   └────────────────────────┘
```

- DNS automático via rede padrão do Compose (`usuarios`, `pedidos`, `gateway`).
- Gateway funciona como BFF simples, centralizando timeout, formatação de resposta e variáveis de ambiente.

## Componentes

### 1. Serviço de Usuários (`usuarios/`)
- Expõe `GET /users` com lista fixa de usuários (id, nome, email, status).
- `GET /health` retorna status e total de registros.
- Porta interna `6000`.

### 2. Serviço de Pedidos (`pedidos/`)
- Expõe `GET /orders` com pedidos (id, user_id, valor, status).
- `GET /health` indica disponibilidade.
- Porta interna `6001`.

### 3. API Gateway (`gateway/`)
- Exponde `GET /users` e `GET /orders`, chamando serviços downstream via `requests`.
- `GET /health` mostra URLs configuradas para cada backend.
- Variáveis configuráveis: `USERS_SERVICE_URL`, `ORDERS_SERVICE_URL`, `REQUEST_TIMEOUT`.
- Porta publicada `8080`.

## Fluxo de Funcionamento

1. Usuário chama `http://localhost:8080/users`.
2. Gateway faz `GET http://usuarios:6000/users` dentro da rede Docker.
3. Resposta é enriquecida com a propriedade `source` e retornada ao cliente.
4. O mesmo padrão vale para `/orders`.
5. Se algum serviço estiver indisponível, o gateway propagará erro 5xx (via `raise_for_status()`), facilitando observabilidade.

## Instruções de Execução

### Pré-requisitos
- Docker Engine + Compose Plugin

### Passo a passo

```bash
cd desafio5
docker compose up --build
```

## Testes Manuais Sugeridos

1. `curl http://localhost:8080/health` → Verifica rotas configuradas.
2. `curl http://localhost:8080/users` → Deve retornar JSON com chave `users` e `source` indicando o serviço interno.
3. `curl http://localhost:8080/orders` → Valida integração com o serviço de pedidos.
4. Simular indisponibilidade: pare o container `desafio5_pedidos` e repita o passo 3 para ver o gateway retornando erro (mostra comportamento esperado).

## Decisões Técnicas

- **Flask** para todos os serviços simplifica a stack e reduz sobrecarga.
- **requests** no gateway provê controle explícito de timeout e tratamento de status HTTP.
- **dados estáticos** para foco em orquestração; facilita substituição futura por bancos ou APIs reais.
- **expose** apenas nos serviços internos para manter isolamento; somente o gateway publica porta no host.

