# 🔧 Troubleshooting - YouTube API# 🔧 Troubleshooting Guide - YouTube API



## 🚀 Problemas ComunsEste guia ajuda a resolver problemas comuns ao usar a YouTube API.



### ❌ API não responde## 📋 Índice



```bash- [Problemas com Docker](#-problemas-com-docker)

# Verificar containers- [Problemas com API](#-problemas-com-api)

docker-compose ps- [Problemas com Redis](#-problemas-com-redis)

- [Problemas com Rate Limiting](#-problemas-com-rate-limiting)

# Ver logs- [Problemas de Performance](#-problemas-de-performance)

./manage.sh logs- [Problemas de Rede](#-problemas-de-rede)



# Reiniciar---

./manage.sh restart

```## 🐳 Problemas com Docker



**Causas:**### ❌ Erro: "Docker not found" ou "Docker daemon is not running"

- Container parado → `./start.sh`

- URL incorreta → Use `/api/v1/` no path**Sintomas:**

- Porta ocupada → Mudar porta no `docker-compose.yml````

docker : The term 'docker' is not recognized...

---```



### ❌ Erro 422 (Validation Error)**Solução:**

1. Instale o Docker Desktop: https://www.docker.com/products/docker-desktop

```json2. Abra o Docker Desktop e aguarde iniciar

{3. Verifique: `docker --version`

  "detail": [4. Tente novamente: `.\start.ps1`

    {"loc": ["query", "q"], "msg": "field required"}

  ]### ❌ Erro: "port is already allocated"

}

```**Sintomas:**

```

**Solução:** Passar parâmetros obrigatóriosError response from daemon: driver failed programming external connectivity on endpoint...

bind: An attempt was made to access a socket in a way forbidden by its access permissions

```bash```

# ❌ Errado

curl http://localhost:8000/api/v1/search/**Causa:** Portas 8000 ou 6379 já estão em uso



# ✅ Correto**Solução 1: Liberar a porta**

curl "http://localhost:8000/api/v1/search/?q=Python&max_results=5"```powershell

```# Verificar o que está usando a porta 8000

netstat -ano | findstr :8000

---

# Matar o processo (substitua PID)

### ❌ Erro 429 (Rate Limit)taskkill /PID <número_do_processo> /F

```

```json

{"detail": "Too many requests"}**Solução 2: Mudar a porta no docker-compose.yml**

``````yaml

services:

**Solução 1:** Aguardar 60 segundos  youtube-api:

    ports:

**Solução 2:** Aumentar limite (dev)      - "8001:8000"  # Mudou para 8001

```yaml```

# docker-compose.yml

environment:### ❌ Containers ficam "unhealthy"

  RATE_LIMIT_REQUESTS: 1000

```**Sintomas:**

```

---youtube-api-1 is unhealthy

```

### ❌ Erro 500 (Internal Error)

**Diagnóstico:**

```bash```powershell

# Ver stack trace# Verificar status

./manage.sh logs | grep ERRORdocker-compose ps



# Testar YouTube connection# Ver logs de erro

docker-compose exec youtube-api python -c "from infrastructure.ytbpy import search; print(search.search_videos('test', 1))"docker-compose logs youtube-api

```

# Verificar health check

**Causas:**docker inspect nova-pasta-youtube-api-1 | Select-String -Pattern "Health"

- YouTube bloqueou → Aguardar ou usar proxy```

- Redis não conecta → Verificar Redis (ver abaixo)

- Bug no código → Ver logs detalhados**Causas Comuns:**

1. **Dependências não instaladas**: Reconstrua a imagem

---   ```powershell

   docker-compose build --no-cache

## 💾 Problemas com Redis   docker-compose up -d

   ```

### Redis não conecta

2. **Redis não conecta**: Verifique se Redis está rodando

```bash   ```powershell

# Verificar Redis   docker-compose ps youtube-api-redis

