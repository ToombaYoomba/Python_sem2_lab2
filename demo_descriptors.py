from src.domain.task import Task


def demo_descriptors():
    task = Task(task_id="demo-1", description="Test task", priority=3)

    print("=" * 50)
    print("1. DATA ДЕСКРИПТОР (ValidatedAttribute)")
    print("   Всегда проверяет значение")
    
    try:
        task.priority = 10
        print(f"   - priority = {task.priority}")
    except Exception as e:
        print(f"   - Ошибка: {e}")

    print("\n2. NON-DATA ДЕСКРИПТОР (CachedProperty)")
    print("   Можно переопределить через __dict__")
    print(f"   - Первый вызов: {task.urgency_score}")
    
    task.__dict__['urgency_score'] = 999
    print(f"   - После подмены: {task.urgency_score}")
    
    del task.__dict__['urgency_score']
    print(f"   - После очистки: {task.urgency_score}")

    print("\n3. НЕИЗМЕНЯЕМЫЙ АТРИБУТ")
    try:
        task.id = "new-id"
    except Exception as e:
        print(f"   - Нельзя изменить id: {e}")

    print("\n" + "=" * 50)
    print("ИТОГ:")
    print("- Data: всегда контролирует доступ")
    print("- Non-data: можно подменить через __dict__")
    print("=" * 50)


if __name__ == "__main__":
    demo_descriptors()