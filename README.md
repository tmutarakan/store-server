# store-server

## Настройка сервера(Ubuntu 22.04)

### Вход под root-ом:
```sh
ssh root@your_server_ip
```

#### Создание пользователя для администрирование сервера:
```sh
adduser new_sudo_user # Создание пользователя
usermod -aG sudo new_sudo_user # Выдача привилегий администратора
usermod -a -G new_sudo_user www-data # 
```

### Настройка и установка СУБД PostgreSQL:
```sh
ssh new_sudo_user@your_server_ip
```
#### Установка пакетов из репозиториев Ubuntu
```sh
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```
#### Создание базы данных PostgreSQL и пользователя
##### Войдите в интерактивный сеанс Postgres, набрав:
```sh
sudo -u postgres psql
```
##### Сначала создайте базу данных для вашего проекта:
```psql
CREATE DATABASE my_db;
CREATE ROLE my_username with password 'my_password';
ALTER ROLE "my_username" WITH LOGIN; 
GRANT ALL PRIVILEGES ON DATABASE "my_db" to "my_username";
ALTER USER my_username CREATEDB;
```
### Развёртывание проекта
#### Клонирование репозитория
```sh
sudo apt install git
git clone https://github.com/tmutarakan/store-server.git
```
#### В каталоге проекта создайте виртуальную среду Python, набрав:
```sh
cd store-server
python3 -m venv venv
```
#### Перед установкой требований к Python для вашего проекта вам необходимо активировать виртуальную среду. Вы можете сделать это, набрав:
```sh
source venv/bin/activate
pip install -r requirements.txt
```
#### Перенос статики для сервера:
```sh
cd store
./manage.py collectstatic
```