docker-compose ps youtube-api-redis   ```



# Testar ping3. **Timeout muito curto**: Aguarde período de start (40s)

docker-compose exec youtube-api-redis redis-cli ping   ```powershell

# Deve retornar: PONG   # Aguarde e verifique novamente

   Start-Sleep -Seconds 50

# Reiniciar Redis   docker-compose ps

./manage.sh restart redis   ```

```

### ❌ Build falha: "pip install error"

**Solução:** Verificar hostname em `docker-compose.yml`

```yaml**Sintomas:**

environment:```

  REDIS_HOST: redis  # Nome do serviçoERROR: Could not install packages due to an EnvironmentError

  REDIS_PORT: 6379```

```

**Solução:**

---```powershell

# Limpar cache do Docker

### Cache não funcionadocker system prune -a



```bash# Rebuild sem cache

# Ver keys no Redisdocker-compose build --no-cache

docker-compose exec youtube-api-redis redis-cli KEYS "*"

# Se ainda falhar, verifique requirements.txt

# Verificar configuraçãocat requirements.txt

docker-compose exec youtube-api env | grep CACHE```

```

---

**Solução:** Habilitar cache Redis

```yaml## 🌐 Problemas com API

environment:

  CACHE_TYPE: redis### ❌ API não responde (404 ou timeout)

  CACHE_TTL: 3600

```**Sintomas:**

- Erro 404 ao acessar endpoints

---- Request timeout

- "Connection refused"

### Redis out of memory

**Diagnóstico:**

```bash```powershell

# Verificar memória# 1. Verificar se container está rodando

docker-compose exec youtube-api-redis redis-cli INFO memorydocker-compose ps



# Limpar cache# 2. Testar health check

docker-compose exec youtube-api-redis redis-cli FLUSHALLcurl http://localhost:8000/api/v1/health

```

# 3. Ver logs de erro

**Solução:** Aumentar maxmemorydocker-compose logs -f youtube-api

```yaml```

# docker-compose.yml

youtube-api-redis:**Soluções:**

  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru

```**Problema 1: URL incorreta**

```powershell

---# ❌ Errado

http://localhost:8000/channels/info

## 🐳 Problemas com Docker

# ✅ Correto

### Port already in usehttp://localhost:8000/api/v1/channels/info

```

```bash

# Linux: Ver quem usa a porta**Problema 2: Container parado**

sudo lsof -i :8000```powershell

docker-compose up -d

# Matar processo```

sudo kill -9 <PID>

**Problema 3: Erro na aplicação**

# Ou mudar porta```powershell

# docker-compose.yml# Ver logs completos

ports:docker-compose logs youtube-api --tail=100

  - "8001:8000"

```# Reiniciar serviço

docker-compose restart youtube-api

---```



### Container unhealthy### ❌ Erro 422: Validation Error



```bash**Sintomas:**

# Ver health check```json

docker inspect youtube-api | grep Health -A 10{

  "detail": [

# Aguardar startup (40s)    {

sleep 50      "loc": ["body", "channel_input"],

docker-compose ps      "msg": "field required",

      "type": "value_error.missing"

# Rebuild se persistir    }

docker-compose build --no-cache  ]

docker-compose up -d}

``````



---**Causa:** Parâmetros obrigatórios faltando ou incorretos



### Build falha**Solução:**



```bash**Para POST** - Envie JSON no body:

# Limpar cache Docker```powershell

docker system prune -a$body = @{

    channel_input = "@PythonBrasil"

# Rebuild} | ConvertTo-Json

docker-compose build --no-cache

```Invoke-RestMethod -Uri "http://localhost:8000/api/v1/channels/info" `

    -Method Post `

---    -Body $body `

    -ContentType "application/json"

## ⚡ Problemas de Performance```



### Requisições lentas**Para GET** - Use query parameters:

```powershell

```bashInvoke-RestMethod "http://localhost:8000/api/v1/channels/info/@PythonBrasil"

# Testar com tempo```

time curl http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ

### ❌ Erro 500: Internal Server Error

# Primeira vez: lento (busca YouTube)

# Segunda vez: rápido (cache)**Sintomas:**

```json

# Verificar cache{

docker-compose exec youtube-api-redis redis-cli KEYS "*"  "success": false,

```  "error": {

    "message": "Internal server error"

**Soluções:**  }

- Habilitar Redis cache (ver acima)}

