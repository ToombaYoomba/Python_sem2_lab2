# Лабораторная №2 "Модель задачи: дескрипторы и свойства". Морхов Захар Александрович. М80-101БВ-25

* **Цель:** Освоить управление доступом к атрибутам и защиту инвариантов доменной модели с помощью пользовательских дескрипторов и `property`
* **Библиотеки:** *datetime*, *typing*, *pytest*
* **Допущения:**
  - Задача (`Task`) содержит `id`, `description`, `priority`, `status`, `created_at`
  - Приоритет задаётся целым числом от 1 до 5
  - Статус может быть: `pending`, `in_progress`, `completed`, `cancelled`
  - `id` и `created_at` являются неизменяемыми (immutable)
  - Валидация атрибутов выполняется через data-дескрипторы
  - Вычисляемые свойства реализованы через `@property` и non-data дескриптор `CachedProperty`

* **Чему я научился:**
    - Создавать data-дескрипторы с валидацией через `__get__` и `__set__`
    - Создавать non-data дескрипторы для кэширования вычислений
    - Использовать `@property` для вычисляемых атрибутов
    - Защищать инварианты объекта через иммутабельные поля


## Структура проекта

## Структура проекта (дополненная)

 <pre>
    .
    ├── src/                               # Исходный код
    │   ├── contracts/                     # Контракты
    │   ├── domain/                        # НОВОЕ: доменная модель с дескрипторами
    │   ├── inbox/                         # ОБНОВЛЕНО: добавлен метод iter_tasks()
    │   ├── sources/                       # Реализации источников
    │   ├── __init__.py
    │   ├── __main__.py                    # Точка входа
    │   └── cli.py                         # ОБНОВЛЕНО: добавлена команда tasks
    ├── source/                            # Пример данных
    ├── tests/                             # Pytest-тесты
    │   └── test_task.py                   # НОВОЕ: тесты модели Task
    ├── demo_descriptors.py                # НОВОЕ: демонстрация дескрипторов
    ├── .gitignore
    ├── pyproject.toml
    ├── uv.lock
    └── README.md
</pre>

## Интересные тест-кейсы
 - Некорректный id (пустая строка, не str) вызывает `InvalidTaskIdError`
 - Слишком короткое (менее 3 символов) или длинное (более 1000) описание вызывает `InvalidDescriptionError`
 - Приоритет вне диапазона 1-5 вызывает `InvalidPriorityError`
 - Недопустимый статус вызывает `InvalidStatusError`
 - Попытка изменения `id` или `created_at` вызывает `ImmutableAttributeError`
 - Недопустимые переходы между статусами (например, завершение отменённой задачи) вызывают `InvalidStatusError`

## Инструкция к использованию
### Запуск программы

```python -m src.__main__ --help```
#### Основные команды
1. Просмотр задач из JSONL-файла
```python -m src.__main__ tasks --jsonl source/messages.jsonl```
2. Просмотр задач с указанным приоритетом
```python -m src.__main__ tasks --jsonl source/messages.jsonl --priority 1```
3. Только готовые к выполнению задачи
```python -m src.__main__ tasks --jsonl source/messages.jsonl --ready```
4. Просмотр задач из стандартного ввода
```echo "99:Test:Me:Hello" | python -m src.__main__ tasks --stdin```
5. Комбинация источников
```echo "99:Stdin:From:StdIn" | python -m src.__main__ tasks --jsonl source/messages.jsonl --stdin```
6. Демонстрация работы дескрипторов
```python demo_descriptors.py```

### Установить репозиторий
```git clone https://github.com/ToombaYoomba/Python_sem2_lab2``` \
```cd Python_sem2_lab2```

### Запустить
```создать виртуальную среду python``` \
```py -m src.__main__ --help```

### Формат входных данных
* JSONL: каждая строка — JSON-объект с полями `id`, `title`, `author`, `message`
```{"id": "1", "title": "Hello", "author": "Alice", "message": "First message"}```
* Стандартный ввод: каждая строка содержит 4 поля, разделённых двоеточием `:`
```id:title:author:message```
* При создании задачи через `Task.from_message()` поле `description` формируется как `"title: message"`
* Приоритет задачи можно задать через опцию `--priority` (от 1 до 5, по умолчанию 3)
