import asyncio
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar, Union

T = TypeVar('T')

# Cache simples em memória
_CACHE: Dict[str, Dict[str, Any]] = {}


class AsyncLRUCache:
    """
    Cache LRU assíncrono para armazenar resultados de funções.
    
    Implementa um cache simples com base no padrão LRU (Least Recently Used)
    para armazenar resultados de operações frequentes e lentas, como consultas
    ao banco de dados.
    """
    
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        """
        Inicializa o cache.
        
        Args:
            max_size: Tamanho máximo do cache (número de itens)
            ttl: Tempo de vida dos itens em segundos
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Obtém um item do cache.
        
        Args:
            key: Chave do item
            
        Returns:
            O valor armazenado no cache, ou None se não existir ou estiver expirado
        """
        if key not in self.cache:
            return None
        
        # Verifica se o item expirou
        item = self.cache[key]
        timestamp = item.get('timestamp', 0)
        if time.time() - timestamp > self.ttl:
            # Remove o item expirado
            del self.cache[key]
            del self._access_times[key]
            return None
        
        # Atualiza o tempo de acesso
        self._access_times[key] = time.time()
        return item.get('value')
    
    async def set(self, key: str, value: Any) -> None:
        """
        Adiciona um item ao cache.
        
        Args:
            key: Chave do item
            value: Valor a ser armazenado
        """
        # Verifica se o cache está cheio
        if len(self.cache) >= self.max_size:
            # Remove o item menos recentemente usado
            oldest_key = min(self._access_times.items(), key=lambda x: x[1])[0]
            del self.cache[oldest_key]
            del self._access_times[oldest_key]
        
        # Adiciona o novo item
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        self._access_times[key] = time.time()
    
    async def invalidate(self, key: str) -> None:
        """
        Remove um item do cache.
        
        Args:
            key: Chave do item a ser removido
        """
        if key in self.cache:
            del self.cache[key]
            del self._access_times[key]
    
    async def clear(self) -> None:
        """Limpa todo o cache."""
        self.cache.clear()
        self._access_times.clear()


# Instância global do cache
_cache = AsyncLRUCache()


def async_cached(ttl: int = 300, prefix: str = ''):
    """
    Decorador para cache assíncrono de funções.
    
    Exemplo de uso:
    ```
    @async_cached(ttl=60, prefix='user')
    async def get_user(user_id: str) -> User:
        # Lógica para buscar o usuário
        return user
    ```
    
    Args:
        ttl: Tempo de vida do cache em segundos
        prefix: Prefixo para a chave do cache
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Constrói a chave do cache
            key_parts = [prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            # Tenta obter do cache
            result = await _cache.get(cache_key)
            if result is not None:
                return result
            
            # Se não estiver no cache, executa a função
            result = await func(*args, **kwargs)
            
            # Armazena o resultado no cache
            await _cache.set(cache_key, result)
            return result
        return wrapper
    return decorator


def invalidate_cache(key_prefix: str = None):
    """
    Decorador para invalidar o cache após a execução de uma função.
    
    Exemplo de uso:
    ```
    @invalidate_cache(key_prefix='user')
    async def update_user(user_id: str, data: dict) -> User:
        # Lógica para atualizar o usuário
        return updated_user
    ```
    
    Args:
        key_prefix: Prefixo para as chaves do cache a serem invalidadas
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            
            # Invalida o cache com o prefixo especificado
            if key_prefix:
                # Precisa implementar uma lógica mais sofisticada para invalidade
                # apenas chaves com o prefixo especificado
                await _cache.clear()
            else:
                await _cache.clear()
            
            return result
        return wrapper
    return decorator