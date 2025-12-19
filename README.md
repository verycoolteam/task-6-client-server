# task-6-client-server

Сервер для управления, хранения и выполнения параметризированных функций вида `y = f(x, λ)`. Поддерживает создание, чтение, обновление, удаление и вычисление функций через REST API и командную строку (CLI).

## Описание

Этот проект предоставляет два интерфейса для работы с динамически определяемыми функциями на Python:
- **HTTP REST API** (на FastAPI) — для интеграции с веб- и мобильными приложениями;
- **Командная строка (CLI)** — для локального управления и тестирования.

Функции сохраняются в файловой системе в формате JSON и могут быть повторно загружены при перезапуске сервера. Каждая функция сопровождается метаданными: именем, описанием, списком входов (`x`) и параметров (`λ`).

## Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone <https://github.com/verycoolteam/task-6-client-server.git>
cd <task-6-client-server>
```

### 2. Создайте виртуальное окружение

```bash
python3 -m venv .venv
```

### 3. Активируйте окружение

- Linux/macOS
```bash
source .venv/bin/activate
```
- Windows (PowerShell)
```bash
.\.venv\Scripts\Activate.ps1
```

### 4. Установите зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Запустите сервер

```bash
uvicorn main:app --reload
```

Сервер будет доступен по адресу: http://localhost:8000

### 6. Используйте UI или API для управления функциями

Пример работы с UI:

```bash
# Создать функцию
python ui.py create linear \
  --code "def linear(x, a, b): return a * x + b" \
  --input-params x \
  --param-names a --param-names b \
  --output-type float \
  --description "Линейная функция"

# Выполнить функцию
python ui.py execute linear --input x=10 --param a=2 --param b=3

# Посмотреть список функций
python ui.py list

# Получить информацию о функции
python ui.py info linear
```

Пример работы с API:

```bash
curl -X POST "http://localhost:8000/functions/" \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "name": "quadratic",
      "signature": {
        "input_params": ["x"],
        "output_type": "float",
        "param_names": ["a", "b", "c"]
      },
      "description": "Квадратичная функция: y = a*x^2 + b*x + c"
    },
    "code": "def quadratic(x, a, b, c): return a * x**2 + b * x + c"
  }'
```