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