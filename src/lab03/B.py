import sys
from lib import text

table_mode = True
stroka = sys.stdin.readline()
tokenized = text.tokenize(stroka)
unique_words = text.count_freq(tokenized)
result = text.count_freq(unique_words)
top_words = result[:5]
if table_mode:
    max_word_ln = max(len(str(word[0][0])) for word in top_words)
    max_width = max(max_word_ln, 5)
    print(f"\nТоп-5:")
    print(f"| {'слово':{max_width}} | {'частота'} |")
    print(f"|{'-' * (max_width + 2)}|---------|")
    for word_row in top_words:
        word = word_row[0][0]
        gusi = word_row[0][1]
        print(f"| {word:{max_width}} | {gusi:<7} |")
else:
    print(f"Топ-{5}:")
    for string in result:
        print(f"{string[0][0]}:{string[0][1]}")
