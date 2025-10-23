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

import json
import csv
from pathlib import Path

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














 