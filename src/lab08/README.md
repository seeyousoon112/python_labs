# Лабораторная работа 8

## Модель `Student`

- реализована в `models.py` с использованием `@dataclass`;
- поля: `fio`, `birthdate`, `group`, `gpa`;
- методы:
  - `age()` — количество полных лет;
  - `to_dict()` / `from_dict()` — (де)сериализация атрибутов;
  - `__str__()` — человекочитаемый вывод;
- валидация в `__post_init__`:
  - формат даты `YYYY-MM-DD`;
  - диапазон `0 ≤ gpa ≤ 5`.

## Сериализация

Модуль `serialize.py` содержит функции:

```python
students_to_json(list[Student], path)
students_from_json(path) -> list[Student]
```

Пример использования:

```python
from lab08.models import Student
from lab08.serialize import students_to_json, students_from_json

students = [
    Student("Алексей Смирнов", "2002-03-14", "SE-01", 4.5),
    Student("Мария Иванова", "2001-11-02", "SE-02", 4.8),
]

students_to_json(students, "data/lab08/students_output.json")
restored = students_from_json("data/lab08/students_output.json")
```

## Примеры JSON

В `data/lab08/` находятся:

- `students_input.json` — исходные данные;
- `students_output.json` — результат сериализации.
Весь код приведет к стилю black 



