class Vacancy:
    """
    Класс для представления вакансии.
    """
    def __init__(self, title, company, salary, description, link):
        self.title = title
        self.company = company
        self.salary = salary
        self.description = description
        self.link = link

    def __repr__(self):
        """
        Возвращает строковое представление объекта Vacancy.
        """
        return f"Vacancy(title={self.title}, company={self.company}, salary={self.salary}, description={self.description}, link={self.link})"

    @staticmethod
    def cast_to_object_list(vacancies):
        """
        Конвертирует список словарей в список объектов Vacancy.
        """
        return [Vacancy(**vacancy) for vacancy in vacancies]

    def __lt__(self, other):
        """
        Сравниваем две вакансии по зарплате.
        """
        return self._parse_salary(self.salary) < self._parse_salary(other.salary)

    def __eq__(self, other):
        """
        Проверяем равенство двух вакансий по зарплате.
        """
        return self._parse_salary(self.salary) == self._parse_salary(other.salary)

    @staticmethod
    def _parse_salary(salary):
        """
        Парсим строку зарплаты в целочисленное значение.
        """
        if not salary:
            return 0
        if isinstance(salary, dict):
            return salary.get('from', 0)
        if ' - ' in salary:
            salary = salary.split(' - ')[0]
        salary = salary.split()[0]
        try:
            return int(salary.replace('руб.', '').replace(' ', ''))
        except ValueError:
            return 0

    def to_dict(self):
        """
        Конвертируем объект Vacancy в словарь.
        """
        return {
            'title': self.title,
            'company': self.company,
            'salary': self.salary,
            'description': self.description,
            'link': self.link
        }


from src.Abstract_class_and_API import HeadHunterAPI


def fetch_and_save_vacancies(file_path, query):
    """
    Получаем вакансии с HeadHunter и сохраняет их в файл.
    """
    api = HeadHunterAPI()

    from src.JSONVacancyStorage import JSONVacancyStorage  # Локальный импорт для избежания циклической зависимости
    storage = JSONVacancyStorage(file_path)

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
        if not link or 'Error' in link:
            link = 'Invalid link'
        vacancies.append(Vacancy(title, company, salary_str, description, link))

    # Сохраняем объекты Vacancy, добавляя их к существующим данным
    storage.append([vacancy.to_dict() for vacancy in vacancies])
    return vacancies


def get_top_vacancies_by_salary(vacancies, top_n):
    """
    Возвращаем топ N вакансий по зарплате.
    """
    return sorted(vacancies, reverse=True)[:top_n]


def search_vacancies_by_keyword(file_path, keyword):
    """
    Ищем вакансии по ключевому слову.
    """
    from src.JSONVacancyStorage import JSONVacancyStorage  # Локальный импорт для избежания циклической зависимости
    storage = JSONVacancyStorage(file_path)
    return storage.find_vacancies_with_keyword(keyword)
