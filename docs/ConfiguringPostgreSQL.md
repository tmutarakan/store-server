### [Назад](../README.md)
### Создание базы данных PostgreSQL и пользователя
#### Войдите в интерактивный сеанс Postgres, набрав:
```sh
sudo -u postgres psql
```
#### Сначала создайте базу данных для вашего проекта:
```psql
CREATE DATABASE my_db;
CREATE ROLE my_username with password 'my_password';
ALTER ROLE "my_username" WITH LOGIN; 
GRANT ALL PRIVILEGES ON DATABASE "my_db" to "my_username";
ALTER USER my_username CREATEDB;
```