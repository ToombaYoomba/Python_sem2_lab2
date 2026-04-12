# Лабораторная №1 "Источники задач и контракты". Морхов Захар Александрович. М80-101БВ-25

* **Цель:** Освоить duck typing и контрактное программирование на примере источников задач
* **Библиотеки:** *typing*, *collections.abc*, *pathlib*, *json*, *typer*
* **Допущения:**
  - Задача (`Message`) содержит только `id`, `title`, `author`, `message`
  - Все источники реализуют контракт `MessageSource`, но не используют наследование
  - Контракт описан через `typing.Protocol` с `@runtime_checkable`
  - Новые источники добавляются без изменения существующего кода
  - Проверка контракта выполняется через `isinstance()`

* **Чему я научился:**
    - Создавать единый контракт для разных источников данных через `Protocol`
    - Проверять, что объект подходит под контракт, с помощью `isinstance`
    - Добавлять новые источники, не меняя старый код (через реестр)
    - Писать консольные команды с `typer`
    - Разработка CLI с помощью `typer`

## Структура проекта

 <pre>
    .
    ├── src/                               # Исходный код
    │   ├── contracts/                     # Контракты
    │   ├── inbox/                         # Ядро платформы
    │   ├── sources/                       # Реализации источников
    │   ├── __init__.py
    │   ├── __main__.py                    # Точка входа
    │   └── cli.py                         # CLI-интерфейс (typer)
    ├── source/                            # Пример данных
    ├── tests/                             # Pytest-тесты
    ├── .gitignore
    ├── pyproject.toml
    ├── uv.lock
    └── README.md
    └── Dockerfile
    └──.dockerignore
</pre>

## Интересные тест-кейсы
 - При чтении JSONL пустые строки игнорируются
 - Отсутствующие поля в JSON заменяются значениями по умолчанию
 - Некорректный JSON вызывает `ValueError` с указанием строки и файла
 - Для stdin строка должна содержать минимум 4 поля, разделённых `:`
 - При комбинировании нескольких источников задачи выводятся в порядке источников

## Инструкция к использованию
### Запуск программы

```python -m src.__main__ --help```
#### Основные команды
1. Просмотр доступных источников
```python -m src.__main__ plugins```
2. Чтение задач из JSONL-файла
```python -m src.__main__ read --jsonl source/messages.jsonl```
3. Чтение задач из стандартного ввода
```echo "1:Hello:Alice:Test" | python -m src.__main__ read --stdin```
4. Чтение с фильтром по содержимому
```python -m src.__main__ read --jsonl source/messages.jsonl --contains "Python"```
5. Комбинация нескольких источников
```
# Один JSONL-файл и stdin
echo "999:Stdin:From:StdIn" | python -m src.__main__ read --jsonl source/messages.jsonl --stdin

# Несколько JSONL-файлов (создайте копию для примера)
cp source/messages.jsonl source/messages2.jsonl
python -m src.__main__ read --jsonl source/messages.jsonl --jsonl source/messages2.jsonl

# Все источники вместе
echo "999:Stdin:From:StdIn" | python -m src.__main__ read --jsonl source/messages.jsonl --jsonl source/messages2.jsonl --stdin
```

### Установить репозиторий
```git clone https://github.com/ToombaYoomba/Python_sem2_lab1``` \
```cd Python_sem2_lab1```

### Запустить
```создать виртуальную среду python``` \
```py -m src.__main__ --help```

### Формат входных данных
* каждая строка — JSON-объект ```{"id": "1", "title": "Hello", "author": "Alice", "message": "First message"}```
* Стандартный ввод: каждая строка содержит 4 поля, разделённых двоеточием : ```id:title:author:message```
* Лучше использовать латиницу в полях title, author и message (это по ходу чисто ошибка windows)
* При указании нескольких JSONL-файлов убедитесь, что файлы существуют по указанным путям
* Для демонстрации работы с несколькими файлами можно создать копию существующего файла командой ```cp source/messages.jsonl source/messages2.jsonl```
