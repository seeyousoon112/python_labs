

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