- Aumentar TTL: `CACHE_TTL: 3600````

- Verificar recursos Docker: 4GB RAM, 4 CPUs

**Diagnóstico:**

---```powershell

# Ver stack trace completo nos logs

### CPU altodocker-compose logs youtube-api | Select-String -Pattern "ERROR"

```

```bash

# Ver consumo**Causas Comuns:**

docker stats

1. **ytbpy module error** (YouTube bloqueou ou mudou estrutura)

# Reduzir workers (docker-compose.yml)   ```powershell

command: uvicorn presentation.main:app --host 0.0.0.0 --port 8000 --workers 2   # Testar diretamente no container

```   docker-compose exec youtube-api python -c "from infrastructure.ytbpy import channel; print(channel.get_channel_info('@youtube'))"

   ```

---

2. **Redis connection error**

## 🌐 Problemas de Rede   ```powershell

   # Verificar conectividade

### CORS error   docker-compose exec youtube-api-redis redis-cli ping

   ```

Edite `src/presentation/main.py`:

```python3. **Environment variables erradas**

app.add_middleware(   ```powershell

    CORSMiddleware,   # Verificar variáveis

    allow_origins=["*"],  # Ou domínio específico   docker-compose exec youtube-api env | Select-String -Pattern "CACHE"

    allow_credentials=True,   ```

    allow_methods=["*"],

    allow_headers=["*"],---

)

```## 💾 Problemas com Redis



---### ❌ Redis não conecta



### Containers não se comunicam**Sintomas:**

```

```bashCould not connect to Redis at redis:6379: Connection refused

# Recriar rede```

docker-compose down

docker-compose up -d**Diagnóstico:**

```powershell

# Testar ping# 1. Verificar se Redis está rodando

docker-compose exec youtube-api ping redisdocker-compose ps youtube-api-redis

```

# 2. Testar ping

---docker-compose exec youtube-api-redis redis-cli ping

# Deve retornar: PONG

## 🛠️ Comandos Úteis

# 3. Verificar rede

### Diagnósticodocker network inspect nova-pasta_youtube-api-network

```

```bash

# Status**Soluções:**

docker-compose ps

**Problema 1: Redis não iniciou**

# Logs em tempo real```powershell

./manage.sh logs -fdocker-compose up -d youtube-api-redis

```

# Logs de erro

./manage.sh logs | grep ERROR**Problema 2: Hostname incorreto**

Verifique `.env` ou `docker-compose.yml`:

# Health check```yaml

curl http://localhost:8000/api/v1/healthREDIS_HOST=redis  # Deve ser "redis" (nome do serviço)

REDIS_PORT=6379

# Redis CLI```

docker-compose exec youtube-api-redis redis-cli

**Problema 3: API iniciou antes do Redis**

# Shell no container```powershell

./manage.sh shell-api# Restart respeitando dependências

docker-compose down

# Estatísticasdocker-compose up -d

docker stats```

```

### ❌ Cache não funciona

---

**Sintomas:**

### Reset Completo- Todas as requisições são lentas

- Redis não mostra keys

```bash

# Parar tudo**Diagnóstico:**

docker-compose down -v```powershell

# 1. Verificar configuração de cache

# Limpar sistemadocker-compose exec youtube-api env | Select-String "CACHE"

docker system prune -a --volumes

# 2. Verificar keys no Redis

# Rebuilddocker-compose exec youtube-api-redis redis-cli KEYS "*"

