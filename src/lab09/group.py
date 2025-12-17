from pathlib import Path
import csv
from typing import List, Union

try:
    from lab08.models import Student
except ImportError:
    import sys
    from pathlib import Path as PathLib
    current_file = PathLib(__file__)
    parent_dir = current_file.parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    from lab08.models import Student

CSV_HEADER = ("fio", "birthdate", "group", "gpa")


class Group:
    def __init__(self, storage_path: Union[str, Path]):
        self.path = Path(storage_path)

    def _read_all(self) -> List[Student]:
        if not self.path.exists():
            return []

        students = []
        with self.path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != list(CSV_HEADER):
                raise ValueError(
                    f"Неверный заголовок CSV. Ожидается: {CSV_HEADER}, "
                    f"получено: {reader.fieldnames}"
                )

            for row in reader:
                try:
                    student = Student.from_dict(row)
                    students.append(student)
                except Exception as e:
                    raise ValueError(
                        f"Ошибка при чтении строки {row}: {e}"
                    ) from e

        return students

    def _write_all(self, students: List[Student]) -> None:
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            for student in students:
                writer.writerow([
                    student.fio,
                    student.birthdate,
                    student.group,
                    student.gpa,
                ])

    def list(self) -> List[Student]:
        return self._read_all()

    def add(self, student: Student) -> None:
        students = self._read_all()
        students.append(student)
        self._write_all(students)

    def find(self, substr: str) -> List[Student]:
        students = self._read_all()
        return [
            student
            for student in students
            if substr.lower() in student.fio.lower()
        ]

    def remove(self, fio: str) -> None:
        students = self._read_all()
        original_count = len(students)
        students = [s for s in students if s.fio != fio]

        if len(students) == original_count:
            raise ValueError(f"Студент с ФИО '{fio}' не найден")

        self._write_all(students)

    def update(self, fio: str, **fields) -> None:
        students = self._read_all()
        found = False

        for student in students:
            if student.fio == fio:
                found = True
                for key, value in fields.items():
                    if key not in CSV_HEADER:
                        raise ValueError(
                            f"Недопустимое поле '{key}'. "
                            f"Допустимые поля: {CSV_HEADER}"
                        )
                    setattr(student, key, value)
                student.__post_init__()
                break

        if not found:
            raise ValueError(f"Студент с ФИО '{fio}' не найден")

        self._write_all(students)


if __name__ == "__main__":
    import sys
    from pathlib import Path as PathLib

    current_file = PathLib(__file__)
    parent_dir = current_file.parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

    from lab08.models import Student

    csv_path = "src/data/lab09/students.csv"
    group = Group(csv_path)

    print("\n1. Список всех студентов:")
    students = group.list()
    if students:
        for i, student in enumerate(students, 1):
            print(f"   {i}. {student}")
    else:
        print("   Список пуст")

    print("\n2. Добавляем нового студента...")
    new_student = Student(
        fio="Петрова Мария",
        birthdate="2002-05-15",
        group="БИВТ-21-2",
        gpa=4.7
    )
    group.add(new_student)
    print(f"Добавлен: {new_student}")

    print("\n3. Список всех студентов после добавления:")
    students = group.list()
    for i, student in enumerate(students, 1):
        print(f"   {i}. {student}")

    print("\n4. Поиск студентов с 'Иван' в ФИО:")
    found = group.find("Иван")
    if found:
        for i, student in enumerate(found, 1):
            print(f"   {i}. {student}")
    else:
        print("   Не найдено")

    print("\n5. Обновляем данные студента 'Иванов Иван'...")
    group.update("Иванов Иван", group="БИВТ-21-3", gpa=4.5)
    print("Обновлено: группа и GPA")

    print("\n6. Список всех студентов после обновления:")
    students = group.list()
    for i, student in enumerate(students, 1):
        print(f"   {i}. {student}")

    print("\n7. Удаляем студента 'Петрова Мария'")
    group.remove("Петрова Мария")
    print("Удалено")

    print("\n8. Финальный список студентов:")
    students = group.list()
    if students:
        for i, student in enumerate(students, 1):
            print(f"   {i}. {student}")
    else:
        print("   Список пуст")

