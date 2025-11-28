# python_labs

# Лабораторная работа #8
## models
```python
from dataclasses import dataclass
from datetime import date, datetime


DATE_FORMAT = "%Y-%m-%d"


@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    @staticmethod
    def _validate_birthdate(value: str) -> date:
        try:
            return datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(
                f"Некорректный формат даты '{value}'. Ожидается {DATE_FORMAT}"
            )

    @staticmethod
    def _validate_gpa(value: float) -> float:
        try:
            gpa_value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Средний балл должен быть числом")

        if not 0 <= gpa_value <= 5:
            raise ValueError("Средний балл должен быть в диапазоне от 0 до 5")
        return gpa_value

    def __post_init__(self) -> None:
        self._birthdate_dt = self._validate_birthdate(self.birthdate)
        self.gpa = self._validate_gpa(self.gpa)

    def age(self) -> int:
        today = date.today()
        years = today.year - self._birthdate_dt.year
        if (today.month, today.day) < (self._birthdate_dt.month, self._birthdate_dt.day):
            years -= 1
        return years

    def to_dict(self):
        return {
            "fio": self.fio,
            "birthdate": self.birthdate,
            "group": self.group,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            fio=data["fio"],
            birthdate=data["birthdate"],
            group=data["group"],
            gpa=data["gpa"],
        )
    # @classmethod
    # def from_dict(data):
    #     return Student(
    #         fio=data["fio"],
    #         birthdate=data["birthdate"],
    #         group=data["group"],
    #         gpa=data["gpa"],
    #     )

    def __str__(self) -> str:
        return f"{self.fio} ({self.group}), {self.age()} лет, GPA {self.gpa:.2f}"
```
![Картинка 1](./images/lab08/database.png)
## serialize
``` python
import json
from pathlib import Path

from models import Student

DATA_DIR = Path(__file__).parent.parent
students = [
    Student(fio="Иванов Иван Иванович", birthdate="2000-05-15", group="ИТ-101", gpa=4.5),
    Student(fio="Петрова Анна Сергеевна", birthdate="2001-03-20", group="ИТ-101", gpa=4.8),
    Student(fio="Сидоров Алексей Петрович", birthdate="1999-12-10", group="ФИ-201", gpa=3.9)
]
def students_to_json(students, path: str | Path) -> None:
    output_path = Path(path)
    data = [student.to_dict() for student in students]
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
students_to_json(students, "src/data/lab08/students_output.json")


def students_from_json(path: str | Path):
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"Файл не найден: {input_path}")
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Ожидается список студентов в JSON")
    return [Student.from_dict(item) for item in data]
students = students_from_json('src/data/lab08/students_output.json')
for student in students:
    print(student)
```
![Картинка 2](./images/lab08/serialize.png)
## стиль
![Картинка 3](./images/lab08/blackk.png)

