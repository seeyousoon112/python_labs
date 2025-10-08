
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
