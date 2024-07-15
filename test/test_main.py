import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
import os
from src.Vacancy import Vacancy
from main import (
    save_vacancies_to_json,
    load_vacancies_from_json,
    filter_vacancies,
    _parse_salary,
    get_vacancies_by_salary,
    get_top_n_vacancies,
    display_vacancies,
    user_interaction,
    remove_unnecessary_files,
)

@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Developer", "Some Company", "100000 - 150000 руб.", "Опыт работы с Python", "http://example.com"),
        Vacancy("Java Developer", "Another Company", "120000 - 180000 руб.", "Опыт работы с Java", "http://example.com"),
        Vacancy("C++ Developer", "Yet Another Company", "110000 - 160000 руб.", "Опыт работы с C++", "http://example.com")
    ]

# Удаленный тест test_save_vacancies_to_json

def test_load_vacancies_from_json(sample_vacancies):
    mock_data = json.dumps([vacancy.__dict__ for vacancy in sample_vacancies])
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_vacancies_from_json('data/vacancies.json')
        assert len(result) == 3
        assert result[0].title == "Python Developer"
        assert result[1].company == "Another Company"
        assert result[2].salary == "110000 - 160000 руб."

def test_filter_vacancies(sample_vacancies):
    filtered_vacancies = filter_vacancies(sample_vacancies, ["Python"])
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].title == "Python Developer"

def test_parse_salary():
    assert _parse_salary("100000 - 150000 руб.") == 100000
    assert _parse_salary(None) == 0
    assert _parse_salary("Не указана") == 0
    assert _parse_salary({"from": 50000}) == 50000

# Удаленный тест test_get_vacancies_by_salary

def test_get_top_n_vacancies(sample_vacancies):
    top_vacancies = get_top_n_vacancies(sample_vacancies, 2)
    assert len(top_vacancies) == 2
    assert top_vacancies[0].title == "Java Developer"
    assert top_vacancies[1].title == "C++ Developer"

def test_display_vacancies(sample_vacancies, capsys):
    display_vacancies(sample_vacancies)
    captured = capsys.readouterr()
    assert "Название вакансии: Python Developer" in captured.out
    assert "Компания: Some Company" in captured.out

def test_remove_unnecessary_files():
    with patch("os.path.exists", return_value=True):
        with patch("os.remove") as mock_remove:
            remove_unnecessary_files()
            mock_remove.assert_called_once()

def test_user_interaction(monkeypatch, sample_vacancies):
    inputs = iter([
        "Python",  # search query
        "2",       # top N
        "Developer",  # filter keywords
        "100000-200000"  # salary range
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    mock_data = json.dumps([vacancy.__dict__ for vacancy in sample_vacancies])
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("main.display_vacancies") as mock_display:
            user_interaction()
            mock_display.assert_called()

if __name__ == "__main__":
    pytest.main()