# Лабораторная работа #7
## test_text
```python
import pytest
from lib.text import normalize
from lib.text import tokenize
from lib.text import count_freq
from lib.text import top_n


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Привет, Мир!", "привет мир"),
        (" Ёлка-ёлка ", "елка-елка"),
        ("", ""),
        ("Hello World 123", "hello world 123"),
        ("!@!###!", ""),
        ("e-mail адрес", "e-mail адрес"),
    ],
)
def test_normalize(text, expected):
    assert normalize(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Привет, Мир!", ["Привет", "Мир"]),
        ("Hello World", ["Hello", "World"]),
        ("", []),
        ("!!!@@@###", []),
        ("e-mail адрес", ["e-mail", "адрес"]),
        ("123 456", ["123", "456"]),
        ("word1 word2 word1", ["word1", "word2", "word1"]),
    ],
)
def test_tokenize(text, expected):
    assert tokenize(text) == expected


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["кот", "кот", "пёс"], [("кот", 2), ("пёс", 1)]),
        (["a", "b", "c"], [("a", 1), ("b", 1), ("c", 1)]),
        ([], []),
        (["word", "word", "word"], [("word", 3)]),
        (["a", "a", "b", "b", "c"], [("a", 2), ("b", 2), ("c", 1)]),
    ],
)
def test_count_freq(tokens, expected):
    result = count_freq(tokens)
    assert result == expected


@pytest.mark.parametrize(
    "freq, n, expected",
    [
        ({"кот": 5, "пёс": 3, "мышь": 1}, 2, [("кот", 5), ("пёс", 3)]),
        ({"banana": 2, "apple": 2, "cherry": 1}, 2, [("apple", 2), ("banana", 2)]),
        ({"яблоко": 3, "банан": 3, "вишня": 2}, 2, [("банан", 3), ("яблоко", 3)]),
        ({"a": 1, "b": 2}, 0, []),
        ({"a": 1, "b": 2}, -1, []),
        ({"a": 1, "b": 2}, 10, [("b", 2), ("a", 1)]),
        ({}, 5, []),
    ],
)
def test_top_n(freq, n, expected):
    assert top_n(freq, n) == expected


def test_top_n_same_frequency_alphabetical():
    freq = {"zebra": 2, "apple": 2, "banana": 2}
    result = top_n(freq, 3)
    assert result == [("apple", 2), ("banana", 2), ("zebra", 2)]
``` 
## test_json_csv
```python
import pytest
import json
import csv
from pathlib import Path
from lib.converters import json_to_csv, csv_to_json

DATA_DIR = Path(__file__).parent.parent / "data" / "samples"
SAMPLE_JSON_PATH = DATA_DIR / "people.json"
SAMPLE_CSV_PATH = DATA_DIR / "people.csv"


class TestJsonToCsv:
    def test_json_to_csv_success(self, tmp_path):

        json_path = SAMPLE_JSON_PATH
        csv_path = tmp_path / "output.csv"

        json_to_csv(str(json_path), str(csv_path))

        assert csv_path.exists()

        with open(json_path, "r", encoding="utf-8") as f:
            original_data = json.load(f)

        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == len(original_data)

        expected_keys = {"name", "age", "city"}
        assert set(rows[0].keys()) == expected_keys

        assert rows[0]["name"] == original_data[0]["name"]
        assert rows[0]["age"] == original_data[0]["age"]
        assert rows[0]["city"] == original_data[0]["city"]

    def test_json_to_csv_file_not_found(self, tmp_path):
        json_path = tmp_path / "nonexistent.json"
        csv_path = tmp_path / "output.csv"

        with pytest.raises(FileNotFoundError, match="JSON файл не найден"):
            json_to_csv(str(json_path), str(csv_path))

    def test_json_to_csv_wrong_extension(self, tmp_path):
        json_path = tmp_path / "test.txt"  # не .json
        csv_path = tmp_path / "output.csv"

        json_path.write_text("{}", encoding="utf-8")

        with pytest.raises(ValueError, match="Проверьте расширение файла"):
            json_to_csv(str(json_path), str(csv_path))

    def test_json_to_csv_empty_file(self, tmp_path):
        json_path = tmp_path / "empty.json"
        csv_path = tmp_path / "output.csv"

        json_path.write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            json_to_csv(str(json_path), str(csv_path))

    def test_json_to_csv_invalid_json(self, tmp_path):
        json_path = tmp_path / "invalid.json"
        csv_path = tmp_path / "output.csv"

        json_path.write_text("{invalid json}", encoding="utf-8")

        with pytest.raises((ValueError, json.JSONDecodeError)):
            json_to_csv(str(json_path), str(csv_path))


class TestCsvToJson:

    def test_csv_to_json_success(self, tmp_path):

        csv_path = SAMPLE_CSV_PATH
        json_path = tmp_path / "output.json"

        csv_to_json(str(csv_path), str(json_path))

        assert json_path.exists()

        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            csv_reader = csv.DictReader(f)
            original_rows = list(csv_reader)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == len(original_rows)

        expected_keys = {"name", "age", "city"}
        assert set(data[0].keys()) == expected_keys

        assert data[0]["name"] == original_rows[0]["name"]
        assert data[0]["age"] == original_rows[0]["age"]
        assert data[0]["city"] == original_rows[0]["city"]

    def test_csv_to_json_file_not_found(self, tmp_path):
        csv_path = tmp_path / "noneexist.csv"
        json_path = tmp_path / "output.json"

        with pytest.raises(FileNotFoundError):
            csv_to_json(str(csv_path), str(json_path))

    def test_csv_to_json_wrong_extension(self, tmp_path):
        csv_path = tmp_path / "test.txt"  # не .csv
        json_path = tmp_path / "output.json"

        csv_path.write_text("name,age\nAlice,22", encoding="utf-8")

        with pytest.raises(ValueError, match="Проверьте расширение файла"):
            csv_to_json(str(csv_path), str(json_path))

    def test_csv_to_json_empty_file(self, tmp_path):
        """Негативный: пустой CSV файл → ValueError"""
        csv_path = tmp_path / "empty.csv"
        json_path = tmp_path / "output.json"

        csv_path.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="В csv файле нет данных"):
            csv_to_json(str(csv_path), str(json_path))


class RoundTrip:
    # туда сюда

    def test_json_to_csv_to_json(self, tmp_path):
        json1_path = SAMPLE_JSON_PATH
        csv_path = tmp_path / "inter.csv"
        json2_path = tmp_path / "final.json"

        # JSON → CSV
        json_to_csv(str(json1_path), str(csv_path))

        # CSV → JSON
        csv_to_json(str(csv_path), str(json2_path))

        with open(json1_path, "r", encoding="utf-8") as f:
            original_data = json.load(f)

        with open(json2_path, "r", encoding="utf-8") as f:
            final_data = json.load(f)

        assert len(original_data) == len(final_data)

        assert original_data == final_data

    def test_csv_to_json_to_csv(self, tmp_path):
        csv1_path = SAMPLE_CSV_PATH
        json_path = tmp_path / "intermediate.json"
        csv2_path = tmp_path / "final.csv"

        csv_to_json(str(csv1_path), str(json_path))

        json_to_csv(str(json_path), str(csv2_path))

        with open(csv1_path, "r", encoding="utf-8", newline="") as f:
            reader1 = csv.DictReader(f)
            original_rows = list(reader1)

        with open(csv2_path, "r", encoding="utf-8", newline="") as f:
            reader2 = csv.DictReader(f)
            final_rows = list(reader2)

        assert len(original_rows) == len(final_rows)

        assert original_rows == final_rows
```
![Картинка 1](./images/lab07/style.png)

