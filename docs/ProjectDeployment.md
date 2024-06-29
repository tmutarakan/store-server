### [Назад](../README.md)
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
#### Установка gunicorn
```sh
pip install gunicorn
```