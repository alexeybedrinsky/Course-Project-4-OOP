import os
import json
from src.JSONVacancyStorage import JSONVacancyStorage
from src.Vacancy import Vacancy
from src.Abstract_class_and_API import HeadHunterAPI

def save_vacancies_to_json(vacancies, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump([vacancy.__dict__ for vacancy in vacancies], file, ensure_ascii=False, indent=4)

def load_vacancies_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [Vacancy(**data) for data in json.load(file)]

def filter_vacancies(vacancies, filter_words):
    filtered_vacancies = [vacancy for vacancy in vacancies if
                          any(word.lower() in (vacancy.description or '').lower() for word in filter_words)]
    print(f"Отобрано {len(filtered_vacancies)} вакансий по ключевым словам {filter_words}")
    return filtered_vacancies

def _parse_salary(salary):
    if not salary or salary == 'Не указана' or 'None' in salary:
        return 0
    if isinstance(salary, str):
        parts = salary.split('-')
        if len(parts) == 2:
            try:
                return int(parts[0].strip())
            except ValueError:
                return 0
    elif isinstance(salary, dict):
        return salary.get('from', 0)
    return 0

def get_vacancies_by_salary(vacancies, salary_range):
    if not salary_range:
        return vacancies
    min_salary, max_salary = map(int, salary_range.replace(' ', '').split('-'))
    filtered_vacancies = []
    for vacancy in vacancies:
        vacancy_salary = _parse_salary(vacancy.salary)
        print(f"Вакансия: {vacancy.title}, Зарплата: {vacancy.salary}, Зарплатное ожидание: {vacancy_salary}")
        if min_salary <= vacancy_salary <= max_salary:
            filtered_vacancies.append(vacancy)
    print(f"Отобрано {len(filtered_vacancies)} вакансий с зарплатной вилкой {salary_range}")
    return filtered_vacancies

def get_top_n_vacancies(vacancies, n):
    sorted_vacancies = sorted(vacancies, key=lambda x: _parse_salary(x.salary) if x.salary else 0, reverse=True)
    top_vacancies = sorted_vacancies[:n]
    print(f"Отобрано топ {n} вакансий")
    return top_vacancies

def display_vacancies(vacancies):
    if not vacancies:
        print("Нет вакансий для показа.")
        return
    for vacancy in vacancies:
        print(f"Название вакансии: {vacancy.title}")
        print(f"Компания: {vacancy.company}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Описание: {vacancy.description}")
        print(f"Ссылка: {vacancy.link}")
        print("=" * 40)

def user_interaction():
    # Обновляем путь к файлу
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'vacancies.json')
    # Закомментированы строки отладочной информации
    # print(f"Текущая рабочая директория: {os.getcwd()}")
    # print(f"Ожидаемый путь к файлу JSON: {json_path}")

    vacancies_list = load_vacancies_from_json(json_path)
    print(f"Загружено {len(vacancies_list)} вакансий из JSON файла.")

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_keywords = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат (например, 50000-100000): ")

    filtered_vacancies = filter_vacancies(vacancies_list, filter_keywords)
    filtered_by_salary = get_vacancies_by_salary(filtered_vacancies, salary_range)
    top_vacancies = get_top_n_vacancies(filtered_by_salary, top_n)

    display_vacancies(top_vacancies)

def remove_unnecessary_files():
    src_vacancies_path = os.path.join(os.path.dirname(__file__), 'src', 'vacancies.json')
    if os.path.exists(src_vacancies_path):
        os.remove(src_vacancies_path)
        print(f"Removed unnecessary file: {src_vacancies_path}")

if __name__ == "__main__":
    remove_unnecessary_files()  # Удаляем ненужный файл

    api = HeadHunterAPI()
    search_query = input("Введите поисковый запрос для загрузки вакансий с hh.ru: ")
    vacancies_data = api.get_vacancies(search_query, per_page=100)

    vacancies = []
    for vacancy in vacancies_data:
        title = vacancy.get('name')
        company = vacancy.get('employer', {}).get('name', '')
        salary = vacancy.get('salary', {})
        if salary:
            salary_from = salary.get('from', 0)
            salary_to = salary.get('to', 0)
            currency = salary.get('currency', '')
            salary_str = f"{salary_from} - {salary_to} {currency}".strip()
        else:
            salary_str = 'Не указана'
        description = vacancy.get('snippet', {}).get('requirement', '')
        link = vacancy.get('alternate_url')
        if not link or 'Error' in link:
            link = 'Invalid link'
        vacancies.append(Vacancy(title, company, salary_str, description, link))

    json_path = os.path.join(os.path.dirname(__file__), 'data', 'vacancies.json')
    save_vacancies_to_json(vacancies, json_path)

    user_interaction()
