import pytest
import json
import csv
from pathlib import Path
from lib.converters import json_to_csv, csv_to_json

DATA_DIR = Path(__file__).parent.parent / "data" / "samples"
SAMPLE_JSON_PATH = DATA_DIR / "people.json"
SAMPLE_CSV_PATH = DATA_DIR / "people.csv"


class TestJsonToCsv:
    def test_json_to_csv_success(self, tmp_path):

        json_path = SAMPLE_JSON_PATH
        csv_path = tmp_path / "output.csv"

        json_to_csv(str(json_path), str(csv_path))

        assert csv_path.exists()

        with open(json_path, "r", encoding="utf-8") as f:
            original_data = json.load(f)

        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == len(original_data)

        expected_keys = {"name", "age", "city"}
        assert set(rows[0].keys()) == expected_keys

        assert rows[0]["name"] == original_data[0]["name"]
        assert rows[0]["age"] == original_data[0]["age"]
        assert rows[0]["city"] == original_data[0]["city"]

    def test_json_to_csv_file_not_found(self, tmp_path):
        json_path = tmp_path / "nonexistent.json"
        csv_path = tmp_path / "output.csv"

        with pytest.raises(FileNotFoundError, match="JSON файл не найден"):
            json_to_csv(str(json_path), str(csv_path))

    def test_json_to_csv_wrong_extension(self, tmp_path):
        json_path = tmp_path / "test.txt"  # не .json
        csv_path = tmp_path / "output.csv"

        json_path.write_text("{}", encoding="utf-8")

        with pytest.raises(ValueError, match="Проверьте расширение файла"):
            json_to_csv(str(json_path), str(csv_path))

    def test_json_to_csv_empty_file(self, tmp_path):
        json_path = tmp_path / "empty.json"
        csv_path = tmp_path / "output.csv"

        json_path.write_text("", encoding="utf-8")

        with pytest.raises(ValueError):
            json_to_csv(str(json_path), str(csv_path))

    def test_json_to_csv_invalid_json(self, tmp_path):
        json_path = tmp_path / "invalid.json"
        csv_path = tmp_path / "output.csv"

        json_path.write_text("{invalid json}", encoding="utf-8")

        with pytest.raises((ValueError, json.JSONDecodeError)):
            json_to_csv(str(json_path), str(csv_path))


class TestCsvToJson:

    def test_csv_to_json_success(self, tmp_path):

        csv_path = SAMPLE_CSV_PATH
        json_path = tmp_path / "output.json"

        csv_to_json(str(csv_path), str(json_path))

        assert json_path.exists()

        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            csv_reader = csv.DictReader(f)
            original_rows = list(csv_reader)

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == len(original_rows)

        expected_keys = {"name", "age", "city"}
        assert set(data[0].keys()) == expected_keys

        assert data[0]["name"] == original_rows[0]["name"]
        assert data[0]["age"] == original_rows[0]["age"]
        assert data[0]["city"] == original_rows[0]["city"]

    def test_csv_to_json_file_not_found(self, tmp_path):
        csv_path = tmp_path / "noneexist.csv"
        json_path = tmp_path / "output.json"

        with pytest.raises(FileNotFoundError):
            csv_to_json(str(csv_path), str(json_path))

    def test_csv_to_json_wrong_extension(self, tmp_path):
        csv_path = tmp_path / "test.txt"  # не .csv
        json_path = tmp_path / "output.json"

        csv_path.write_text("name,age\nAlice,22", encoding="utf-8")

        with pytest.raises(ValueError, match="Проверьте расширение файла"):
            csv_to_json(str(csv_path), str(json_path))

    def test_csv_to_json_empty_file(self, tmp_path):
        """Негативный: пустой CSV файл → ValueError"""
        csv_path = tmp_path / "empty.csv"
        json_path = tmp_path / "output.json"

        csv_path.write_text("", encoding="utf-8")

        with pytest.raises(ValueError, match="В csv файле нет данных"):
            csv_to_json(str(csv_path), str(json_path))


class RoundTrip:
    # туда сюда

    def test_json_to_csv_to_json(self, tmp_path):
        json1_path = SAMPLE_JSON_PATH
        csv_path = tmp_path / "inter.csv"
        json2_path = tmp_path / "final.json"

        # JSON → CSV
        json_to_csv(str(json1_path), str(csv_path))

        # CSV → JSON
        csv_to_json(str(csv_path), str(json2_path))

        with open(json1_path, "r", encoding="utf-8") as f:
            original_data = json.load(f)

        with open(json2_path, "r", encoding="utf-8") as f:
            final_data = json.load(f)

        assert len(original_data) == len(final_data)

        assert original_data == final_data

    def test_csv_to_json_to_csv(self, tmp_path):
        csv1_path = SAMPLE_CSV_PATH
        json_path = tmp_path / "intermediate.json"
        csv2_path = tmp_path / "final.csv"

        csv_to_json(str(csv1_path), str(json_path))

        json_to_csv(str(json_path), str(csv2_path))

        with open(csv1_path, "r", encoding="utf-8", newline="") as f:
            reader1 = csv.DictReader(f)
            original_rows = list(reader1)

        with open(csv2_path, "r", encoding="utf-8", newline="") as f:
            reader2 = csv.DictReader(f)
            final_rows = list(reader2)

        assert len(original_rows) == len(final_rows)

        assert original_rows == final_rows