# Лабораторная работа #6
## cli_text 
```python
iimport argparse
from pathlib import Path
import sys 
current_file = Path(__file__)
 
parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir)) 
from lib.text import frequencies_from_text, sorted_word_counts

def main():
    parser = argparse.ArgumentParser(description='CLI утилита')
    subparser = parser.add_subparsers(dest='command')

    cat_parser=subparser.add_parser(
        'cat',
        help='Вывести содержимое файла',
        description='Вывести содержимое файла построчно. C -n добавляет номера строк'
    )
    cat_parser.add_argument('--input', required=True, help='Путь к входному файлу')
    cat_parser.add_argument('-n', action='store_true', dest='n', help='Нумеровать строки')

    stats_parser=subparser.add_parser(
        'stats',
        help='Анализ частот слов',
        description='Подсчитать частоты слов из файла и вывести топ-N самых частых'
    )
    stats_parser.add_argument('--input', required=True, dest='input', help='Путь к входному файлу')
    stats_parser.add_argument('--top', type=int, default=5, help='Сколько слов показать (по умолчанию 5)')
    args=parser.parse_args()
    if args.command is None:
        raise SystemExit(parser.format_help())

    if args.command == 'cat':
        in_path = Path(args.input)
        if not in_path.exists():
            raise FileNotFoundError(f"Входной файл не найден: {args.input}")
        with open(args.input, 'r', encoding='utf-8') as f:
            if args.n:
                for i, line in enumerate(f, 1):
                    print(f"{i}:{line}", end='')
            else:
                for line in f:
                    print(line, end='')
        
    elif args.command=='stats':
        in_path = Path(args.input)
        if not in_path.exists():
            raise FileNotFoundError(f"Входной файл не найден: {args.input}")
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
            freqs = frequencies_from_text(content)
            top_words = sorted_word_counts(freqs)[:args.top]
            for word, count in top_words:
                print(f"{word}:{count}")
if __name__=='__main__':
    main()

```
## -h сводка команд
python3 -m src.lab06.cli_text -h        
python3 -m src.lab06.cli_text cat -h    
python3 -m src.lab06.cli_text stats -h 
## сводка команд для проверки работоспособности программы: 
python3 -m src.lab06.cli_text cat --input src/data/input.txt -n

