import pytest
from lib.text import normalize
from lib.text import tokenize
from lib.text import count_freq
from lib.text import top_n


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Привет, Мир!", "привет мир"),
        (" Ёлка-ёлка ", "елка-елка"),
        ("", ""),
        ("Hello World 123", "hello world 123"),
        ("!@!###!", ""),
        ("e-mail адрес", "e-mail адрес"),
    ],
)
def test_normalize(text, expected):
    assert normalize(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Привет, Мир!", ["Привет", "Мир"]),
        ("Hello World", ["Hello", "World"]),
        ("", []),
        ("!!!@@@###", []),
        ("e-mail адрес", ["e-mail", "адрес"]),
        ("123 456", ["123", "456"]),
        ("word1 word2 word1", ["word1", "word2", "word1"]),
    ],
)
def test_tokenize(text, expected):
    assert tokenize(text) == expected


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["кот", "кот", "пёс"], [("кот", 2), ("пёс", 1)]),
        (["a", "b", "c"], [("a", 1), ("b", 1), ("c", 1)]),
        ([], []),
        (["word", "word", "word"], [("word", 3)]),
        (["a", "a", "b", "b", "c"], [("a", 2), ("b", 2), ("c", 1)]),
    ],
)
def test_count_freq(tokens, expected):
    result = count_freq(tokens)
    assert result == expected


@pytest.mark.parametrize(
    "freq, n, expected",
    [
        ({"кот": 5, "пёс": 3, "мышь": 1}, 2, [("кот", 5), ("пёс", 3)]),
        ({"banana": 2, "apple": 2, "cherry": 1}, 2, [("apple", 2), ("banana", 2)]),
        ({"яблоко": 3, "банан": 3, "вишня": 2}, 2, [("банан", 3), ("яблоко", 3)]),
        ({"a": 1, "b": 2}, 0, []),
        ({"a": 1, "b": 2}, -1, []),
        ({"a": 1, "b": 2}, 10, [("b", 2), ("a", 1)]),
        ({}, 5, []),
    ],
)
def test_top_n(freq, n, expected):
    assert top_n(freq, n) == expected


def test_top_n_same_frequency_alphabetical():
    freq = {"zebra": 2, "apple": 2, "banana": 2}
    result = top_n(freq, 3)
    assert result == [("apple", 2), ("banana", 2), ("zebra", 2)]
