# Проект по БД. Курсовая работа

Проект позволяет получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.
С API hh.ru можно ознакомиться по ссылке: https://api.hh.ru/openapi/redoc.
Для подключения к БД используется библиотека `psycopg2`.

### В файле `db.py` содержатся следующие функции:

- get_hh_data() - получение данных о работодателях и их вакансиях с сайта hh.ru
- create_database() - создание базы данных и таблиц для сохранения данных о компаниях и вакансиях
- save_data_to_database() - сохранение данных о компаниях и вакансиях в базу данных

### В файле `classes.py` содержится класс DBManager со следующими методами:

- get_companies_and_vacancies_count() — получает список всех компаний и количество вакансий у каждой компании.
- get_all_vacancies() — получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
- get_avg_salary() — получает среднюю зарплату по вакансиям.
- get_vacancies_with_higher_salary() — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
- get_vacancies_with_keyword() — получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.

### Скрипт в файле `main.py`:

- получает данные с платформы hh.ru
- сохраняет полученные данные в БД
- содержит функцию 'main()' для взаимодействия с пользователем и вывода данных в зависимости от набранной команды


