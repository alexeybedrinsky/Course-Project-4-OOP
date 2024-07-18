from Abstract_class_and_API import HeadHunterAPI
from Vacancy import Vacancy
from JSONVacancyStorage import JSONVacancyStorage

def interact_with_user(file_path):
    """
    Функция для интерактивного взаимодействия с юзером.
    Позволяет юзеру выполнить следующие действия:
    1. Запросить вакансии с hh по поисковому запросу.
    2. Вывести топ N вакансий по зарплате.
    3. Найти вакансии по ключслову в описании.
    """
    api = HeadHunterAPI()
    storage = JSONVacancyStorage(file_path)

    query = input("Введите поисковый запрос для запроса вакансий с hh.ru: ")
    vacancies_data = api.get_vacancies(query, per_page=100)  # Загрузка 100 вакансий

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
        if not link or 'Произошла ошибка' in link:
            link = 'Некорректная ссылка'
        vacancies.append(Vacancy(title, company, salary_str, description, link))

    # Сохраняем объекты Vacancy, добавляя их к существующим данным
    storage.append([vacancy.to_dict() for vacancy in vacancies])

    try:
        top_n = int(input("Введите количество вакансий для вывода топ N по зарплате: "))
    except ValueError:
        print("Ошибка: введите числовое значение.")
        return

    sorted_vacancies = sorted(vacancies, reverse=True)[:top_n]
    print(f"Топ {top_n} вакансий по зарплате:")
    for vacancy in sorted_vacancies:
        print(vacancy)

    keyword = input("Введите ключевое слово для поиска вакансий по описанию: ")
    matching_vacancies = storage.find_vacancies_with_keyword(keyword)
    print(f"Вакансии с ключевым словом '{keyword}' в описании:")
    for vacancy in matching_vacancies:
        print(vacancy)

if __name__ == "__main__":
    file_path = "vacancies.json"
    interact_with_user(file_path)
