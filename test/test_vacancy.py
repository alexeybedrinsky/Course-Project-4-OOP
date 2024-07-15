import pytest
from src.Vacancy import Vacancy

# Тестирование инициализации объекта Vacancy
def test_vacancy_initialization():
    vacancy = Vacancy("Python Developer", "Some Company", "100000 - 150000 руб.", "Job description", "http://example.com")
    assert vacancy.title == "Python Developer"
    assert vacancy.company == "Some Company"
    assert vacancy.salary == "100000 - 150000 руб."
    assert vacancy.description == "Job description"
    assert vacancy.link == "http://example.com"

# Тестирование метода _parse_salary
def test_parse_salary():
    vacancy = Vacancy("Python Developer", "Some Company", "100000 - 150000 руб.", "Job description", "http://example.com")
    assert vacancy._parse_salary("100000 - 150000 руб.") == 100000
    assert vacancy._parse_salary({"from": 100000, "to": 150000}) == 100000
    assert vacancy._parse_salary("Not a salary") == 0
    assert vacancy._parse_salary(None) == 0

# Тестирование метода cast_to_object_list
def test_cast_to_object_list():
    vacancies_data = [
        {
            "title": "Python Developer",
            "company": "Some Company",
            "salary": "100000 - 150000 руб.",
            "description": "Job description",
            "link": "http://example.com"
        },
        {
            "title": "Java Developer",
            "company": "Another Company",
            "salary": "120000 - 180000 руб.",
            "description": "Job description",
            "link": "http://example.com"
        }
    ]
    vacancies = Vacancy.cast_to_object_list(vacancies_data)
    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Python Developer"
    assert vacancies[1].title == "Java Developer"

# Тестирование операторов сравнения
def test_comparison_operators():
    vacancy1 = Vacancy("Python Developer", "Some Company", "100000 - 150000 руб.", "Job description", "http://example.com")
    vacancy2 = Vacancy("Java Developer", "Another Company", "120000 - 180000 руб.", "Job description", "http://example.com")
    vacancy3 = Vacancy("C++ Developer", "Yet Another Company", "100000 - 150000 руб.", "Job description", "http://example.com")

    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert vacancy1 == vacancy3
    assert vacancy1 != vacancy2

if __name__ == "__main__":
    pytest.main()