python3 -m src.lab06.cli_text stats --input src/data/input.txt --top 5
# cli_converter
```py
import argparse
from pathlib import Path
import sys 
current_file = Path(__file__)
print(f"Текущий файл: {current_file}")

parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))
from lab05.A import csv_to_json, json_to_csv
from lab05.B import csv_to_xlsx
def main():
    parser=argparse.ArgumentParser(description='CLI конвертация файлов')
    subparsers=parser.add_subparsers(dest='command')

    #json2csv
    json2csv_parser=subparsers.add_parser(
        'json2csv',
        help='Конвертировать JSON в CSV',
        description='Преобразовать JSON-файл (список объектов) в CSV с заголовком'
    )
    json2csv_parser.add_argument('--in', dest='input', required=True, help='Входной JSON-файл')
    json2csv_parser.add_argument('--out', dest='output', required=True, help='Выходной CSV-файл')
    
    #csv2json
    csv2json_parser=subparsers.add_parser(
        'csv2json',
        help='Конвертировать CSV в JSON',
        description='Преобразовать CSV-файл в JSON'
    )
    csv2json_parser.add_argument('--in', dest='input', required=True, help='Входной CSV-файл')
    csv2json_parser.add_argument('--out', dest='output', required=True, help='Выходной JSON-файл')

    #csv2xlsx
    csv2xlsx_parser=subparsers.add_parser(
        'csv2xlsx',
        help='Конвертировать CSV в XLSX',
        description='Преобразовать CSV-файл в Excel'
    )
    csv2xlsx_parser.add_argument('--in', dest='input', required=True, help='Входной CSV-файл')
    csv2xlsx_parser.add_argument('--out', dest='output', required=True, help='Выходной XLSX-файл')
    args=parser.parse_args()
    if args.command is None:
        raise SystemExit(parser.format_help())
    in_path = Path(args.input)
    if not in_path.exists():
        raise FileNotFoundError(f"Входной файл не найден: {args.input}")
    if args.command == 'json2csv':
        if in_path.suffix.lower() != '.json':
            raise ValueError("Ожидается входной файл .json для команды json2csv")
        if Path(args.output).suffix.lower() != '.csv':
            raise ValueError("Ожидается выходной файл .csv для команды json2csv")
        json_to_csv(args.input, args.output)
    elif args.command == 'csv2json':
        if in_path.suffix.lower() != '.csv':
            raise ValueError("Ожидается входной файл .csv для команды csv2json")
        if Path(args.output).suffix.lower() != '.json':
            raise ValueError("Ожидается выходной файл .json для команды csv2json")
        csv_to_json(args.input, args.output)
    elif args.command == 'csv2xlsx':
        if in_path.suffix.lower() != '.csv':
            raise ValueError("Ожидается входной файл .csv для команды csv2xlsx")
        if Path(args.output).suffix.lower() != '.xlsx':
            raise ValueError("Ожидается выходной файл .xlsx для команды csv2xlsx")
        csv_to_xlsx(args.input, args.output)
if __name__=='__main__':
    main()
    
    
```
## -h сводка команд:
python3 -m src.lab06.cli_convert -h

python3 -m src.lab06.cli_convert json2csv -h

python3 -m src.lab06.cli_convert csv2json -h