docker-compose build --no-cache

# 3. Monitorar operações Redis

# Iniciardocker-compose exec youtube-api-redis redis-cli MONITOR

./start.sh```



# Aguardar**Soluções:**

sleep 60

docker-compose ps**Problema 1: Cache desabilitado**

```No `docker-compose.yml`:

```yaml

---environment:

  CACHE_TYPE: redis  # Não pode ser "memory" ou "none"

## 📊 Monitoramento```



### Dashboard em tempo real**Problema 2: TTL muito curto**

```yaml

```bashCACHE_TTL: 3600  # 1 hora em segundos

./monitor.sh```

```

**Problema 3: Redis sem memória**

**Mostra:**```powershell

- Status dos containers# Verificar uso de memória

- Logs recentesdocker-compose exec youtube-api-redis redis-cli INFO memory

- Estatísticas de uso

- Health checks# Limpar cache

- Redis infodocker-compose exec youtube-api-redis redis-cli FLUSHALL

```

---

### ❌ Redis out of memory

### Verificar saúde do sistema

**Sintomas:**

```bash```

# APIOOM command not allowed when used memory > 'maxmemory'

curl http://localhost:8000/api/v1/health```



# Redis**Solução:**

docker-compose exec youtube-api-redis redis-cli pingNo `docker-compose.yml`:

```yaml

# Dockeryoutube-api-redis:

docker-compose ps  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru

```

# Recursos

docker stats --no-stream```powershell

```# Restart Redis com nova configuração

docker-compose restart youtube-api-redis

---```



## ✅ Checklist de Troubleshooting---



Antes de procurar ajuda:## ⏱️ Problemas com Rate Limiting



- [ ] Docker está rodando?### ❌ Erro 429: Too Many Requests

- [ ] Portas 8000/6379 livres?

- [ ] Containers "healthy"? (`docker-compose ps`)**Sintomas:**

- [ ] Logs sem erros? (`./manage.sh logs`)```json

- [ ] Health check OK? (`curl localhost:8000/api/v1/health`){

- [ ] Redis responde? (`docker-compose exec youtube-api-redis redis-cli ping`)  "detail": "Too many requests. Try again later."

- [ ] Tentou reiniciar? (`./manage.sh restart`)}

- [ ] Tentou rebuild? (`docker-compose build --no-cache`)```



---**Headers da Resposta:**

```

## 🔍 Debug AvançadoX-RateLimit-Limit: 100

X-RateLimit-Remaining: 0

### Entrar no containerX-RateLimit-Reset: 60

```

```bash

./manage.sh shell-api**Solução 1: Aguardar reset**

```powershell

# Dentro do container# Esperar tempo indicado em X-RateLimit-Reset (em segundos)

python -c "from infrastructure.ytbpy import search; print(search.search_videos('test', 1))"Start-Sleep -Seconds 60

curl localhost:8000/api/v1/health```

env | grep CACHE

```**Solução 2: Aumentar limite (desenvolvimento)**

No `docker-compose.yml`:

---```yaml

environment:

### Monitorar Redis  RATE_LIMIT_REQUESTS: 1000  # Aumentar limite

  RATE_LIMIT_WINDOW: 60      # Janela em segundos

```bash```

# Ver todas as operações

docker-compose exec youtube-api-redis redis-cli MONITOR```powershell

docker-compose restart youtube-api

# Ver estatísticas```

docker-compose exec youtube-api-redis redis-cli INFO

**Solução 3: Usar modo desenvolvimento**

# Ver keys```powershell

docker-compose exec youtube-api-redis redis-cli KEYS "*"# Dev mode tem rate limit mais alto

```.\docker.ps1 dev

```

---

### ❌ Rate limit muito restritivo em produção

### Verificar configuração

**Sintomas:**

