# � YTBridge

> The bridge between YouTube data and your applications

**YTBridge** connects your applications to YouTube's vast content library through a clean, fast, and reliable REST API. Extract video metadata, channel info, playlists, and search results with enterprise-grade caching and performance.

Built with **Clean Architecture**, **SOLID principles**, and **production-ready infrastructure**.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 🚀 **Deploy in 30 seconds on Proxmox/Linux**: See [SETUP-PROXMOX.md](SETUP-PROXMOX.md)

## 📋 Índice

- [Características](#-características)
- [Arquitetura](#-arquitetura)
- [Endpoints Disponíveis](#-endpoints-disponíveis)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [Documentação](#-documentação)
- [Exemplos](#-exemplos)

## ✨ Features

- 🌉 **Universal Bridge**: One API for all YouTube data needs
- ⚡ **Lightning Fast**: Redis caching with 95%+ hit rate
- �️ **Clean Architecture**: 4 layers, fully testable, SOLID compliant
- � **Production Ready**: Rate limiting, health checks, graceful shutdown
- � **Deploy in 30s**: Docker Compose + bash scripts
- � **Interactive Docs**: Swagger UI + ReDoc
- 🔍 **Observable**: Structured logs, Redis metrics, monitoring dashboard

### What You Can Do
- 📺 **Channel Data**: Complete metadata, statistics, and recent videos
- 🎬 **Video Info**: Details, views, likes, duration, and formats
- 📋 **Playlists**: Information and complete video lists
- � **Search**: Advanced YouTube video search
- � **Related Videos**: Discover similar content

## 🏗️ Architecture

YTBridge follows **Clean Architecture** with clear separation of concerns:

```
ytbridge/
├── 📁 src/                  # Source code (Clean Architecture)
│   ├── domain/              # Business rules and entities
│   ├── application/         # Use cases
│   ├── infrastructure/      # Technical implementations
│   └── presentation/        # User interface (FastAPI)
│
├── 📁 docs/                 # Documentação completa
│   ├── ARCHITECTURE.md      # Detalhes da arquitetura
│   ├── QUICK-START.md       # Guia de início rápido
│   ├── TESTING.md           # Guia de testes
│   └── TROUBLESHOOTING.md   # Solução de problemas
│
├── 📁 tests/                # Testes automatizados
│   ├── unit/                # Testes unitários
│   ├── integration/         # Testes de integração
│   └── e2e/                 # Testes end-to-end
│
├── 🐳 Docker files
│   ├── Dockerfile           # Imagem da API
│   ├── docker-compose.yml   # Orquestração (prod)
│   └── docker-compose.dev.yml # Desenvolvimento
│
├── 🔧 Scripts
│   ├── start.sh             # Início rápido
│   ├── manage.sh            # Gerenciamento
│   └── monitor.sh           # Monitoramento
│
└── ⚙️  Configuração
    ├── requirements.txt     # Dependências Python
    ├── .env.example         # Variáveis de ambiente
    └── .gitignore
```

**Detalhes da arquitetura em camadas:**
- **Domain**: Entidades e interfaces (contratos)
- **Application**: Use cases e DTOs
- **Infrastructure**: Repositórios, cache, configurações
- **Presentation**: Rotas FastAPI, middleware

### Princípios SOLID Aplicados

- ✅ **S**ingle Responsibility: Cada classe tem uma única responsabilidade
- ✅ **O**pen/Closed: Aberto para extensão, fechado para modificação
- ✅ **L**iskov Substitution: Abstrações podem ser substituídas
- ✅ **I**nterface Segregation: Interfaces específicas e enxutas
- ✅ **D**ependency Inversion: Dependa de abstrações, não de implementações

## 🎯 Endpoints Disponíveis

### Canais
- `POST /api/v1/channels/info` - Informações completas do canal
- `GET /api/v1/channels/info/{channel_input}` - Informações do canal (GET)
- `POST /api/v1/channels/videos` - Vídeos do canal
- `GET /api/v1/channels/videos/{channel_input}` - Vídeos do canal (GET)

### Vídeos
- `POST /api/v1/videos/info` - Informações detalhadas do vídeo
- `GET /api/v1/videos/info/{video_id}` - Informações do vídeo (GET)
- `POST /api/v1/videos/related` - Vídeos relacionados
- `GET /api/v1/videos/related/{video_id}` - Vídeos relacionados (GET)

### Playlists
- `POST /api/v1/playlists/info` - Informações da playlist
- `GET /api/v1/playlists/info/{playlist_id}` - Informações da playlist (GET)

### Busca
- `POST /api/v1/search/` - Buscar vídeos
- `GET /api/v1/search/?q=query` - Buscar vídeos (GET)

### Utilitários
- `GET /api/v1/health` - Status da API

## 🚀 Instalação

### 🐳 **Docker (Recomendado)**

**Pré-requisitos**: Docker e Docker Compose

#### Quick Start:

```bash
# Dar permissão aos scripts
chmod +x start.sh manage.sh monitor.sh

# Iniciar tudo com um comando
./start.sh
```

Isso vai:
- ✅ Construir as imagens Docker
- ✅ Iniciar API + Redis automaticamente
- ✅ Aguardar health checks
- ✅ Mostrar status dos serviços

**Acessar:**
- API: http://localhost:8000
- Docs: http://localhost:8000/api/v1/docs
- Redis: localhost:6379

**Comandos úteis:**
```bash
./manage.sh logs     # Ver logs
./manage.sh stop     # Parar tudo
./manage.sh restart  # Reiniciar
./manage.sh test     # Testar API
./manage.sh dev      # Modo desenvolvimento (hot reload)
./monitor.sh         # Dashboard de monitoramento
```

📚 **[Documentação Completa](docs/)** - Guias detalhados

---

### 🐍 **Instalação Manual (Alternativa)**

**Pré-requisitos**: Python 3.8+ e pip

1. **Crie um ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure variáveis de ambiente (opcional):**
```bash
cp .env.example .env
# Edite .env conforme necessário
```

4. **Execute a API:**
```bash
uvicorn src.presentation.main:app --reload --host 0.0.0.0 --port 8000
```

5. **Acesse:**
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 💻 Uso

### Exemplo com Python Requests

```python
import requests

# Buscar vídeos
response = requests.get(
    "http://localhost:8000/api/v1/search/",
    params={"q": "Python tutorial", "max_results": 10}
)
print(response.json())

# Informações de canal
response = requests.get(
    "http://localhost:8000/api/v1/channels/info/@PythonBrasil",
    params={"include_videos": True, "max_videos": 5}
)
print(response.json())

# Informações de vídeo
response = requests.get(
    "http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ"
)
print(response.json())
```

### Exemplo com cURL

```bash
# Buscar vídeos
curl "http://localhost:8000/api/v1/search/?q=Python&max_results=5"

# Informações de canal
curl "http://localhost:8000/api/v1/channels/info/@PythonBrasil"

# Informações de vídeo
curl "http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ"
```

### Exemplo com JavaScript/Fetch

```javascript
// Buscar vídeos
fetch('http://localhost:8000/api/v1/search/?q=JavaScript&max_results=10')
  .then(response => response.json())
  .then(data => console.log(data));

// Informações de canal
fetch('http://localhost:8000/api/v1/channels/info/@javascript')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 📚 Documentação

### Guias Disponíveis

- 📖 **[SETUP-PROXMOX.md](SETUP-PROXMOX.md)** - Deploy em Proxmox/Linux
- 📖 **[PROJECT-STRUCTURE.md](PROJECT-STRUCTURE.md)** - Estrutura do projeto
- 📂 **[docs/](docs/)** - Documentação completa
  - [QUICK-START.md](docs/QUICK-START.md) - Início rápido
  - [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Clean Architecture
  - [TESTING.md](docs/TESTING.md) - Guia de testes
  - [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Solução de problemas
  - [README-DOCKER.md](docs/README-DOCKER.md) - Guia Docker completo

### Scripts Úteis

```bash
./start.sh              # Iniciar API + Redis
./manage.sh logs        # Ver logs
./manage.sh test        # Testar API
./manage.sh restart     # Reiniciar serviços
./monitor.sh            # Dashboard em tempo real
```

## ⚙️ Configuração

Todas as configurações podem ser definidas via variáveis de ambiente (arquivo `.env`):

### Cache
```env
CACHE_ENABLED=True          # Habilitar cache
CACHE_TYPE=memory           # Tipo: memory ou redis
CACHE_TTL=3600             # TTL em segundos (1 hora)
CACHE_MAX_SIZE=1000        # Tamanho máximo do cache em memória
```

### Redis (se CACHE_TYPE=redis)
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_password
```

### Rate Limiting
```env
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100    # Máximo de requisições
RATE_LIMIT_PERIOD=60       # Por período (segundos)
```

### Servidor
```env
HOST=0.0.0.0
PORT=8000
WORKERS=4                  # Número de workers (produção)
DEBUG=False                # Modo debug
```

## 📝 Exemplos

### Buscar Vídeos sobre Dota 2

```bash
curl "http://localhost:8000/api/v1/search/?q=Dota+2+gameplay&max_results=20"
```

### Obter Informações de Canal com Vídeos

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/channels/info",
    json={
        "channel_input": "@Dota2OldSchoolShow",
        "include_videos": True,
        "max_videos": 50
    }
)

data = response.json()
if data["success"]:
    channel = data["data"]
    print(f"Canal: {channel['title']}")
    print(f"Inscritos: {channel.get('subscriber_count_text', 'N/A')}")
    print(f"Total de vídeos: {channel.get('videos_count', 0)}")
```

### Obter Playlist Completa

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/playlists/info/PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf",
    params={"max_results": 100}
)

data = response.json()
if data["success"]:
    playlist = data["data"]
    print(f"Playlist: {playlist['title']}")
    print(f"Total de vídeos: {playlist.get('videos_count', 0)}")
    for video in playlist.get("videos", []):
        print(f"- {video['title']}")
```

## 💾 Cache

O sistema de cache reduz drasticamente a carga no YouTube e melhora a performance:

- **Cache em Memória**: Rápido, ideal para desenvolvimento e servidores single-instance
- **Cache Redis**: Escalável, ideal para produção com múltiplas instâncias

### Como funciona:
1. Primeira requisição → busca dados do YouTube → armazena no cache
2. Requisições subsequentes → retorna do cache (muito mais rápido)
3. Após TTL expirar → busca novamente do YouTube

### Chave de cache:
Gerada automaticamente com base nos parâmetros da requisição.

## 🛡️ Rate Limiting

Protege a API contra abuso:

- **Limite padrão**: 100 requisições por minuto por IP
- **Headers de resposta**:
  - `X-RateLimit-Limit`: Limite total
  - `X-RateLimit-Remaining`: Requisições restantes
  - `X-RateLimit-Reset`: Timestamp do reset

Quando o limite é excedido, retorna erro 429 (Too Many Requests).

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar testes
pytest tests/
```

## 📦 Deploy em Produção

### Com Docker (recomendado)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.presentation.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```bash
docker build -t youtube-api .
docker run -p 8000:8000 --env-file .env youtube-api
```

### Com Uvicorn (produção)

```bash
uvicorn src.presentation.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Com Gunicorn + Uvicorn Workers

```bash
gunicorn src.presentation.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ seguindo as melhores práticas de arquitetura de software.

## 🙏 Agradecimentos

- Módulo ytbpy para extração de dados do YouTube
- FastAPI pelo excelente framework
- Comunidade Python

---

**Nota**: Esta API não está afiliada ao YouTube ou Google. Use de forma responsável respeitando os Termos de Serviço do YouTube.