python3 -m src.lab06.cli_convert csv2xlsx -
## сводка команд для провреки работоспособности программы:
python3 -m src.lab06.cli_convert json2csv --in src/data/people.json --out src/data/people.csv

python3 -m src.lab06.cli_convert csv2json --in src/data/people.csv --out src/data/people.json

python3 -m src.lab06.cli_convert csv2xlsx --in src/data/people.csv --out src/data/people.xlsx

# Лабораторная работа #5
## csv -> json
```py
import json
import csv
from pathlib import Path
import sys
current_file = Path(__file__)
print(f"Текущий файл: {current_file}")

parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))


def csv_to_json(csv_path: str, json_path: str) -> None:
    encoding='utf-8'
    input_path=Path(csv_path)
    output_path=Path(json_path)
    if not input_path.exists():
        raise FileNotFoundError('пожалуйста, проверьте путь к файлу')
    if input_path.suffix.lower()!='.csv':
        raise ValueError('Проверьте расширение файла')
    data=[]
    with open(input_path,'r',encoding=encoding,newline='') as csv_file:
        csv_reader=csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    with open(output_path,'w',encoding=encoding,newline='') as json_file:
        json.dump(data,json_file,ensure_ascii=False,indent=2 )
        print('Конвертация прошла успешно')
        print(f'Всего записей конвертировано:{len(data)}')
csv_to_json('src/data/people1.csv','src/data/people1.json')
```
## На ввод программе был дан .csv файл с данным содержимым:
![Картинка 1](./images/lab05/csv->json.png)
## результат записи: 
![Картинка 2](./images/lab05/result_json.png)

## json -> csv
```py
import json
import csv
from pathlib import Path
import sys
current_file = Path(__file__)
print(f"Текущий файл: {current_file}")
parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))
def json_to_csv(json_path: str | Path, csv_path: str | Path, encoding: str = "utf-8") -> None:
    input_path=Path(json_path)
    output_path=Path(csv_path)
    if not input_path.exists():
        raise FileNotFoundError(f"JSON файл не найден: {json_path}")
    with open(input_path,'r', encoding=encoding) as json_file:
        data = json.load(json_file)
    with open(output_path, 'w', newline='', encoding=encoding) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['name','age','city'])
        writer.writeheader()
        writer.writerows(data)
    print(f'Конвертировано {len(data)}')
json_to_csv('src/data/people2.json','src/data/people2.csv')
```
## На ввод программе был дан .json файл с данным содержимым:
![Картинка 1](./images/lab05/result_json.png)
## результат записи: 
![Картинка 2](./images/lab05/csv->json.png)
# csv -> xlsx
```py
import csv
from openpyxl import Workbook
from pathlib import Path
import sys
current_file = Path(__file__)
print(f"Текущий файл: {current_file}")

parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))

def csv_to_xlsx(csv_path: str | Path, xlsx_path: str | Path, encoding: str = "utf-8") -> None:

    csv_file = Path(csv_path)
    xlsx_file = Path(xlsx_path)
    
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV файл не найден: {csv_path}")
    
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Data"
    
    with open(csv_file, 'r', encoding='utf-8', newline='') as csv_open:
        csv_reader = csv.reader(csv_open)
        
        for row_index, row in enumerate(csv_reader,1):
            for col_index, value in enumerate(row,1):
                worksheet.cell(row=row_index, column=col_index, value=value)
    workbook.save(xlsx_file)
    print(f"Успешно сконвертировано: {csv_path} -> {xlsx_path}")
csv_to_xlsx('src/data/people.csv','src/data/test_for_xlsx.xlsx')
```
## На ввод программе был дан .csv файл с данным содержимым:
![Картинка 1](./images/lab05/csv->json.png)
## В результате перезаписи получаем это:
![Картинка 2](./images/lab05/excel_result.png)

# Лабораторная работа #4
# Все реализованные функции для работы с csv файлами:
![Картинка 1](./images/lab04/true_lab04.png)
# Все реализованные функции для работы со словами:
![Картинка 2](./images/lab04/realize_func.png)

