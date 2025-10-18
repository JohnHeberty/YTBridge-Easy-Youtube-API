# 🚀 Guia de Deploy - YTBridge

## ⚡ Início Rápido

```bash
# 1. Dar permissão aos scripts
chmod +x start.sh manage.sh monitor.sh

# 2. Iniciar tudo
./start.sh

# 3. Acessar
http://localhost:8000/api/v1/docs
```

**Pronto!** A API está rodando em 30 segundos.

---

## 📋 Pré-requisitos

### Necessário
- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM livre
- 5GB disco livre

### Instalação Docker (Debian/Ubuntu)

```bash
# Instalar Docker
curl -fsSL https://get.docker.com | bash

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Verificar instalação
docker --version
docker-compose --version
```

---

## 🎯 Comandos Essenciais

### Gerenciamento Básico

```bash
./start.sh          # Iniciar tudo
./manage.sh stop    # Parar serviços
./manage.sh restart # Reiniciar
./manage.sh status  # Ver status
./manage.sh logs    # Ver logs
```

### Monitoramento

```bash
./monitor.sh        # Dashboard em tempo real
./manage.sh test    # Testar endpoints
docker stats        # Recursos (CPU/RAM)
```

### Desenvolvimento

```bash
./manage.sh dev     # Modo dev (hot reload + Redis Commander)
# Redis Commander: http://localhost:8081
```

### Manutenção

```bash
./manage.sh build   # Rebuildar imagens
./manage.sh clean   # Limpar tudo
docker system prune # Limpar Docker
```

---

## 🐳 Modos de Execução

### Produção (Padrão)

```bash
./start.sh
# ou
docker-compose up -d
```

**Características:**
- 4 workers Uvicorn
- Cache Redis persistente
- Rate limiting: 100 req/min
- Restart automático
- Logs otimizados

### Desenvolvimento

```bash
./manage.sh dev
# ou
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

**Características:**
- Hot reload (código atualiza automaticamente)
- Redis Commander (UI: http://localhost:8081)
- Rate limiting relaxado: 1000 req/min
- Logs verbose
- Source code montado como volume

---

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```bash
# Cache
CACHE_TYPE=redis              # memory ou redis
CACHE_TTL=3600               # TTL em segundos

# Redis
REDIS_HOST=redis             # hostname do Redis
REDIS_PORT=6379              # porta
REDIS_DB=0                   # database number

# Rate Limiting
RATE_LIMIT_REQUESTS=100      # máx requisições
RATE_LIMIT_WINDOW=60         # janela em segundos

# API
API_TITLE="YTBridge"
API_VERSION="1.0.0"
WORKERS=4                    # workers Uvicorn
```

### Alterar Configurações

```bash
# Editar .env
nano .env

# Reiniciar para aplicar
./manage.sh restart
```

---

## 🔍 Testando a API

### Health Check

```bash
curl http://localhost:8000/api/v1/health

# Resposta
{
  "status": "ok",
  "cache_type": "redis",
  "cache_available": true,
  "timestamp": "2025-10-18T..."
}
```

### Buscar Vídeos

```bash
curl "http://localhost:8000/api/v1/search/?q=Python&max_results=5"
```

### Info de Canal

```bash
curl http://localhost:8000/api/v1/channels/info/@YouTube
```

### Info de Vídeo

```bash
curl http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ
```

### Testar Cache

```bash
# Primeira chamada (lenta - busca YouTube)
time curl http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ

# Segunda chamada (rápida - cache)
time curl http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ
```

---

## 🔧 Troubleshooting

### Containers não iniciam

```bash
# Ver logs de erro
./manage.sh logs

# Verificar status
docker-compose ps

# Rebuild limpo
./manage.sh clean
./manage.sh build
./start.sh
```

### Porta 8000 ocupada

```bash
# Verificar o que está usando
sudo ss -tulpn | grep 8000

# Matar processo
sudo kill -9 <PID>

# Ou mudar porta no docker-compose.yml
ports:
  - "8001:8000"  # Mudar para 8001
```

### API não responde

```bash
# Verificar health
curl http://localhost:8000/api/v1/health

# Verificar containers
docker-compose ps

# Verificar logs
./manage.sh logs

# Reiniciar
./manage.sh restart
```

### Redis não conecta

```bash
# Testar Redis
docker-compose exec youtube-api-redis redis-cli ping
# Deve retornar: PONG

# Verificar logs Redis
./manage.sh logs-redis

# Restart Redis
docker-compose restart youtube-api-redis
```

### Performance lenta

```bash
# Verificar recursos
docker stats

# Verificar cache
docker-compose exec youtube-api-redis redis-cli INFO stats

# Verificar hit rate
docker-compose exec youtube-api-redis redis-cli INFO stats | grep keyspace

