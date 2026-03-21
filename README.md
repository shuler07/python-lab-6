# Лабораторная работа №6

Система обработки задач с использованием объектно-ориентированного подхода и автоматизированного тестирования.

---

## Описание

Проект реализует платформу обработки задач (task processing platform). Задача — абстрактная единица работы с идентификатором и произвольными данными (payload), которая может поступать из различных источников, валидироваться и обрабатываться системой.

Реализованы две лабораторные работы в рамках единой предметной области.

---

## Лабораторная работа №1 — Источники задач и контракты

Реализована подсистема приёма задач. Источники не связаны наследованием, но реализуют единый поведенческий контракт через `typing.Protocol`.

**Что реализовано:**

- `TaskSource` — протокол источника задач (`@runtime_checkable`)
- `TaskJsonSource` — загрузка задач из JSON-файла
- `TaskGeneratorSource` — программная генерация случайных задач
- `TaskApiSource` — получение задач из API-заглушки
- `TaskProcessor` — обработка задач из любого источника через единый контракт
- Runtime-проверка контракта через `isinstance(source, TaskSource)`

---

## Лабораторная работа №2 — Модель задачи: дескрипторы и @property

Реализована модель задачи с корректной инкапсуляцией и валидацией состояния.

**Что реализовано:**

- `ValidatedLiteral` — пользовательский data-дескриптор (`__get__`, `__set__`, `__set_name__`) для валидации атрибутов с фиксированным набором допустимых значений
- `Task.status` и `Task.priority` — валидируются через `ValidatedLiteral` на уровне класса
- `Task.description` — валидируется через `@property` (data-дескриптор, встроенный)
- Специализированные исключения (`ValueError`, `TypeError`) при нарушении инвариантов
- `Task.ts_created_at` — время создания задачи в UTC (timestamp)

**Типы статусов:** `idle`, `active`, `done`

**Типы приоритетов:** `low`, `medium`, `high`, `critical`

---

## Установка

```bash
pip install -r requirements.txt
```

---

## Запуск

Точка входа — модуль `src.main`:

```bash
python -m src.main [КОМАНДА] [АРГУМЕНТЫ]
```

### Команды

#### `task get` — получить задачи из источника

```bash
python -m src.main task get [SOURCE] [OPTIONS]
```

| Аргумент | Описание | По умолчанию |
|---|---|---|
| `SOURCE` | Источник: `generator`, `api`, `json` | `generator` |
| `-p`, `--path PATH` | Путь к JSON-файлу (только для `json`) | — |
| `-a`, `--all` | Получить все доступные задачи | `False` |

**Примеры:**

```bash
# Получить одну задачу из генератора
python -m src.main task get

# Получить все задачи из генератора
python -m src.main task get generator --all

# Получить одну задачу из API
python -m src.main task get api

# Загрузить все задачи из JSON-файла
python -m src.main task get json -p example.json --all
```

#### `task process` — обработать задачи из источника

```bash
python -m src.main task process [SOURCE] [OPTIONS]
```

| Аргумент | Описание | По умолчанию |
|---|---|---|
| `SOURCE` | Источник: `generator`, `api`, `json` | `generator` |
| `-p`, `--path PATH` | Путь к JSON-файлу (только для `json`) | — |
| `-a`, `--all` | Обработать все доступные задачи | `False` |

**Примеры:**

```bash
# Обработать одну задачу из генератора
python -m src.main task process generator

# Обработать все задачи из JSON-файла
python -m src.main task process json -p example.json --all

# Обработать одну задачу из API
python -m src.main task process api
```

### Формат JSON-файла

```json
[
  {
    "id": 1,
    "payload": {
      "description": "Обработать заказ",
      "status": "idle",
      "priority": "high",
      "extras": "any_data",
    }
  }
]
```

---

## Тестирование

```bash
# Запустить тесты
pytest

# С отчётом о покрытии
pytest --cov --cov-report=term-missing
```

Минимальное покрытие: **80%**. Текущее покрытие: **~90%**.

---

## Структура проекта

```
.
├── src/
│   ├── __init__.py
│   ├── cli.py                   # CLI-интерфейс (typer)
│   ├── constants.py             # Константы
│   ├── descriptors.py           # Пользовательские дескрипторы (ValidatedLiteral)
│   ├── logger.py                # Логирование
│   ├── main.py                  # Точка входа
│   ├── task.py                  # Класс задачи, протокол TaskSource
│   ├── task_process.py          # TaskProcessor — обработка задач из источников
│   └── task_sources.py          # Источники задач (JSON, генератор, API)
├── tests/
│   ├── __init__.py
│   └── test_task_process.py     # Модульные тесты (pytest)
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml               # Конфиг проекта и pytest-cov
├── example.json                 # Пример JSON-файла с задачами
├── README.md
└── requirements.txt             # Зависимости проекта
```
