# 📚 Documentação - YouTube API

Documentação completa do projeto com foco em SOLID, Clean Architecture e práticas diretas.

---

## 📋 Documentos Disponíveis

### 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md)
**Clean Architecture + SOLID + Docker**

- 4 camadas (Domain, Application, Infrastructure, Presentation)
- 5 princípios SOLID com exemplos práticos
- Padrões: Repository, Factory, Dependency Injection
- Arquitetura Docker e escalabilidade
- Testabilidade e manutenibilidade

### 🚀 [DEPLOY.md](DEPLOY.md)
**Guia prático de deployment**

- Início rápido em 30 segundos
- Comandos essenciais (start/stop/monitor)
- Configuração e variáveis de ambiente
- Setup Proxmox/Linux
- Backup, monitoramento, auto-start

### 🧪 [TESTING.md](TESTING.md)
**Testes e validação**

- Testes de endpoint (curl + scripts)
- Verificação de cache Redis
- Testes de performance e carga
- Rate limiting validation
- Exemplos Python/JavaScript

### 🔧 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
**Solução de problemas**

- Erros comuns (API, Docker, Redis)
- Diagnóstico rápido
- Comandos úteis
- Reset e rebuild
- Checklist de debug

---

## 🎯 Começar Rápido

### Novo no projeto?
1. [README principal](../README.md) - Visão geral
2. [DEPLOY.md](DEPLOY.md) - Subir em 30 segundos
3. Swagger UI - `http://localhost:8000/api/v1/docs`

### Entender arquitetura?
1. [ARCHITECTURE.md](ARCHITECTURE.md) - Clean Architecture + SOLID
2. Explore o código em `src/`

### Fazer deploy?
1. [DEPLOY.md](DEPLOY.md) - Instalação e comandos
2. Configure variáveis de ambiente
3. Use scripts bash (start.sh, manage.sh, monitor.sh)

### Problema?
1. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Soluções rápidas
2. Execute diagnóstico: `./manage.sh logs`

### Testar?
1. [TESTING.md](TESTING.md) - Exemplos práticos
2. Execute: `./manage.sh test`

---

## 📖 Documentação Interativa

API rodando:

- **Swagger UI** - `http://localhost:8000/api/v1/docs`
- **ReDoc** - `http://localhost:8000/api/v1/redoc`
- **OpenAPI JSON** - `http://localhost:8000/openapi.json`

---

## 🔍 Referência Rápida

### Comandos
```bash
./start.sh              # Iniciar
./manage.sh logs        # Logs
./manage.sh test        # Testar
./monitor.sh            # Dashboard
```

### Endpoints
```bash
/api/v1/health                    # Status
/api/v1/search/?q=Python          # Buscar
/api/v1/videos/info/{id}          # Vídeo
/api/v1/channels/info/{channel}   # Canal
```

### Variáveis
```bash
CACHE_TYPE=redis          # Cache
REDIS_HOST=redis          # Host
RATE_LIMIT_REQUESTS=100   # Limite
```

---

## 📝 Padrão da Documentação

- ✅ Explicações diretas (sem redundância)
- ✅ Exemplos práticos
- ✅ Foco em SOLID
- ✅ Comandos funcionais
- ✅ Checklist de validação

---

**Atualizado**: Dezembro 2024
