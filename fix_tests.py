#!/usr/bin/env python
import os
import re
import glob
from pathlib import Path

"""
Este script corrige os testes automaticamente:

1. Adiciona @pytest.mark.asyncio a todas as funções de teste que devem ser assíncronas
2. Converte run_async(usecase.execute(...)) para await usecase.execute(...)
3. Substitui await_count por assert_awaited_once_with
"""

def fix_test_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verifica se o pytest.mark.asyncio já está importado
    if 'import pytest' in content and 'pytest.mark.asyncio' not in content:
        content = content.replace('import pytest', 'import pytest')
    
    # Corrigir imports
    if 'from domain.__seedwork.test_utils import async_return, async_side_effect, run_async' in content:
        content = content.replace(
            'from domain.__seedwork.test_utils import async_return, async_side_effect, run_async',
            'from domain.__seedwork.test_utils import async_return, async_side_effect'
        )
    
    # Substituir Mock por AsyncMock
    if 'def cart_item_repository():' in content and 'return Mock()' in content:
        content = content.replace('return Mock()', 'return AsyncMock()')
    
    # Adicionar decorator para testes async e mudar a função para async
    test_funcs = re.finditer(r'def (test_\w+)\((.*?)\):', content)
    for match in test_funcs:
        func_name = match.group(1)
        args = match.group(2)
        
        # Pula se já estiver decorado
        prev_line = content[:match.start()].split('\n')[-1].strip()
        if '@pytest.mark.asyncio' in prev_line:
            continue
        
        # Substitui a definição da função
        old_def = f'def {func_name}({args}):'
        new_def = f'@pytest.mark.asyncio\nasync def {func_name}({args}):'
        content = content.replace(old_def, new_def)
    
    # Substituir run_async por await
    pattern = r'(\w+) = run_async\((\w+\.\w+\(.*?\))\)'
    content = re.sub(pattern, r'\1 = await \2', content)
    
    # Substituir await_count por assert_awaited_once_with
    pattern = r'assert (\w+\.\w+)\.await_count == 1'
    content = re.sub(pattern, r'\1.assert_awaited_once_with()', content)
    
    # Substituir run_async(usecase.execute)(args) por await usecase.execute(args)
    pattern = r'run_async\((\w+\.\w+)\)\((.*?)\)'
    content = re.sub(pattern, r'await \1(\2)', content)
    
    # Salvar o arquivo corrigido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {file_path}")

def main():
    # Localiza todos os arquivos de teste
    test_files = glob.glob("src/**/test_*.py", recursive=True)
    for file_path in test_files:
        if os.path.exists(file_path):
            fix_test_file(file_path)

if __name__ == "__main__":
    main() 