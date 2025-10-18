# 🧪 Guia de Testes - YTBridge

## 📋 Testes Rápidos

### 1. Health Check
```bash
curl http://localhost:8000/api/v1/health

# Deve retornar
{
  "status": "ok",
  "cache_type": "redis",
  "cache_available": true
}
```

### 2. Buscar Vídeos
```bash
curl "http://localhost:8000/api/v1/search/?q=Python&max_results=5"
```

### 3. Info de Canal
```bash
curl http://localhost:8000/api/v1/channels/info/@YouTube
```

### 4. Info de Vídeo
```bash
curl http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ
```

### 5. Vídeos de Canal
```bash
curl "http://localhost:8000/api/v1/channels/videos/@YouTube?max_videos=10"
```

### 6. Vídeos Relacionados
```bash
curl http://localhost:8000/api/v1/videos/related/dQw4w9WgXcQ
```

### 7. Info de Playlist
```bash
curl http://localhost:8000/api/v1/playlists/info/PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf
```

---

## 🎯 Teste Automatizado

### Script de Teste Completo

```bash
#!/bin/bash

echo "🧪 Testando YTBridge..."

BASE_URL="http://localhost:8000/api/v1"
PASSED=0
FAILED=0

test_endpoint() {
    local name=$1
    local url=$2
    local expected_code=${3:-200}
    
    echo -n "Testing $name... "
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$response" -eq "$expected_code" ]; then
        echo "✅ PASSED"
        ((PASSED++))
    else
        echo "❌ FAILED (got $response, expected $expected_code)"
        ((FAILED++))
    fi
}

# Executar testes
test_endpoint "Health Check" "$BASE_URL/health"
test_endpoint "Search" "$BASE_URL/search/?q=Python&max_results=5"
test_endpoint "Channel Info" "$BASE_URL/channels/info/@YouTube"
test_endpoint "Video Info" "$BASE_URL/videos/info/dQw4w9WgXcQ"
test_endpoint "Channel Videos" "$BASE_URL/channels/videos/@YouTube?max_videos=5"
test_endpoint "Related Videos" "$BASE_URL/videos/related/dQw4w9WgXcQ"

echo ""
echo "📊 Resultados: $PASSED passed, $FAILED failed"

if [ $FAILED -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
    exit 0
else
    echo "❌ Alguns testes falharam"
    exit 1
fi
```

### Executar

```bash
chmod +x test-api.sh
./test-api.sh
```

---

## ⚡ Teste de Cache

### Verificar Performance

```bash
# Primeira chamada (cache miss - lenta)
time curl http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ

# Segunda chamada (cache hit - rápida)
time curl http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ

# Diferença esperada: 95%+ mais rápido
```

### Verificar Redis

```bash
# Ver keys no Redis
docker-compose exec youtube-api-redis redis-cli KEYS "*"

# Ver estatísticas
docker-compose exec youtube-api-redis redis-cli INFO stats

# Ver hit/miss rate
docker-compose exec youtube-api-redis redis-cli INFO stats | grep keyspace
```

---

## 🔥 Teste de Rate Limiting

### Script de Teste

```bash
#!/bin/bash

echo "Testing rate limit..."

for i in {1..105}; do
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/health)
    echo "Request $i: $response"
    
    if [ "$response" -eq "429" ]; then
        echo "✅ Rate limit working! (blocked at request $i)"
        exit 0
    fi
done

echo "❌ Rate limit not working (expected 429 after 100 requests)"
exit 1
```

---

## 📊 Teste de Carga

### Usando Apache Bench

```bash
# Instalar ab
sudo apt install apache2-utils

# 1000 requisições, 10 concorrentes
ab -n 1000 -c 10 http://localhost:8000/api/v1/health

# Com cache habilitado
ab -n 1000 -c 10 "http://localhost:8000/api/v1/videos/info/dQw4w9WgXcQ"
```

### Usando wrk

```bash
# Instalar wrk
sudo apt install wrk

# Teste por 30 segundos, 10 threads, 100 conexões
wrk -t10 -c100 -d30s http://localhost:8000/api/v1/health
```

