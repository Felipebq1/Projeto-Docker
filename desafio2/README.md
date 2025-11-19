# Desafio 2

## Descrição da Solução

Este desafio demonstra a persistência de dados usando volumes Docker. A solução consiste em dois containers Python que trabalham com um banco de dados SQLite armazenado em um volume nomeado do Docker.

### Arquitetura

```
┌─────────────────┐         ┌─────────────────┐
│  Container      │         │  Container      │
│  ESCRITOR       │         │  LEITOR         │
│                 │         │                 │
│  - Cria BD      │         │  - Lê dados     │
│  - Insere dados │         │  - Valida       │
│  - Finaliza     │         │    persistência │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └───────────┬───────────────┘
                     │
            ┌────────▼────────┐
            │  Volume Docker  │
            │  dados_db       │
            │  /data/         │
            │  desafio2.db    │
            └─────────────────┘
```

### Componentes

1. **Container Escritor** (`escritor/`):
   - Cria o banco de dados SQLite se não existir
   - Insere dados de exemplo (usuários)
   - Demonstra a escrita no volume

2. **Container Leitor** (`leitor/`):
   - Lê os dados do banco persistido
   - Valida que os dados sobreviveram à remoção do container escritor
   - Demonstra a leitura do volume

3. **Volume Docker** (`dados_db`):
   - Volume nomeado que persiste os dados
   - Montado em `/data` em ambos os containers
   - Permanece mesmo após remoção dos containers

### Fluxo de Execução

1. **Container Escritor**:
   - Inicia e monta o volume `dados_db` em `/data`
   - Cria o arquivo `desafio2.db` se não existir
   - Cria a tabela `usuarios` se não existir
   - Insere 3 registros de exemplo
   - Lista os dados inseridos
   - Finaliza (container é removido)

2. **Container Leitor**:
   - Aguarda o escritor terminar (`depends_on`)
   - Monta o mesmo volume `dados_db` em `/data`
   - Verifica se o banco existe
   - Lê e exibe todos os registros
   - Demonstra que os dados persistiram

### Persistência Comprovada

O volume Docker garante que:
- ✅ Dados permanecem após remoção do container escritor
- ✅ Dados são acessíveis por outros containers
- ✅ Dados sobrevivem a `docker compose down`
- ✅ Volume pode ser inspecionado com `docker volume inspect`

## Instruções de Execução

### Pré-requisitos
- Docker instalado
- Docker Compose instalado

### Passo a Passo

#### 1. Navegar para o diretório do desafio
```bash
cd desafio2
```

#### 2. Construir e executar os containers
```bash
docker compose up --build
```

## Explicação do Código

### `escritor/app.py`
- **`criar_banco()`**: Cria tabela `usuarios` com campos id, nome, email, criado_em
- **`inserir_dados()`**: Insere 3 registros de exemplo
- **`listar_dados()`**: Exibe todos os registros para confirmação

### `leitor/app.py`
- **`verificar_banco()`**: Valida existência do arquivo do banco
- **`ler_dados()`**: Consulta e exibe todos os registros, comprovando persistência

### `docker-compose.yml`
- **Volume `dados_db`**: Volume nomeado montado em `/data` em ambos containers
- **`depends_on`**: Garante que escritor execute antes do leitor
- **Rede**: Containers na mesma rede para comunicação (se necessário no futuro)

## Resultados e Comprovação

### Evidências de Persistência

1. **Logs do Leitor**: Mostram que dados foram lidos após remoção do escritor
2. **Volume Docker**: Permanece listado mesmo após `docker compose down`
3. **Reexecução**: Leitor consegue ler dados de execuções anteriores

## Conclusão

Este desafio demonstra com sucesso:
- ✅ Uso correto de volumes Docker nomeados
- ✅ Persistência de dados entre execuções de containers
- ✅ Compartilhamento de dados entre containers diferentes
- ✅ Isolamento e gerenciamento de dados pelo Docker

Os dados do banco SQLite são armazenados no volume `desafio2_volume` e permanecem disponíveis mesmo após a remoção completa dos containers, comprovando a persistência solicitada no desafio.