# Limpar cache (se necessário)
docker-compose exec youtube-api-redis redis-cli FLUSHALL
```

---

## 🌐 Acesso Externo (Proxmox/LXC)

### Port Forward (Host Proxmox)

```bash
# No host Proxmox
iptables -t nat -A PREROUTING -p tcp --dport 8000 -j DNAT --to <LXC-IP>:8000
iptables -t nat -A POSTROUTING -s <LXC-IP>/32 -j MASQUERADE

# Salvar regras
iptables-save > /etc/iptables/rules.v4
```

### Firewall (Container)

```bash
# Permitir porta 8000
sudo ufw allow 8000/tcp
sudo ufw enable
sudo ufw status
```

### Reverse Proxy (NGINX)

```nginx
# /etc/nginx/sites-available/youtube-api
server {
    listen 80;
    server_name api.seu-dominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Ativar
sudo ln -s /etc/nginx/sites-available/youtube-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📊 Monitoramento

### Dashboard Real-time

```bash
./monitor.sh
```

**Exibe:**
- Status dos containers
- Uso de CPU/RAM
- Health checks
- Estatísticas Redis (hits/misses)
- Hit rate do cache
- Refresh automático (5s)

### Logs

```bash
# Todos os logs
./manage.sh logs

# Apenas API
./manage.sh logs-api

# Apenas Redis
./manage.sh logs-redis

# Seguir logs em tempo real
./manage.sh logs -f

# Últimas 100 linhas
docker-compose logs --tail=100
```

### Métricas Docker

```bash
# Recursos em tempo real
docker stats

# Espaço em disco
docker system df

# Informações detalhadas
docker inspect youtube-api
```

---

## 💾 Backup e Restore

### Backup Redis

```bash
# Forçar save
docker-compose exec youtube-api-redis redis-cli SAVE

# Copiar dump
docker cp youtube-api-redis:/data/dump.rdb ./backup-redis-$(date +%Y%m%d).rdb
```

### Restore Redis

```bash
# Parar Redis
docker-compose stop youtube-api-redis

# Copiar backup
docker cp ./backup-redis-YYYYMMDD.rdb youtube-api-redis:/data/dump.rdb

# Iniciar Redis
docker-compose start youtube-api-redis
```

### Backup Completo

```bash
# Exportar imagens
docker save -o youtube-api-images.tar $(docker-compose config | grep image: | awk '{print $2}')

# Backup volumes
docker run --rm -v redis_data:/data -v $(pwd):/backup alpine \
  tar czf /backup/redis-data-$(date +%Y%m%d).tar.gz -C /data .

# Backup configuração
tar czf config-$(date +%Y%m%d).tar.gz docker-compose*.yml .env
```

---

## 🚀 Auto-start (Systemd)

### Criar Service

```bash
sudo nano /etc/systemd/system/youtube-api.service
```

```ini
[Unit]
Description=YTBridge Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/caminho/para/youtube-api
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

### Ativar

```bash
sudo systemctl daemon-reload
sudo systemctl enable youtube-api
sudo systemctl start youtube-api
sudo systemctl status youtube-api
```

---

## 📈 Escalabilidade

### Múltiplas Instâncias

```bash
# Escalar para 3 instâncias da API
docker-compose up -d --scale youtube-api=3
```

### Load Balancer (NGINX)

```nginx
upstream youtube_api {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://youtube_api;
    }
}
```

---

## 🔐 Segurança

### Implementado
- ✅ Non-root user em containers
- ✅ Network isolation
- ✅ Rate limiting por IP
- ✅ Input validation (Pydantic)
- ✅ Resource limits (Redis 256MB)
- ✅ Health checks (auto-recovery)

### Recomendado para Produção
- [ ] SSL/HTTPS (Let's Encrypt)
- [ ] Autenticação (JWT)
- [ ] Firewall rules (UFW/iptables)
- [ ] Monitoring (Prometheus/Grafana)
- [ ] Backup automático
- [ ] Log rotation

---

## 📚 Documentação Adicional

- **Arquitetura**: `ARCHITECTURE.md` - Clean Architecture e SOLID
- **Testes**: `TESTING.md` - Como testar todos os endpoints
- **Troubleshooting**: `TROUBLESHOOTING.md` - Resolver problemas comuns
- **API Docs**: http://localhost:8000/api/v1/docs (Swagger UI)

---

## 🎯 Checklist de Deploy

- [ ] Docker instalado e funcionando
- [ ] Portas 8000 e 6379 livres
- [ ] Permissão aos scripts (chmod +x)
- [ ] Executado `./start.sh`
- [ ] API respondendo (curl health)
- [ ] Redis funcionando (redis-cli ping)
- [ ] Cache funcionando (teste duplo)
- [ ] Logs sem erros graves
- [ ] Firewall configurado (se necessário)
- [ ] Backup configurado (se produção)
- [ ] Monitoring ativo (se produção)

---

**Deploy completo em menos de 5 minutos!** 🚀
