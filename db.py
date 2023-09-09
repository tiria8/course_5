from typing import Any

import psycopg2
import requests

emp_id = ['2180', '3529', '2460946', '15478', '1740', '1455', '84585', '1616587', '4721563', '218800']


def get_hh_data(employer_ids):
    """Получение данных о работодателях и их вакансиях с сайта hh.ru"""

    data = []
    vacancies = []
    companies = []
    for employer_id in employer_ids:
        vacancies_request = requests.get(f'https://api.hh.ru/vacancies?employer_id={employer_id}')
        vacancies_data = vacancies_request.json()["items"]

        for vacancy in vacancies_data:
            vacancies.append({
                'title': vacancy['name'],
                'url': vacancy['url'],
                'salary_from': vacancy["salary"]["from"] if vacancy["salary"] and vacancy["salary"]["from"] is not None else 0,
                'salary_to': vacancy["salary"]["to"] if vacancy["salary"] and vacancy["salary"]["to"] is not None else 0,
                'currency': vacancy["salary"]["currency"] if vacancy["salary"] and vacancy["salary"]["currency"] else 'null',
                'company_id': vacancy['employer']['id']
            })

        company_request = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        company_data = company_request.json()

        companies.append({
            'company_id': company_data['id'],
            'title': company_data['name'],
            'description': company_data['description'],
            'url': company_data['alternate_url'],
        })

        data.append({
            'vacancies': vacancies,
            'companies': companies
        })

    return data


def create_database(database_name: str):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', user="postgres", password="dasha888", host="localhost")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, user="postgres", password="dasha888", host="localhost")

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id varchar(20) PRIMARY KEY UNIQUE NOT NULL,
                company_name VARCHAR(255),
                description text,
                url VARCHAR(255)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
           CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255),
                url VARCHAR(255),
                salary_from int,
                salary_to int,
                currency varchar(5),
                company_id varchar(20)
           );

           ALTER TABLE vacancies add constraint fk_company 
           foreign key (company_id) 
           references companies (company_id)
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data, database_name: str):
    """Сохранение данных о компаниях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, user="postgres", password="dasha888", host="localhost")

    with conn.cursor() as cur:
        for company in data[0]['companies']:
            cur.execute(
                """
                INSERT INTO companies (company_id, company_name, description, url)
                VALUES (%s, %s, %s, %s)
                """,
                (company['company_id'], company['title'], company['description'], company['url'])
            )

        for vacancy in data[0]['vacancies']:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_name, url, salary_from, salary_to, currency, company_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (vacancy['title'], vacancy['url'], vacancy['salary_from'],
                 vacancy['salary_to'], vacancy['currency'], vacancy['company_id'])
            )

    conn.commit()
    conn.close()