```bash- Aplicação legítima sendo bloqueada

# Ver config final do Docker Compose- Múltiplos usuários afetados

docker-compose config

**Solução: Configurar rate limit por usuário (não por IP)**

# Ver variáveis de ambiente

docker-compose exec youtube-api envEdite `src/presentation/api/middleware/rate_limit.py`:

```python

# Ver processos# Usar header de autenticação em vez de IP

docker-compose exec youtube-api ps auxuser_id = request.headers.get("X-User-ID", request.client.host)

``````



---Ou desabilite temporariamente em `src/presentation/main.py`:

```python

## 📞 Coletar Informações# Comentar esta linha

# app.add_middleware(RateLimitMiddleware, max_requests=100, window=60)

Se precisar reportar erro:```



```bash---

# 1. Salvar logs

./manage.sh logs > logs.txt## 🐌 Problemas de Performance



# 2. Status dos containers### ❌ Requisições muito lentas (> 5 segundos)

docker-compose ps > status.txt

**Diagnóstico:**

# 3. Health check```powershell

curl http://localhost:8000/api/v1/health > health.json# 1. Testar com curl e medir tempo

Measure-Command {

# 4. Versões    Invoke-RestMethod "http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ"

docker --version > versions.txt}

docker-compose --version >> versions.txt

python --version >> versions.txt# 2. Verificar se é cache miss

docker-compose exec youtube-api-redis redis-cli KEYS "*"

# 5. Enviar: logs.txt, status.txt, health.json, versions.txt

```# 3. Monitorar recursos

docker stats

---```



## 📚 Ver Também**Causas Comuns:**



- **DEPLOY.md** - Guia de instalação e comandos**Problema 1: Sem cache (primeira requisição)**

- **TESTING.md** - Como testar a API- **Normal**: Primeira requisição é lenta (busca no YouTube)

- **ARCHITECTURE.md** - Estrutura e design patterns- **Solução**: Requisições subsequentes serão rápidas (cache)


**Problema 2: Cache desabilitado**
```yaml
# Habilitar Redis cache
CACHE_TYPE: redis
```

**Problema 3: YouTube está lento**
```powershell
# Testar diretamente no YouTube
curl https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Problema 4: Recursos insuficientes**
```yaml
# Aumentar recursos no Docker Desktop
# Settings > Resources > Advanced
# CPU: 4 cores
# Memory: 4GB
```

### ❌ Alta latência no Redis

**Sintomas:**
```
Redis response time > 100ms
```

**Diagnóstico:**
```powershell
# Medir latência do Redis
docker-compose exec youtube-api-redis redis-cli --latency-history
```

**Soluções:**

1. **Persistir Redis em memória** (docker-compose.yml):
```yaml
youtube-api-redis:
  volumes:
    - /dev/shm/redis:/data  # Usar memória compartilhada
```

2. **Desabilitar persistência** (dev only):
```yaml
command: redis-server --save "" --appendonly no
```

3. **Otimizar TTL**:
```yaml
CACHE_TTL: 1800  # 30 minutos (menos writes)
```

### ❌ CPU alto (>80%)

**Diagnóstico:**
```powershell
# Verificar qual container consome mais
docker stats

# Ver processos dentro do container
docker-compose exec youtube-api top
```

**Soluções:**

1. **Reduzir workers Uvicorn** (docker-compose.yml):
```yaml
command: uvicorn presentation.main:app --host 0.0.0.0 --port 8000 --workers 2
```

2. **Limitar CPU no Docker**:
```yaml
youtube-api:
  deploy:
    resources:
      limits:
        cpus: '2.0'
```

3. **Verificar loop infinito nos logs**:
```powershell
docker-compose logs youtube-api | Select-String -Pattern "ERROR"
```

---

## 🌐 Problemas de Rede

### ❌ Containers não se comunicam

**Sintomas:**
```
youtube-api cannot resolve 'redis'
```

**Diagnóstico:**
```powershell
# Verificar rede
docker network ls
docker network inspect nova-pasta_youtube-api-network

