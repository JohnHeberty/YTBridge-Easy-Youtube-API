# 🏗️ Arquitetura - YouTube API

## Visão Geral

Este projeto implementa **Clean Architecture** com princípios **SOLID**, garantindo código manutenível, testável e escalável.

---

## 🎯 Clean Architecture (4 Camadas)

```
┌─────────────────────────────────────────────────────┐
│                  PRESENTATION                        │
│  FastAPI, Routes, Middleware, Schemas               │
│  • Recebe requisições HTTP                          │
│  • Valida entrada (Pydantic)                        │
│  • Retorna respostas JSON                           │
└─────────────────┬───────────────────────────────────┘
                  │ Chama
                  ▼
┌─────────────────────────────────────────────────────┐
│                  APPLICATION                         │
│  Use Cases, DTOs                                    │
│  • Orquestra lógica de negócio                     │
│  • Coordena entre camadas                          │
│  • Independente de frameworks                      │
└─────────────────┬───────────────────────────────────┘
                  │ Usa
                  ▼
┌─────────────────────────────────────────────────────┐
│                 INFRASTRUCTURE                       │
│  Repositories, Cache, Config, ytbpy                │
│  • Implementa interfaces do domain                 │
│  • Acessa recursos externos (Redis, YouTube)       │
│  • Detalhes técnicos de implementação              │
└─────────────────┬───────────────────────────────────┘
                  │ Implementa
                  ▼
┌─────────────────────────────────────────────────────┐
│                    DOMAIN                            │
│  Entities, Interfaces (Repositories)                │
│  • Regras de negócio puras                         │
│  • Independente de tudo                            │
│  • Apenas Python puro                              │
└─────────────────────────────────────────────────────┘
```

### Fluxo de Requisição

```
HTTP Request
    ↓
[Middleware: Rate Limit]
    ↓
[Middleware: Error Handler]
    ↓
[Route Handler]
    ↓
[Use Case] ← Injeta Repository
    ↓
[Repository] → Cache? → YouTube API
    ↓
[Entity (Domain)]
    ↓
[Response Schema]
    ↓
HTTP Response (JSON)
```

---

## 🔵 Princípios SOLID

### 1. **S**ingle Responsibility Principle

**"Uma classe deve ter apenas uma razão para mudar"**

```python
# ✅ BOM: Cada use case faz UMA coisa
class GetChannelInfoUseCase:
    def execute(self, channel_input: str) -> Channel:
        return self.repository.get_channel_info(channel_input)

class GetChannelVideosUseCase:
    def execute(self, channel_input: str) -> List[Video]:
        return self.repository.get_channel_videos(channel_input)

# ❌ RUIM: Use case fazendo múltiplas coisas
class ChannelUseCase:
    def get_info_and_videos_and_stats(...):  # Muitas responsabilidades!
        pass
```

**No projeto:**
- `GetChannelInfoUseCase` → Apenas buscar info do canal
- `GetChannelVideosUseCase` → Apenas buscar vídeos
- `SearchYouTubeUseCase` → Apenas fazer buscas
- `MemoryCache` → Apenas cache em memória
- `RedisCache` → Apenas cache no Redis

---

### 2. **O**pen/Closed Principle

**"Aberto para extensão, fechado para modificação"**

```python
# ✅ BOM: Interface estável, fácil adicionar novos tipos
class ICache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int):
        pass

# Adicionar novo tipo SEM modificar código existente
class MemcachedCache(ICache):  # Nova implementação
    async def get(self, key: str):
        return await self.memcached_client.get(key)
    
    async def set(self, key: str, value: Any, ttl: int):
        await self.memcached_client.set(key, value, ttl)
```

**No projeto:**
- Adicionar novo tipo de cache? Implemente `ICache`
- Adicionar nova fonte de dados? Implemente `IYouTubeRepository`
- Adicionar novo endpoint? Crie nova rota

---

### 3. **L**iskov Substitution Principle

**"Subtipos devem ser substituíveis por seus tipos base"**

```python
# ✅ BOM: Qualquer ICache pode ser usado
repository = YTBPyRepository(cache=MemoryCache())  # Funciona
repository = YTBPyRepository(cache=RedisCache())   # Também funciona

# O repository não sabe (nem precisa saber) qual cache está usando
# Ambos implementam a mesma interface ICache
```

**No projeto:**
- `MemoryCache` e `RedisCache` são intercambiáveis
- Use cases não sabem qual repository está sendo usado
- Routes não sabem qual use case implementation está rodando

---

### 4. **I**nterface Segregation Principle

**"Clientes não devem depender de interfaces que não usam"**

```python
# ✅ BOM: Interface enxuta com apenas o necessário
class IYouTubeRepository(ABC):
    @abstractmethod
    async def get_channel_info(self, channel_input: str) -> Channel:
        pass
    
    @abstractmethod
    async def get_video_info(self, video_id: str) -> Video:
        pass
    # ... apenas métodos realmente usados

# ❌ RUIM: Interface inchada
class IMegaRepository(ABC):
    async def get_channel_info(...): pass
    async def get_video_info(...): pass
    async def send_email(...): pass  # ❌ Não tem nada a ver!
    async def log_to_database(...): pass  # ❌ Outra responsabilidade
    async def upload_file(...): pass  # ❌ Misturando conceitos
```

