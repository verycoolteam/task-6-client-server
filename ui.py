import click
import json
from storage import FunctionStorage
from executor import execute_function
from models import (
    FunctionDefinition,
    FunctionMetadata,
    FunctionSignature,
    FunctionExecutionRequest
)

storage = FunctionStorage()

@click.group()
def ui():
    pass

@ui.command()
@click.argument('name')
@click.option('--code', prompt='Код функции (def ...)', help='Тело функции на Python')
@click.option('--input-params', multiple=True, help='Имена входных параметров x (можно указывать несколько раз, например: --input-params x1 --input-params x2)')
@click.option('--param-names', multiple=True, help='Имена параметров λ (можно указывать несколько раз)')
@click.option('--output-type', default='Any', help='Тип выхода')
@click.option('--description', help='Описание функции')
def create(name, code, input_params, param_names, output_type, description):
    signature = FunctionSignature(
        input_params=list(input_params),
        output_type=output_type,
        param_names=list(param_names)
    )
    metadata = FunctionMetadata(
        name=name,
        signature=signature,
        description=description
    )
    func_def = FunctionDefinition(metadata=metadata, code=code)
    storage.save_function(func_def)
    click.echo(f"Функция '{name}' создана.")

@ui.command()
@click.argument('name')
def info(name):
    func = storage.get_function(name)
    if not func:
        click.echo(f"Функция '{name}' не найдена.")
        return
    click.echo(json.dumps(func.metadata.dict(), indent=2, ensure_ascii=False))

@ui.command(name='list')
def list_functions():
    funcs = storage.list_functions()
    if not funcs:
        click.echo("Нет сохраненных функций.")
    else:
        for f in funcs:
            click.echo(f"• {f}")

@ui.command()
@click.argument('name')
def delete(name):
    if storage.delete_function(name):
        click.echo(f"Функция '{name}' удалена.")
    else:
        click.echo(f"Функция '{name}' не найдена.")

@ui.command()
@click.argument('name')
@click.option('--input', 'input_pairs', multiple=True, help='Входные параметры: key=value')
@click.option('--param', 'param_pairs', multiple=True, help='Параметры λ: key=value')
def execute(name, input_pairs, param_pairs):
    func = storage.get_function(name)
    if not func:
        click.echo(f"Функция '{name}' не найдена.")
        return

    inputs = {}
    for i in input_pairs:
        if '=' not in i:
            click.echo(f"Неверный формат входного параметра: {i}. Ожидается key=value")
            return
        k, v = i.split('=', 1)
        try:
            inputs[k] = float(v) if '.' in v else int(v)
        except ValueError:
            inputs[k] = v

    parameters = {}
    for p in param_pairs:
        if '=' not in p:
            click.echo(f"Неверный формат параметра: {p}. Ожидается key=value")
            return
        k, v = p.split('=', 1)
        try:
            parameters[k] = float(v) if '.' in v else int(v)
        except ValueError:
            parameters[k] = v

    try:
        result = execute_function(func, inputs, parameters)
        click.echo(f"Результат: {result}")
    except Exception as e:
        click.echo(f"Ошибка выполнения: {e}")

if __name__ == '__main__':
    ui()