# Testar ping entre containers
docker-compose exec youtube-api ping redis
```

**Solução:**
```powershell
# Recriar rede
docker-compose down
docker-compose up -d
```

### ❌ CORS error no browser

**Sintomas:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://example.com' 
has been blocked by CORS policy
```

**Solução:**
Edite `src/presentation/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://example.com"],  # Seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Ou permita todos (dev only):
```python
allow_origins=["*"]
```

### ❌ Cannot connect from host to container

**Sintomas:**
```
Invoke-RestMethod : Unable to connect to the remote server
```

**Diagnóstico:**
```powershell
# 1. Verificar se porta está aberta
netstat -an | findstr :8000

# 2. Testar localhost
curl http://localhost:8000/api/v1/health

# 3. Verificar firewall
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Docker*"}
```

**Soluções:**

1. **Usar 127.0.0.1 em vez de localhost**:
```powershell
curl http://127.0.0.1:8000/api/v1/health
```

2. **Adicionar exceção no firewall**:
```powershell
New-NetFirewallRule -DisplayName "Docker API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

3. **Verificar binding no container**:
```yaml
command: uvicorn presentation.main:app --host 0.0.0.0 --port 8000
```

---

## 🛠️ Ferramentas de Diagnóstico

### Monitor Dashboard

Use o script de monitoramento:
```powershell
.\monitor.ps1 dashboard  # Dashboard em tempo real
.\monitor.ps1 test       # Testar API
.\monitor.ps1 stats      # Estatísticas
```

### Comandos Úteis

```powershell
# Status geral
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Inspecionar container
docker inspect nova-pasta-youtube-api-1

# Shell dentro do container
docker-compose exec youtube-api bash

# Redis CLI
docker-compose exec youtube-api-redis redis-cli

# Verificar configuração final
docker-compose config

# Recursos em tempo real
docker stats

# Verificar health
curl http://localhost:8000/api/v1/health
```

### Reset Completo

Se nada funcionar, reset total:
```powershell
# 1. Parar tudo
docker-compose down -v

# 2. Limpar imagens e volumes
docker system prune -a --volumes

# 3. Rebuild do zero
docker-compose build --no-cache

# 4. Iniciar novamente
docker-compose up -d

# 5. Aguardar health checks
Start-Sleep -Seconds 60
docker-compose ps
```

---

## 📞 Suporte

Se ainda tiver problemas:

1. **Verificar logs completos**:
```powershell
docker-compose logs > logs.txt
```

2. **Coletar informações do sistema**:
```powershell
docker --version
docker-compose --version
$PSVersionTable
```

3. **Testar configuração mínima**:
```powershell
docker run hello-world
```

4. **Consultar documentação**:
- [README-DOCKER.md](README-DOCKER.md)
- [TESTING.md](TESTING.md)
- [ARCHITECTURE-DOCKER.md](ARCHITECTURE-DOCKER.md)

---

## 🔍 Checklist de Troubleshooting

Antes de procurar ajuda, verifique:

- [ ] Docker Desktop está rodando?
- [ ] Portas 8000 e 6379 estão livres?
- [ ] `.env` está configurado corretamente?
- [ ] Containers estão "healthy"? (`docker-compose ps`)
- [ ] Logs não mostram erros? (`docker-compose logs`)
- [ ] Health check funciona? (`curl localhost:8000/api/v1/health`)
- [ ] Redis responde? (`docker-compose exec youtube-api-redis redis-cli ping`)
- [ ] Testou com dados de exemplo? (vídeo "dQw4w9WgXcQ")
- [ ] Tentou rebuild? (`docker-compose build --no-cache`)
- [ ] Tentou reset completo? (`docker-compose down -v`)

Se todos os itens acima estão OK e o problema persiste, documente:
1. Comando executado
2. Erro completo (screenshot)
3. Logs relevantes
4. Sistema operacional e versões
