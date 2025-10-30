from pathlib import Path
import csv
def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    print(f"Читаю файл: {path}") 
    p = Path(path)
    text = p.read_text(encoding=encoding)
    if encoding!='utf-8':
        raise UnicodeDecodeError('Проверьте кодировку')
    if p.suffix.lower()!='.csv':
        raise ValueError('Файл должен иметь расширение .csv, получено')
    
    print(f"Прочитал {len(text)} символов")
    return text

def write_csv(rows: list[tuple | list], path: str | Path, 
              header: tuple[str, ...] | None = None,check_csv:bool=False) -> None:
    p = Path(path)
    if p.suffix.lower()!='.csv':
        raise ValueError(f'Файл должен иметь расширение .csv, получено: {p.suffix}')

    if rows:
        first_length = len(rows[0])
        for i, row in enumerate(rows):
            if len(row) != first_length:
                raise ValueError(f"ошибка лютая")
    with p.open('w',newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        if header is not None:
            writer.writerow(header)
        
        for row in rows:
            writer.writerow(row)
            