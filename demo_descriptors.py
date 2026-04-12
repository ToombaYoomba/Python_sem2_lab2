from src.domain.task import Task


def demo_descriptors():
    print("=" * 60)
    print("Data vs Non-Data Descriptors Demo")
    print("=" * 60)

    task = Task(task_id="demo-1", description="Test task", priority=3)

    print("\n1. Data descriptor (ValidatedAttribute):")
    print("   - Has __get__ and __set__")
    print("   - Always intercepts attribute access")

    try:
        task.priority = 10
    except Exception as e:
        print(f"   - Validation works: {e}")

    print("\n2. Non-data descriptor (CachedProperty):")
    print("   - Has only __get__, no __set__")
    print("   - Can be shadowed by instance attribute")

    print(f"   - First call (cached): {task.urgency_score}")
    print(f"   - Second call (from cache): {task.urgency_score}")

    print(f"\n   - Instance __dict__ before: {[k for k in task.__dict__.keys() if 'urgency' in k]}")
    task.__dict__['urgency_score'] = 999
    print(f"   - After __dict__['urgency_score'] = 999")
    print(f"   - Instance __dict__ after: {[k for k in task.__dict__.keys() if 'urgency' in k]}")
    print(f"   - Access via descriptor still returns cached: {task.urgency_score}")
    print(f"   - Direct __dict__ access: {task.__dict__['urgency_score']}")

    del task.__dict__['urgency_score']
    print(f"\n   - After deletion from __dict__")
    print(f"   - Access via descriptor: {task.urgency_score}")

    print("\n3. Immutable attributes:")
    try:
        task.id = "new-id"
    except Exception as e:
        print(f"   - Cannot modify id: {e}")

    print("\n" + "=" * 60)
    print("Key difference:")
    print("- Data descriptor: __set__ ALWAYS called, cannot be shadowed")
    print("- Non-data descriptor: can be shadowed by instance __dict__")
    print("- CachedProperty computes once, stores in __dict__, then returns directly")
    print("=" * 60)


if __name__ == "__main__":
    demo_descriptors()