# Задание A
```py
import sys
from pathlib import Path

current_file = Path(__file__)
print(f"Текущий файл: {current_file}")

parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))

from lib.io_txt_csv import read_text,write_csv
result=read_text('src/data/input.txt')
test=[('крокодил',3),('мурад',3 )]
write_csv(test,'src/data/output.csv',header=('word','count'))
```
# Задание B
```py 
from pathlib import *
import sys 
current_file = Path(__file__)
print(f"Текущий файл: {current_file}")

parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))
from lib.io_txt_csv import *
from lib.text import *

input_file = "src/data/input_test.txt" 
output_file = "data/output.csv" 
encoding = "utf-8" 
input_path = Path(input_file)
if not input_path.exists():
    print(f"Ошибка: Файл '{input_file}' не найден.")
    print("Пожалуйста, проверьте правильность пути к файлу.")
else:
    file=read_text(input_file,encoding)
    freq = frequencies_from_text(file)
    sorted_words = sorted_word_counts(freq)
        
    csv_rows = [[word, count] for word, count in sorted_words]
    csv_header = ('word', 'count')
        
    total_words = sum(freq.values())
    unique_words = len(freq)
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ 5 самых частых слов:")
        
    top_5 = sorted_words[:5]
    if top_5:
        for i, (word, count) in enumerate(top_5):
            print(f"  {i+1}. '{word}': {count}")
```
# на ввод заданию B был дан рассказ "Юшка" и вот что из этого вышло:
![Картинка 3](./images/lab04/report.png)

# Лабораторная работа 3
# Задание A
# normalize
```python 
import re
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True): 
    if casefold:
        text = text.casefold()
    if yo2e:
        text = text.replace('ё', 'е').replace('Ё', 'Е')
    pattern= (r'[a-zA-Zа-яА-ЯёЁ0-9]+([-][a-zA-Zа-яА-ЯёЁ0-9]+)*')
    normalized = []
    for match in re.finditer(pattern, text):
        normalized.append(match.group())
    return ' '.join(normalized).strip()
test_cases = ["ПрИвЕт\nМИр\t","ёжик, Ёлка","Hello\r\nWorld","  двойные   пробелы  "]
for test in test_cases:
    result=normalize(test)
    print(result)
```
![Картинка 1](./images/lab03/Alab1.png)
# tokenize
```python
from re import *
def tokenize(text):
    pattern = (r'[a-zA-Zа-яА-ЯёЁ0-9]+([-][a-zA-Zа-яА-ЯёЁ0-9]+)*')
    tokens = []
    for match in finditer(pattern,text):
        tokens.append(match.group())
    return tokens
test_cases = [
    "привет мир",
    "hello,world!!!",
    "no-настоящему круто", 
    "2025 год",
    "emoji 💬 не слово"
]
for text in test_cases:
    result = tokenize(text)
    print(result)
```
![Картинка 2](./images/lab03/Alab2.png)
# count_freq+top_n
```python
def count_freq(tokens: list[str]):
    d={x:tokens.count(x) for x in set(tokens)}
    return sorted(d.items(),key=lambda x:-x[1])
test_case1 = (["a","b","a","c","b","a"])
test_case2=["bb","aa","bb","aa","cc"]
print(count_freq(test_case1),count_freq(test_case2))
```
![Картинка 3](./images/lab03/Alab3.png)
# Задание B
```py
import sys
from lib import text
table_mode=True
stroka = sys.stdin.readline()
tokenized = text.tokenize(stroka)
unique_words = text.count_freq(tokenized)
result = text.count_freq(unique_words)
top_words=result[:5]
if table_mode:
    max_word_ln=max(len(str(word[0][0])) for word in top_words)
    max_width=max(max_word_ln,5)
    print(f"\nТоп-5:")
    print(f"| {'слово':{max_width}} | {'частота'} |")
    print(f"|{'-' * (max_width + 2)}|---------|")
    for word_row in top_words:
        word=word_row[0][0]
        gusi= word_row[0][1]
        print(f"| {word:{max_width}} | {gusi:<7} |")
else:
    print(f"Топ-{5}:")
    for string in result:
        print(f'{string[0][0]}:{string[0][1]}')
```
![Картинка 4](./images/lab03/B.png)

