import json
import csv
from pathlib import Path
import sys
current_file = Path(__file__)
print(f"Текущий файл: {current_file}")

parent_dir = current_file.parent.parent
sys.path.append(str(parent_dir))

def csv_to_json(csv_path: str, json_path: str) -> None:
    input_file='src/data/people.csv'
    output_file='src/data/people.json'
    encoding='utf-8'


 