---

## 🐍 Testes com Python

### Exemplo Básico

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("✅ Health check passed")

def test_search():
    response = requests.get(f"{BASE_URL}/search/", params={
        "q": "Python tutorial",
        "max_results": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert len(data["data"]["results"]) > 0
    print("✅ Search test passed")

def test_channel():
    response = requests.get(f"{BASE_URL}/channels/info/@YouTube")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "name" in data["data"]
    print("✅ Channel test passed")

def test_video():
    response = requests.get(f"{BASE_URL}/videos/info/dQw4w9WgXcQ")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "title" in data["data"]
    print("✅ Video test passed")

if __name__ == "__main__":
    test_health()
    test_search()
    test_channel()
    test_video()
    print("\n✅ Todos os testes passaram!")
```

### Executar

```bash
python test_api.py
```

---

## 🌐 Testes com JavaScript/Node

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api/v1';

async function testHealth() {
    const response = await axios.get(`${BASE_URL}/health`);
    console.assert(response.status === 200);
    console.assert(response.data.status === 'ok');
    console.log('✅ Health check passed');
}

async function testSearch() {
    const response = await axios.get(`${BASE_URL}/search/`, {
        params: { q: 'JavaScript', max_results: 5 }
    });
    console.assert(response.status === 200);
    console.assert(response.data.success === true);
    console.log('✅ Search test passed');
}

async function runTests() {
    try {
        await testHealth();
        await testSearch();
        console.log('\n✅ Todos os testes passaram!');
    } catch (error) {
        console.error('❌ Teste falhou:', error.message);
    }
}

runTests();
```

---

## 🔍 Validação de Dados

### Testar Validação de Input

```bash
# Busca sem query (deve falhar)
curl "http://localhost:8000/api/v1/search/"
# Esperado: 422 Unprocessable Entity

# Video ID inválido
curl http://localhost:8000/api/v1/videos/info/invalid
# Esperado: 400 ou 404

# Max results muito alto
curl "http://localhost:8000/api/v1/search/?q=Python&max_results=9999"
# Esperado: 422 ou limitado automaticamente
```

---

## 📈 Monitorar Durante Testes

### Terminal 1: Rodar testes
```bash
./test-api.sh
```

### Terminal 2: Monitorar logs
```bash
./manage.sh logs -f
```

### Terminal 3: Monitorar recursos
```bash
docker stats
```

### Terminal 4: Monitorar Redis
```bash
docker-compose exec youtube-api-redis redis-cli MONITOR
```

---

## ✅ Checklist de Testes

### Funcionalidade
- [ ] Health check responde
- [ ] Busca retorna resultados
- [ ] Info de canal funciona
- [ ] Info de vídeo funciona
- [ ] Vídeos de canal funcionam
- [ ] Vídeos relacionados funcionam
- [ ] Info de playlist funciona

### Performance
- [ ] Cache reduz latência (95%+)
- [ ] Redis armazena dados
- [ ] Hit rate > 50% após warmup
- [ ] Resposta < 100ms com cache

### Segurança
- [ ] Rate limiting funciona
- [ ] Validação de input funciona
- [ ] Erros não expõem internals
- [ ] CORS configurado corretamente

### Infraestrutura
- [ ] Containers rodam estáveis
- [ ] Health checks passam
- [ ] Logs sem erros críticos
- [ ] Restart automático funciona

---

## 🐛 Debug de Testes

### Se teste falhar

```bash
# Ver logs detalhados
./manage.sh logs

# Testar manualmente com verbose
curl -v http://localhost:8000/api/v1/health

# Verificar containers
docker-compose ps

# Entrar no container
./manage.sh shell-api

# Testar dentro do container
curl localhost:8000/api/v1/health
```

---

## 📚 Documentação Interativa

Acesse Swagger UI para testar interativamente:

```
http://localhost:8000/api/v1/docs
```

**Recursos:**
- Testar todos os endpoints
- Ver schemas de request/response
- Executar testes direto no navegador
- Ver exemplos de código