## Лабораторная работа 2
# Задание 1
# min_max
```python
arr1 = [3, -1, 5, 5, 0]
arr2 = [42]
arr3 = [-5, -2, -9]
arr4 = [1.5, 2, 2.0, -3.1]
arr5=[]
def min_max(nums: list[float | int]):
    n =[a for a in nums]
    if len(n)!=0:
        return min(n),max(n)
    if len(n)==0:
        raise ValueError
print(min_max(arr1))
print(min_max(arr2))
print(min_max(arr3))
print(min_max(arr4))
#print(min_max(arr5))
```
# unique_sorted
```python
def unique_sorted(nums: list[float | int]):
    a=sorted(set(x for x in nums))
    return a
arr3=[1.0,1,2.5,2.5,0]
arr2=[-1,-1,0,2,2]
arr1=[3,1,2,1,3]

print(f(arr1),f(arr2),f(arr3))
```
# flatten
```python
array1 = [[1, 2], [3, 4]]
array2 = [[1, 2], (3, 4, 5)]
array3 = [[1], [], [2, 3]]
array4=[[1, 2], "ab"]
def flatten(mat: list[list | tuple]):
    answer = []
    for n in mat:
        if isinstance(n,list) or isinstance(n,tuple):
            for y in n:
                answer += [y]
        else:
            raise TypeError
    return answer
print(flatten(array1))
print(flatten(array2))
print(flatten(array3))
print(flatten(array4))
```
![Картинка 1](./images/lab02/01lab2.png)

# Задание 2

# transpose
```python
def transpose(mat: list[list[float | int]]):
    res=[list(x) for x in zip(*mat)]
    for row in mat:
        if len(mat[0])!=len(row):
            raise ValueError
    return res
array1=[[1,2,3]]
array2=[[1],[2],[3]]
array3=[[1,2],[3,4]]
array4=[]
array5=[[1, 2], [3]]
print(transpote(array1))
print(transpote(array2))
print(transpote(array3))
print(transpote(array4))
print(transpote(array5))

```
# row_sums
```python

array1=[[1,2,3],[4,5,6]]
array2=[[-1,1],[10,-10]]
array3=[[0, 0], [0, 0]]
array4=[[1, 2], [3]]
def row_sums(mat: list[list[float | int]]):
    res=[sum(x) for x in mat]
    for row in mat:
        if len(mat[0])!=len(row):
            raise ValueError
    return res
print(row_sums(array1))
print(row_sums(array2))
print(row_sums(array3))
print(row_sums(array4))
```
# col_sums
```python
array1=[[1,2,3],[4,5,6]]
array2=[[-1,1],[10,-10]]
array3=[[0,0],[0,0]]
array4=[[1, 2], [3]]
def col_sums(mat: list[list[float | int]]):
    res=[sum(x) for x in zip(*mat)]
    for row in mat:
        if len(mat[0])!=len(row):
            raise ValueError
    return res
print(col_sums(array1))
print(col_sums(array2))
print(col_sums(array3))
print(col_sums(array4))
```
![Картинка 2](./images/lab02/B.png)

