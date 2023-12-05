# Код, который я использовал для создания базы данных
# Создание базы данных
CREATE DATABASE employers_vacancies
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

# Создание таблицы Регионы
CREATE TABLE area
(
	area_id int PRIMARY KEY,
	area_name varchar(100)
);

# Создание таблицы Работодатели
CREATE TABLE employers
(
	employer_id int PRIMARY KEY,
	employer_name varchar(100),
	area_id int REFERENCES area,
	site_url varchar(100),
	alternate_url varchar(100),
	vacancies_url varchar(100),
	description text
);

# Создание таблицы Вакансии
CREATE TABLE vacancies
(
	vacancy_id int PRIMARY KEY,
	vacancy_name varchar(100),
	salary int,
	requirement text,
	responsibility text,
	area_id int REFERENCES area,
	employer_id int REFERENCES employers,
	contacts varchar(100),
	created_at timestamp,
	alternate_url varchar(100)
);