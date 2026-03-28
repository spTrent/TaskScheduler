# Task Scheduler

Проект для управления задачами
---

## Возможности

* Создание задач с инвариантами
* Поддержка нескольких источников данных:

  * Файл (`FileSource`)
  * JSON (`JsonSource`)
  * Генератор (`GeneratorSource`)
  * Ручной ввод (`ManualSource`)
* Валидация данных через дескрипторы
* Управление статусом задач:

  * завершение (`mark_done`)
  * переоткрытие (`reopen`)

---

### Task

```python
Task.create(
    id=1,
    title="Finish project",
    priority=3,
    description="Complete backend logic",
)
```

### Основные поля:

* `id: int`
* `title: str`
* `priority: int`
* `description: str`
* `created_at: datetime`
* `deadline: datetime`
* `done: bool`
* `done_at: Optional[datetime]`

---

### Инварианты:

* ❌ Нельзя указать `done_at`, если `done=False`
* ❌ `deadline < created_at`
* ❌ `done_at < created_at`
* ❌ `reopen()` с прошедшим дедлайном

---

### Методы:

```python
task.mark_done()
task.reopen()
```

---

## Структура

```
src/
├── contracts/
│   ├── task.py
│   ├── source.py
│   ├── descriptors/
│   └── exceptions/
│
├── sources/
│   ├── file_source.py
│   ├── json_source.py
│   ├── generator_source.py
│   └── manual_source.py
```

---

## Источники задач

Все источники реализуют общий интерфейс:

```python
class Source(Protocol):
    def get_task(self) -> Task: ...
```

## Формат дат

Используется стандарт ISO 8601:

```
2026-03-27T15:30:00+00:00
```