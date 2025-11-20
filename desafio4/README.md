# Desafio 4 — Microsserviços Independentes

## Descrição da Solução

Este desafio implementa dois microsserviços Python/Flask que se comunicam por HTTP sem gateway intermediário. O **Serviço A** expõe uma lista estática de usuários, enquanto o **Serviço B** consome o endpoint de usuários e produz um relatório textual agregando as informações recebidas.

## Arquitetura

```
┌─────────────────────┐     HTTP (porta 5000)     ┌─────────────────────┐
│  Serviço A          │ ─────────────────────────▶ │  Serviço B          │
│  `servicoA/`        │                           │  `servicoB/`        │
│  Flask + JSON       │ ◀──────────────────────── ┤  Flask + Requests   │
│  /usuarios, /health │     Health checks         │  /relatorio, /health│
└─────────┬───────────┘                           └─────────┬───────────┘
          │                                               │
          └─────────────── Rede docker-compose ───────────┘
```

- **Rede**: default do `docker-compose`, garantindo DNS automático (`servicoa` e `servicob`).
- **Comunicação**: Serviço B usa `USERS_API_URL=http://servicoa:5000/usuarios`.
- **Isolamento**: Cada serviço possui seu próprio Dockerfile, dependências e porta exposta.

## Componentes

### Serviço A (`servicoA/`)
- Endpoint principal `GET /usuarios` que responde com JSON em `{ "usuarios": [...] }`.
- Endpoint `GET /health` para verificação rápida.
- Lista estática simula um catálogo de usuários ativos.

### Serviço B (`servicoB/`)
- Endpoint `GET /relatorio` que chama o Serviço A, compõe frases como `Usuário Alice ativo há 5 anos...` e devolve JSON com total e lista.
- Endpoint `GET /health` retorna a URL configurada para o Serviço A.
- Variáveis de ambiente: `USERS_API_URL`, `REQUEST_TIMEOUT`.

### Docker Compose
- Sobe ambos os serviços com uma única rede.
- Expõe as portas locais `5000` (Serviço A) e `5001` (Serviço B).
- Define `depends_on` para garantir que o Serviço A esteja pronto antes do B iniciar.

## Fluxo de Funcionamento

1. O usuário executa `docker compose up --build`.
2. O Serviço A sobe em `http://localhost:5000/usuarios` servindo o JSON.
3. O Serviço B sobe em `http://localhost:5001/relatorio`, faz requisições HTTP ao Serviço A e monta o relatório.
4. Chamadas subsequentes ao Serviço B utilizam o cache inexistente (tudo em tempo real) garantindo que qualquer alteração no Serviço A (futuras versões) seja refletida.

## Instruções de Execução

### Pré-requisitos
- Docker 24+
- Docker Compose Plugin

### Passo a passo

```bash
cd desafio4
docker compose up --build
```

Após o build:
- `http://localhost:5000/usuarios` → JSON de usuários.
- `http://localhost:5001/relatorio` → Relatório textual em JSON.

## Decisões Técnicas

- **Flask**: framework leve, rápido de prototipar e suficiente para o escopo.
- **requests** no Serviço B pela simplicidade no consumo HTTP.
- **Lista estática** no Serviço A para manter o foco em comunicação entre serviços, mas o contrato JSON facilita substituição futura por banco de dados ou API externa.
- **Timeout configurável** evita travamentos em caso de indisponibilidade do Serviço A.
