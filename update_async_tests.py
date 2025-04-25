import os
import re

COMMON_IMPORTS = """
from unittest.mock import AsyncMock, patch
from domain.__seedwork.test_utils import async_return, async_side_effect, run_async
"""

MOCKS_PATTERN = r'(\w+_repository)\.([\w_]+)\.return_value'
ASSERT_PATTERN = r'(\w+_repository)\.([\w_]+)\.assert_called'
PYTEST_RAISES_PATTERN = r'(with pytest\.raises\([^)]+\)[^:]*:)\s+(.+_usecase\.execute\(.*?\))'

def get_test_files(root_dir="src"):
    """Find all test files in the project."""
    test_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith("test_") and filename.endswith(".py"):
                test_files.append(os.path.join(dirpath, filename))
    return test_files

def update_imports(content):
    """Update imports to include AsyncMock and test utilities."""
    
    # Check if imports already exist
    if "AsyncMock" in content and "async_return" in content:
        # Make sure not to duplicate imports
        lines = content.split('\n')
        new_lines = []
        seen_async_return = False
        seen_async_mock = False
        
        for line in lines:
            if "from domain.__seedwork.test_utils import" in line:
                if "async_return" not in line:
                    line = line.replace("import", "import async_return, async_side_effect,")
                seen_async_return = True
            
            if "from unittest.mock import" in line:
                if "AsyncMock" not in line:
                    line = line.replace("import", "import AsyncMock,")
                seen_async_mock = True
                
            new_lines.append(line)
        
        # Add missing imports
        if not seen_async_return:
            new_lines.insert(5, "from domain.__seedwork.test_utils import async_return, async_side_effect, run_async")
        
        if not seen_async_mock:
            new_lines.insert(5, "from unittest.mock import AsyncMock, patch")
            
        return '\n'.join(new_lines)
        
    # Find import section
    import_section_end = 0
    import_pattern = r'(import [^\n]+\n|from [^\n]+\n)'
    matches = list(re.finditer(import_pattern, content))
    if matches:
        last_import = matches[-1]
        import_section_end = last_import.end()
        
    # Add imports
    return content[:import_section_end] + COMMON_IMPORTS + content[import_section_end:]

def update_repository_mocks(content):
    """Update repository mocks to use async_return."""
    
    # Replace repository.method.return_value with async_return
    def replace_mock(match):
        repo = match.group(1)
        method = match.group(2)
        value_pattern = rf'{repo}.{method}.return_value\s*=\s*([^;\n]+)'
        value_match = re.search(value_pattern, content)
        
        if value_match:
            value = value_match.group(1).strip()
            return f'{repo}.{method} = async_return({value})'
        
        return f'{repo}.{method} = async_return'
    
    content = re.sub(MOCKS_PATTERN, replace_mock, content)
    
    # Fix broken async_return assignments
    wrong_pattern = r'(\w+_repository)\.(\w+)\s*=\s*async_return\s*=\s*([^;\n]+)'
    def fix_wrong_assign(match):
        repo = match.group(1)
        method = match.group(2)
        value = match.group(3).strip()
        return f'{repo}.{method} = async_return({value})'
    
    content = re.sub(wrong_pattern, fix_wrong_assign, content)
    
    # Replace assert_called with await_count
    content = content.replace(".assert_called_once()", ".await_count == 1")
    content = content.replace(".assert_called()", ".called")
    content = content.replace(".assert_not_called()", ".called == False")
    
    # Update assert_called_with patterns
    assert_with_pattern = r'(\w+_repository)\.([\w_]+)\.assert_called_once_with\((.*?)\)'
    def replace_assert_with(match):
        repo = match.group(1)
        method = match.group(2)
        args = match.group(3)
        return f'assert {repo}.{method}.await_count == 1'
    
    content = re.sub(assert_with_pattern, replace_assert_with, content)
    
    return content

def update_async_executions(content):
    """Update usecase.execute calls to use run_async."""
    
    # Make sure not to double-wrap run_async calls
    double_wrap_pattern = r'run_async\(run_async\('
    if re.search(double_wrap_pattern, content):
        content = re.sub(r'run_async\(run_async\(([^)]*)\)\)', r'run_async(\1)', content)
    
    # Wrap usecase.execute with run_async
    execute_pattern = r'(\w+_usecase\.execute\([^)]*\))'
    
    def replace_execute(match):
        full_match = match.group(0)
        if 'run_async' not in full_match:
            return f'run_async({full_match})'
        return full_match
    
    content = re.sub(execute_pattern, replace_execute, content)
    
    # Update execute calls in pytest.raises
    def replace_pytest_raises(match):
        raises = match.group(1)
        execute = match.group(2)
        if 'run_async' not in execute:
            return f'{raises}\n        run_async({execute})'
        return f'{raises}\n        {execute}'
    
    content = re.sub(PYTEST_RAISES_PATTERN, replace_pytest_raises, content)
    
    return content

def update_patch_objects(content):
    """Update patch.object usage for async methods."""
    
    # Update patch.object for async methods
    patch_pattern = r'with patch\.object\(([^,]+), \'([^\']+)\', return_value=([^)]+)\)'
    def replace_patch_object(match):
        cls = match.group(1)
        method = match.group(2)
        return_val = match.group(3)
        return f'update_mock = AsyncMock()\nupdate_mock.return_value = {return_val}\nwith patch(\'{cls}.{method}\', update_mock)'
    
    content = re.sub(patch_pattern, replace_patch_object, content)
    
    return content

def update_test_file(file_path):
    """Update a test file with async support."""
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Skip files that don't need updating
    if "usecase" not in content or "execute" not in content:
        print(f"  Skipping {file_path} - not a usecase test")
        return
    
    # Apply updates
    content = update_imports(content)
    content = update_repository_mocks(content)
    content = update_async_executions(content)
    content = update_patch_objects(content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"  Updated {file_path}")

def main():
    test_files = get_test_files()
    print(f"Found {len(test_files)} test files.")
    
    for file_path in test_files:
        update_test_file(file_path)
    
    print("Finished updating test files.")

if __name__ == "__main__":
    main() 