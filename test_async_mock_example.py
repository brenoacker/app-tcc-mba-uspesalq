import asyncio
import pytest
from unittest.mock import AsyncMock, patch

# O módulo que estamos testando
class Repository:
    async def find_item(self, item_id):
        # Simulando acesso a banco de dados
        await asyncio.sleep(0.1)
        return {"id": item_id, "name": "Test Item"}

class UseCase:
    def __init__(self, repository):
        self.repository = repository
    
    async def execute(self, item_id):
        item = await self.repository.find_item(item_id=item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found")
        return item

# Utilitários para teste
def async_return(value):
    mock = AsyncMock()
    mock.return_value = value
    return mock

# Testes
@pytest.mark.asyncio
async def test_execute_success():
    # Arranjo
    repository = AsyncMock()
    repository.find_item = async_return({"id": 1, "name": "Test Item"})
    
    use_case = UseCase(repository)
    
    # Ação
    result = await use_case.execute(1)
    
    # Asserção
    assert result["id"] == 1
    assert result["name"] == "Test Item"
    # Verificar se o mock foi chamado
    repository.find_item.assert_awaited_once_with(item_id=1)

@pytest.mark.asyncio
async def test_execute_not_found():
    # Arranjo
    repository = AsyncMock()
    repository.find_item = async_return(None)
    
    use_case = UseCase(repository)
    
    # Ação/Asserção
    with pytest.raises(ValueError) as excinfo:
        await use_case.execute(1)
    
    assert str(excinfo.value) == "Item with id 1 not found"
    repository.find_item.assert_awaited_once_with(item_id=1)

def test_sync_way():
    # Esta é outra forma de testar código assíncrono de forma síncrona
    async def run_test():
        repository = AsyncMock()
        repository.find_item = async_return({"id": 1, "name": "Test Item"})
        
        use_case = UseCase(repository)
        result = await use_case.execute(1)
        
        assert result["id"] == 1
        assert result["name"] == "Test Item"
        
    # Execute a coroutine em um novo event loop
    asyncio.run(run_test()) 