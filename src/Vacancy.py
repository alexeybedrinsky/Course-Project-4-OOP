class Vacancy:
    def __init__(self, title, company, salary, description, link):
        self.title = title
        self.company = company
        self.salary = salary
        self.description = description
        self.link = link

    def _parse_salary(self, salary):
        if isinstance(salary, str):
            parts = salary.split('-')
            if len(parts) == 2:
                return int(parts[0].strip().split()[0].replace('руб.', '').replace(' ', ''))
        elif isinstance(salary, dict):
            return salary.get('from', 0)
        return 0

    def __repr__(self):
        return f"Vacancy(title={self.title}, company={self.company}, salary={self.salary}, description={self.description}, link={self.link})"

    @staticmethod
    def cast_to_object_list(vacancies):
        return [Vacancy(**vacancy) for vacancy in vacancies]

    def __lt__(self, other):
        return self._parse_salary(self.salary) < self._parse_salary(other.salary)

    def __eq__(self, other):
        return self._parse_salary(self.salary) == self._parse_salary(other.salary)

    @staticmethod
    def _parse_salary(salary):
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
