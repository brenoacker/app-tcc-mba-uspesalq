import asyncio
import functools
import inspect
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from unittest.mock import AsyncMock, MagicMock, patch

T = TypeVar('T')

def run_async(coro):
    """
    Executa uma coroutine em um novo event loop.
    
    NOTA: Para testes marcados com @pytest.mark.asyncio, use "await" diretamente.
    Esta função é útil apenas para testes síncronos que precisam chamar código assíncrono.
    
    Exemplo:
    ```
    # Em um teste síncrono normal:
    result = run_async(my_async_function())
    
    # Em um teste assíncrono (@pytest.mark.asyncio):
    # Não use run_async, use await diretamente:
    result = await my_async_function()
    ```
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        return loop.run_until_complete(coro)
    finally:
        if not loop.is_running():
            loop.close()

def async_return(value: Any) -> AsyncMock:
    """
    Cria um AsyncMock que retorna o valor especificado quando awaited.
    
    Exemplo:
    ```
    repository.find_item = async_return(some_value)
    ```
    """
    mock = AsyncMock()
    mock.return_value = value
    return mock

def async_side_effect(side_effect: Union[List[Any], Dict[Any, Any], Callable, Exception]) -> AsyncMock:
    """
    Cria um AsyncMock com um side_effect especificado.
    
    Exemplo:
    ```
    repository.find_item = async_side_effect(ValueError("Not found"))
    ```
    """
    mock = AsyncMock()
    mock.side_effect = side_effect
    return mock

def patch_async_mock(target: str, **kwargs) -> Any:
    """
    Cria um patch com um AsyncMock.
    
    Exemplo:
    ```
    @patch_async_mock('module.AsyncClass.method')
    @pytest.mark.asyncio
async def test_method(self, mock_method):
        mock_method.return_value = value
        ...
    ```
    """
    return patch(target, new_callable=AsyncMock, **kwargs) 