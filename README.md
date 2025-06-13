# store-server

## Локальный запуск 
### При помощи docker
#### Файл docker-compose.yml для запуска необходимых сервисов
Требуются порты 5432 6379 8082
#### Команда для запуска:
```sh
docker-compose up -d
```
#### В каталоге проекта создайте виртуальную среду Python, набрав:
```sh
cd store-server
python3 -m venv venv
```
#### uv - пакетный менеджер и менеджер виртуальных окружений
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
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
#### Запуск локального сервера
```sh
uv run manage.py runserver
```
## Запуск на сервере

### [Настройка сервера](docs/ServerSetup.md)
### [Аутентификацию SSH по ключу](docs/KeySSH.md)
### [Установка и настройка СУБД PostgreSQL](docs/ConfiguringPostgreSQL.md)
### [Развёртывание проекта](docs/ProjectDeployment.md)
### [Nginx и Gunicorn](docs/Nginx&Gunicorn.md)
### [Настройка Redis](docs/ConfiguringRedis.md)
### [Настройка Celery](docs/ConfiguringCelery.md)
### [Установка и настройка firewall UFW](docs/Installing&ConfiguringUFW.md)
### [Подключение SSL сертификата](docs/CertificateSSL.md)

## Полезные ссылки

[Как настроить Django с помощью Postgres, Nginx и Gunicorn в Debian 11](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-debian-11)

[Как установить и обезопасить Redis в Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-22-04)

[Настройка Celery](https://docs.celeryq.dev/en/stable/userguide/daemonizing.html#usage-systemd)

[Первоначальная настройка сервера Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-22-04)

[Как защитить Nginx с помощью Let's Encrypt в Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-22-04)