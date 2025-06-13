### [Назад](../README.md)
### Развёртывание проекта
#### Клонирование репозитория
```sh
sudo apt install git
cd /var/www/html
git clone https://github.com/tmutarakan/store-server.git
```
#### В каталоге проекта создайте виртуальную среду Python, набрав:
```sh
cd store-server
uv sync
```
#### Перенос статики для сервера:
```sh
cd store
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py collectstatic
```
#### Установка gunicorn
```sh
uv add gunicorn
```