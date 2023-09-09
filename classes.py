import psycopg2

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="headhunter",
            user="postgres",
            password="dasha888"
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании
        """
        self.cur.execute("SELECT COUNT(*), companies.company_name FROM vacancies "
                         "INNER JOIN companies USING (company_id) "
                         "GROUP BY companies.company_name")
        result = self.cur.fetchall()

        return result

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        self.cur.execute("SELECT companies.company_name, vacancy_name, vacancies.url, salary_to, salary_from, currency FROM vacancies "
                         "INNER JOIN companies USING (company_id)")
        result = self.cur.fetchall()

        return result

    def get_avg_salary(self):
        """
       получает среднюю зарплату по вакансиям
        """
        self.cur.execute("SELECT AVG(salary_from - salary_to) FROM vacancies")
        result = self.cur.fetchall()

        return result

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        self.cur.execute("SELECT * FROM vacancies "
                         "WHERE salary_from > (SELECT AVG(salary_to - salary_from) FROM vacancies)")
        result = self.cur.fetchall()

        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        self.cur.execute(f"SELECT * FROM vacancies "
                         f"WHERE vacancy_name LIKE '%{keyword}%'")
        result = self.cur.fetchall()

        return result

