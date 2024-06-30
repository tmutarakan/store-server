# store-server

## Локальный запуск 
### При помощи docker
#### Файл docker-compose.yml для запуска необходимых сервисов
```yaml
version: "3.9"
services:
  postgres:
    image: postgres:14.9-alpine
    container_name: store-server-db
    environment:
      POSTGRES_DB: "store_db"
      POSTGRES_USER: "store_username"
      POSTGRES_PASSWORD: "store_password"
      PGDATA: "/var/lib/postgresql/data/pgdata"
    volumes:
      - db:/var/lib/postgresql/data
    #  - $PWD/data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  adminer:
    image: adminer
    container_name: "store-server-webface"
    ports:
      - 8082:8080

  redis:
    image: redis:7.0.4-alpine
    container_name: "store_redis"
    ports:
      - "6379:6379"
    volumes:
      - cache:/data
      #- cache/redis.conf:/etc/redis/redis.conf
    #  - $PWD/pyredis/redis_snapshot:/data
    #  - $PWD/pyredis/config/redis.conf:/etc/redis/redis.conf
    
volumes:
  db:
    driver: local
  cache:
    driver: local

```
#### Команда для запуска:
```sh
docker-compose up -d
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
#### Запуск локального сервера
```sh
./manage.py runserver
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