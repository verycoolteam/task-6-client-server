import ast
import types
from typing import Any, Dict, Callable
from models import FunctionDefinition

def create_function_from_code(func_def: FunctionDefinition) -> Callable:
    """Создает исполняемую функцию из строки кода."""
    code_str = func_def.code.strip()
    if not code_str.startswith("def "):
        raise ValueError("Код функции должен начинаться с 'def'")

    # Парсим AST
    tree = ast.parse(code_str, mode='exec')
    # Компилируем
    compiled = compile(tree, filename="<string>", mode="exec")
    # Создаем локальное пространство
    local_scope = {}
    exec(compiled, {}, local_scope)

    # Находим определенную функцию
    func_name = func_def.metadata.name
    if func_name not in local_scope:
        raise ValueError(f"Функция '{func_name}' не найдена в коде")

    func = local_scope[func_name]

    # Проверяем сигнатуру (упрощенно)
    # Можно расширить для проверки типов и количества аргументов
    return func

def execute_function(func_def: FunctionDefinition, inputs: Dict[str, Any], parameters: Dict[str, Any]) -> Any:
    """Выполняет функцию с заданными входами и параметрами."""
    func = create_function_from_code(func_def)

    # Объединяем входы и параметры в один словарь
    all_args = {**inputs, **parameters}

    # Получаем список ожидаемых аргументов функции
    import inspect
    sig = inspect.signature(func)
    expected_args = list(sig.parameters.keys())

    # Проверяем, что все нужные аргументы переданы
    missing = [arg for arg in expected_args if arg not in all_args]
    if missing:
        raise ValueError(f"Отсутствуют обязательные аргументы: {missing}")

    # Вызываем функцию
    try:
        result = func(**all_args)
        return result
    except Exception as e:
        raise RuntimeError(f"Ошибка выполнения функции: {e}")