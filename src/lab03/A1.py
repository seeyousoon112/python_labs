import re


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True):
    if casefold:
        text = text.casefold()
    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")
    pattern = r"[a-zA-Zа-яА-ЯёЁ0-9]+([-][a-zA-Zа-яА-ЯёЁ0-9]+)*"
    normalized = []
    for match in re.finditer(pattern, text):
        normalized.append(match.group())
    return " ".join(normalized).strip()


test_cases = ["ПрИвЕт\nМИр\t", "ёжик, Ёлка", "Hello\r\nWorld", "  двойные   пробелы  "]
for test in test_cases:
    result = normalize(test)
    print(result)
