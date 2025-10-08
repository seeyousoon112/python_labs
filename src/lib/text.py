from re import *
def tokenize(text):
    pattern = (r'[a-zA-Zа-яА-ЯёЁ0-9]+([-][a-zA-Zа-яА-ЯёЁ0-9]+)*')
    tokens = []
    for match in finditer(pattern,text):
        tokens.append(match.group())
    return tokens

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True):
    if casefold:text=text.casefold()
    if yo2e:
        text=text.replace('ё','е').replace('Ё','Е')
    text=text.replace('\t',' ').replace('\r',' ').replace('\n',' ').replace('\\',' ').replace('\'',' ').replace('\"',' ').replace('\a',' ').replace('\b',' ').replace('\f',' ').replace('\v',' ')
    text=text.split()
    new_text=' '.join(text)
    return new_text.strip()

def count_freq(tokens: list[str]):
    d={x:tokens.count(x) for x in set(tokens)}
    return sorted(d.items(),key=lambda x:-x[1])

from collections import * 

def frequencies_from_text(text: str) -> dict[str, int]:
    tokens=tokenize(normalize(text))
    return Counter(tokens)

def sorted_word_counts(freq: dict[str, int]) -> list[tuple[str, int]]:
    return sorted(freq.items(),key=lambda x: (-x[1],x[0]))
