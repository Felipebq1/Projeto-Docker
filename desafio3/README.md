# Desafio 3 — Docker Compose Orquestrando Serviços

## Descrição da Solução

Este desafio demonstra a orquestração de múltiplos serviços usando Docker Compose. A solução consiste em três serviços interdependentes: uma aplicação web (Flask), um banco de dados (PostgreSQL) e um cache (Redis), todos configurados com dependências, variáveis de ambiente e rede interna.

### Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    Rede Interna                          │
│              desafio3_network (bridge)                   │
│                                                           │
│  ┌──────────────┐    ┌──────────────┐  ┌──────────────┐ │
│  │   Serviço    │    │   Serviço    │  │   Serviço    │ │
│  │     WEB      │───▶│      DB      │  │    CACHE     │ │
│  │  (Flask)     │    │ (PostgreSQL) │  │   (Redis)    │ │
│  │              │    │              │  │              │ │
│  │ Porta 5000   │    │  Porta 5432  │  │  Porta 6379  │ │
│  │ (exposta)    │    │  (interna)   │  │  (interna)   │ │
│  └──────────────┘    └──────────────┘  └──────────────┘ │
│         │                   │                  │        │
│         └───────────────────┴──────────────────┘        │
│                    depends_on                            │
│              (aguarda healthcheck)                        │
└─────────────────────────────────────────────────────────┘
```

### Componentes

1. **Serviço WEB** (`web/`):
   - Aplicação Flask que expõe API REST
   - Conecta-se ao PostgreSQL para persistência
   - Conecta-se ao Redis para cache
   - Expõe porta 5000 para acesso externo
   - Aguarda serviços db e cache estarem saudáveis antes de iniciar

2. **Serviço DB** (`db`):
   - PostgreSQL 16 Alpine (leve e eficiente)
   - Armazena dados em volume persistente
   - Healthcheck configurado para garantir disponibilidade
   - Acessível apenas na rede interna

3. **Serviço CACHE** (`cache`):
   - Redis 7 Alpine com persistência habilitada
   - Armazena dados em volume persistente
   - Healthcheck configurado
   - Acessível apenas na rede interna

## Decisões Técnicas

### Por que Flask?
- **Simplicidade**: Framework Python leve e fácil de entender
- **Adequado ao objetivo**: Demonstra comunicação entre serviços sem complexidade desnecessária
- **Flexibilidade**: Fácil integração com PostgreSQL e Redis

### Por que PostgreSQL?
- **Robustez**: Banco relacional completo e confiável
- **Padrão da indústria**: Amplamente utilizado em produção
- **Healthcheck nativo**: Suporta verificação de saúde com `pg_isready`

### Por que Redis?
- **Performance**: Cache em memória extremamente rápido
- **Simplicidade**: Fácil de usar e configurar
- **Persistência**: Suporta AOF (Append Only File) para durabilidade

## Funcionamento Detalhado

### Fluxo de Inicialização

1. **Docker Compose inicia os serviços**:
   - Cria a rede `desafio3_network`
   - Cria os volumes `desafio3_db_data` e `desafio3_cache_data`

2. **Serviço DB inicia**:
   - PostgreSQL inicia e aguarda estar pronto
   - Healthcheck verifica com `pg_isready` a cada 5 segundos
   - Quando saudável, marca como `healthy`

3. **Serviço CACHE inicia**:
   - Redis inicia com persistência AOF habilitada
   - Healthcheck verifica com `redis-cli ping` a cada 5 segundos
   - Quando saudável, marca como `healthy`

4. **Serviço WEB inicia** (após db e cache estarem saudáveis):
   - `depends_on` com `condition: service_healthy` garante ordem
   - Flask inicia e tenta conectar ao PostgreSQL e Redis
   - Inicializa tabela `acessos` no banco se não existir
   - Expõe API na porta 5000

### Comunicação Entre Serviços

- **Rede Interna**: Todos os serviços estão na mesma rede bridge
- **Resolução DNS**: Docker resolve nomes dos serviços automaticamente
  - `db` → IP do container PostgreSQL
  - `cache` → IP do container Redis
- **Variáveis de Ambiente**: Configurações passadas via `docker-compose.yml`
- **Portas**: Apenas o serviço web expõe porta externamente (5000)

### Endpoints da API

#### `GET /`
Testa comunicação com todos os serviços e retorna status.

**Resposta:**
```json
{
  "servico": "web",
  "status": "online",
  "timestamp": "2025-11-19T21:30:00",
  "servicos": {
    "database": {
      "status": "conectado",
      "host": "db",
      "port": "5432"
    },
    "cache": {
      "status": "conectado",
      "host": "cache",
      "port": "6379"
    }
  }
}
```

#### `GET /db/test`
Testa operações no banco de dados (inserção e consulta).

**Resposta:**
```json
{
  "status": "sucesso",
  "acesso_id": 1,
  "total_acessos": 1,
  "mensagem": "Dados inseridos e consultados com sucesso"
}
```

#### `GET /cache/test`
Testa operações no cache Redis (incremento e armazenamento).

**Resposta:**
```json
{
  "status": "sucesso",
  "contador": 1,
  "ultimo_acesso": "2025-11-19T21:30:00",
  "mensagem": "Cache funcionando corretamente"
}
```

#### `GET /integracao`
Demonstra integração completa entre web, db e cache.

**Resposta:**
```json
{
  "status": "sucesso",
  "operacoes": [
    {
      "servico": "database",
      "acao": "inserir",
      "status": "sucesso",
      "acesso_id": 2
    },
    {
      "servico": "cache",
      "acao": "incrementar_contador",
      "status": "sucesso",
      "contador": 1
    }
  ]
}
```

## Instruções de Execução

### Pré-requisitos
- Docker instalado
- Docker Compose instalado
- Porta 5000 disponível (ou altere no docker-compose.yml)

### Passo a Passo

#### 1. Navegar para o diretório do desafio
```bash
cd desafio3
```

#### 2. Construir e executar os serviços
```bash
docker compose up --build
```

#### 3. Testar a aplicação

**a) Verificar status geral:**
```bash
curl http://localhost:5000/
```

**b) Testar banco de dados:**
```bash
curl http://localhost:5000/db/test
```

**c) Testar cache:**
```bash
curl http://localhost:5000/cache/test
```

**d) Testar integração completa:**
```bash
curl http://localhost:5000/integracao
```

## Conclusão

Este desafio demonstra com sucesso:
- ✅ Orquestração de múltiplos serviços com Docker Compose
- ✅ Configuração de dependências com `depends_on` e healthchecks
- ✅ Uso de variáveis de ambiente para configuração
- ✅ Comunicação entre serviços via rede interna
- ✅ Persistência de dados com volumes
- ✅ Estrutura organizada e boas práticas

A solução mostra como três serviços independentes (web, db, cache) podem ser orquestrados de forma coordenada, com inicialização ordenada, comunicação eficiente e configuração flexível através do Docker Compose.

