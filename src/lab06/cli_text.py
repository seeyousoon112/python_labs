import argparse
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