# Задание 3
```python
format_record(records: tuple[str, str, float]) -> str
    result=[]
    for rec in records:
        fio,group,gpa = rec
        cleaned_fio=[' '.join(fio.strip().split()),group,gpa]
        if len(cleaned_fio[0].split())>=3:
            name=cleaned_fio[0].split()[1][0].title()+'.'
            otch=cleaned_fio[0].split()[2][0].title()+'.'
            famil=cleaned_fio[0].split()[0].title()
            form = f'{famil} {name}{otch}'
            form_res=f'{form}, гр. {cleaned_fio[1]}, GPA {gpa:.2f}'
            result+=[form_res]
        if len(cleaned_fio[0].split())<=2:
            name=cleaned_fio[0].split()[1][0].title()+'.'
            famil=cleaned_fio[0].split()[0].title()
            form=f'{famil} {name}'
            form_res=f'{form}, гр. {cleaned_fio[1]}, GPA {gpa:.2f}'
            result+=[form_res]
    return result
test_cases = [
    ("Иванов Иван Иванович", "BIVT-25", 4.6),
    ("Петров Пётр", "IKBO-12", 5.0),
    ("  cидорова  анна   сергеевна ", "ABB-01", 3.999)
]
print(format_records(test_cases))
```
![Картинка 3](./images/lab02/Clab.png)

# Лабораторная работа 1


## Задание 1
```python
name=str(input('Введите имя:'))
age=int(input('Введите возраст:'))
print('Привет, ', f'{name}''!' ' Через год тебе будет ' f'{age+1}''.')
```
![Картинка 1](./images/lab01/01.png)

## Задание 2
```python
first_num=float(input().replace(',','.'))
second_num=float(input().replace(',','.'))
sum=first_num+second_num
avg=(first_num+second_num)/2
print(sum,round(avg,2))
```
![Картинка 2](./images/lab01/02.png)

## Задание 3
```python
price=float(input())
discount=float(input())
vat=float(input())
base=price*(1-discount/100)
vat_amount=base*(vat/100)
total = base+vat_amount
print('База после скидки: 'f'{base:.2f}'' ₽', 'НДС: 'f'{vat_amount:.2f}'' ₽', 'Итого к оплате: 'f'{total:.2f}'' ₽',sep='\n')
```
![Картинка 3](./images/lab01/03.png)

## Задание 4
```python
minutes=int(input())
count=0
hours=(minutes-minutes%60)//60
resmin=minutes%60
result=f'{str(hours)}' + ':' + f'{str(resmin)}'
print(result)
```
```python
m = int(input().strip())
hours = m // 60
minutes = m % 60
print(f"{hours}:{minutes:02d}")
```
![Картинка 4](./images/lab01/04.png)
![Картинка 4](./images/lab01/044.png)

## Задание 5
```python
fio=str(input())
res=''
for i in range(len(fio)-1):
    if fio[i-1]==' ' and fio[i] in 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
        res+=str(fio[i])
k=2
for j in fio:
    if j!=' ':
        k+=1
print(res+'.',k)
```
![Картинка 5](./images/lab01/05.png)
```python
name = str(input('ФИО: '))
abc1='ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'
l=0
count=0
letters=[]
m=-10**10
for r in range(len(name)):
    if name[r] in abc1:
        count+=1
        letters+=[name[r]]
        while count>3:
            if name[l] in abc1:
                count-=1
            l+=1
    m=max(m,r-l+1)
print(m,*letters,end='.')
```

## Задание 6
```python
n = int(input())
offline_count = 0
online_count = 0
for i in range(n):
    sub = input().split()
    if sub[-1] == 'True':online_count += 1
    else:offline_count += 1
print(online_count,offline_count)
```
![Картинка 6](./images/lab01/06.png)

## Задание 7
```python
from string import *
sub='thisisabracadabraHt1eadljjl12ojh.'
abc1=ascii_uppercase
abc2=ascii_lowercase
count_first_letter=0
result=''
count_second_letter =0 
ind1=-1
ind2=-1
trueresult=''

for i in range(len(sub)-1):
    if sub[i] in ascii_uppercase:
        count_first_letter+=1
    if sub[i] in ascii_uppercase and count_first_letter==1:
        result+=sub[i]
        ind1=i
    if sub[i] in '0123456789' and sub[i+1] in abc2 :
        count_second_letter+=1
    if count_second_letter==1 and sub[i] in '0123456789' and sub[i+1] in abc2 :
        ind2=i+1
        result+=sub[i+1]
for i in range(ind1,len(sub),ind2-ind1):
    trueresult+=sub[i]
print(trueresult)
```
![Картинка 7](./images/lab01/07.png)
