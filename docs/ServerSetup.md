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
usermod -a -G new_sudo_user www-data # 
```
### Установка пакетов из репозиториев Ubuntu
```sh
ssh new_sudo_user@your_server_ip
sudo apt update
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl redis
```