**No projeto:**
- `ICache` → Apenas get/set
- `IYouTubeRepository` → Apenas métodos de YouTube
- Use cases → Apenas execute()

---

### 5. **D**ependency Inversion Principle

**"Dependa de abstrações, não de implementações"**

```python
# ✅ BOM: Use case depende da INTERFACE
class GetChannelInfoUseCase:
    def __init__(self, repository: IYouTubeRepository):  # ← Interface
        self.repository = repository
    
    async def execute(self, channel_input: str) -> Channel:
        return await self.repository.get_channel_info(channel_input)

# ❌ RUIM: Use case dependendo de implementação concreta
class GetChannelInfoUseCase:
    def __init__(self, repository: YTBPyRepository):  # ← Implementação
        self.repository = repository
```

**No projeto:**
```python
# Injeção de dependências em presentation/api/dependencies.py
def get_channel_info_use_case() -> GetChannelInfoUseCase:
    cache = cache_factory.create_cache()
    repository = YTBPyRepository(cache=cache)
    return GetChannelInfoUseCase(repository=repository)  # Injeta interface

# Routes recebem use cases via Depends()
@router.post("/info")
async def channel_info(
    use_case: GetChannelInfoUseCase = Depends(get_channel_info_use_case)
):
    result = await use_case.execute(request.channel_input)
```

---

## 📐 Padrões de Design

### Repository Pattern
```python
# Interface define o contrato
class IYouTubeRepository(ABC):
    @abstractmethod
    async def get_channel_info(self, channel_input: str) -> Channel:
        pass

# Implementação concreta
class YTBPyRepository(IYouTubeRepository):
    async def get_channel_info(self, channel_input: str) -> Channel:
        data = await self._get_cached_or_fetch(...)
        return Channel(**data)
```

### Factory Pattern
```python
class CacheFactory:
    @staticmethod
    def create_cache() -> ICache:
        if settings.CACHE_TYPE == "redis":
            return RedisCache()
        else:
            return MemoryCache()
```

### Dependency Injection
```python
@router.post("/search/")
async def search(
    request: SearchRequest,
    use_case: SearchYouTubeUseCase = Depends(get_search_use_case)
):
    return await use_case.execute(request.q, request.max_results)
```

---

## 🐳 Infraestrutura Docker

### Arquitetura

```
┌──────────────────────────────────────┐
│     youtube-api-network (bridge)     │
│                                      │
│  ┌────────────────┐  ┌────────────┐ │
│  │  youtube-api   │  │   redis    │ │
│  │  (FastAPI)     │──│  (cache)   │ │
│  │  Port: 8000    │  │  Port:6379 │ │
│  └────────────────┘  └────────────┘ │
└──────────────────────────────────────┘
         │                    │
    localhost:8000       localhost:6379
```

### Componentes

- **API**: Python 3.11-slim, 4 workers, non-root user
- **Redis**: v7-alpine, 256MB limit, persistência em volume
- **Network**: Bridge isolada
- **Health checks**: Ambos containers monitorados

---

## 🔄 Fluxo de Dados Completo

```
1. HTTP GET /api/v1/channels/info/@youtube
2. [RateLimitMiddleware] → Verifica rate limit
3. [ErrorHandlerMiddleware] → Try/catch global
4. [Route] → Valida entrada (Pydantic)
5. [Use Case] → use_case.execute("@youtube")
6. [Repository] → Gera hash cache
7a. Cache HIT → Retorna do Redis
7b. Cache MISS → Scraping YouTube → Salva Redis
8. [Route] → Converte para APIResponse
9. HTTP Response 200 OK
```

---

## 🧪 Testabilidade

```python
# Test unitário (mock)
def test_get_channel_info():
    mock_repo = Mock(spec=IYouTubeRepository)
    mock_repo.get_channel_info.return_value = Channel(name="Test")
    use_case = GetChannelInfoUseCase(repository=mock_repo)
    assert use_case.execute("@test").name == "Test"

# Test integração (cache fake)
def test_repository_with_cache():
    repository = YTBPyRepository(cache=MemoryCache())
    channel = repository.get_channel_info("@youtube")
    assert channel.name is not None

# Test E2E (API real)
def test_api_endpoint():
    response = client.get("/api/v1/channels/info/@youtube")
    assert response.status_code == 200
```

---

## 🚀 Escalabilidade

```
Load Balancer
      ↓
API-1, API-2, API-3  ← Horizontal scaling
      ↓
  Redis (shared)     ← Cache compartilhado
```

```bash
# Escalar para 3 instâncias
docker-compose up -d --scale youtube-api=3
```

---

## 🎯 Benefícios

- ✅ **Manutenível**: Código organizado e limpo
- ✅ **Testável**: Mocks fáceis, testes isolados
- ✅ **Escalável**: Stateless, cache compartilhado
- ✅ **Extensível**: Adicionar features sem quebrar código
