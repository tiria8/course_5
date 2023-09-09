from db import get_hh_data, create_database, save_data_to_database
from classes import DBManager

def main():
    emp_id = ['2180', '3529', '2460946', '15478', '1740', '1455', '84585', '1616587', '4721563', '218800']
    hh_data = get_hh_data(emp_id)
    create_database('headhunter')
    save_data_to_database(hh_data, 'headhunter')
    db = DBManager()

    print('Привет! Давай найдем вакансии.')

    while True:
        command = input(
            '1 - Вывести список вакансий\n'
            '2 - Вывести список всех компаний и количество вакансий у каждой компании\n'
            '3 - Вывести среднюю зарплату по вакансиям\n'
            '4 - Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
            '5 - Вывести список всех вакансий по ключевому слову\n'
            '6 - выйти '
        )

        if command == '6':
            break
        elif command == '1':
            print(db.get_all_vacancies())
        elif command == '2':
            print(db.get_companies_and_vacancies_count())
        elif command == '3':
            print(db.get_avg_salary())
        elif command == '4':
            print(db.get_vacancies_with_higher_salary())
        elif command == '5':
            keyword = input('Введи ключевое слово: ')
            print(db.get_vacancies_with_keyword(keyword))

if __name__ == "__main__":
    main()
