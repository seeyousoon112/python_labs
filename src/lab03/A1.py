def normalize(text: str, *, casefold: bool = True, yo2e: bool = True):
    text=text.replace('ё','е').replace('Ё','Е')
    text=text.replace('\t',' ').replace('\r',' ').replace('\n',' ')
    text=text.split()
    new_text=' '.join(text)
    return new_text.strip().lower()
test1="ПрИвЕт\nМИр\t"
test2="ёжик, Ёлка"
test3="Hello\r\nWorld"
test4="  двойные   пробелы  "
print(normalize(test1),normalize(test2),normalize(test3),normalize(test4),sep='\n')

