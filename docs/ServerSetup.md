### [Назад](../README.md)
### Настройка сервера(Ubuntu 22.04)

#### Вход под root-ом:
```sh
ssh root@your_server_ip
```

#### Создание пользователя для администрирование сервера:
```sh
adduser new_sudo_user # Создание пользователя
usermod -aG sudo new_sudo_user # Выдача привилегий администратора
usermod -a -G www-data new_sudo_user# 
```
### Установка пакетов из репозиториев Ubuntu
```sh
ssh new_sudo_user@your_server_ip
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl redis
sudo apt install nginx curl redis postgresql postgresql-contrib
curl -LsSf https://astral.sh/uv/install.sh | sh
```