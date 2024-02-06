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
sudo apt install python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl redis
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
#### Установка gunicorn
```sh
pip install gunicorn
```
#### Создание файлов systemd  Socket и Service для Gunicorn

Сокет Gunicorn будет создан при загрузке и будет прослушивать соединения. Когда соединение произойдет, система автоматически запустит процесс Gunicorn для обработки соединения.

Начните с создания и открытия файла сокета systemd для Gunicorn с правами sudo:
```sh
sudo nano /etc/systemd/system/gunicorn.socket
```
Внутри вы создадите раздел [Unit] для описания сокета, раздел [Socket] для определения местоположения сокета и раздел [Install], чтобы убедиться, что сокет создан в нужное время:
```sh
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
Сохраните и закройте файл, когда закончите.

Далее создайте и откройте служебный файл systemd для Gunicorn с правами sudo в вашем текстовом редакторе. Имя служебного файла должно совпадать с именем файла сокета, за исключением расширения:
```sh
sudo nano /etc/systemd/system/gunicorn.service
```
Начните с раздела [Unit], который используется для указания метаданных и зависимостей. Разместите здесь описание службы и сообщите системе инициализации, чтобы она запускалась только после того, как будет достигнута сетевая цель. Поскольку ваша служба полагается на сокет из файла сокета, вам необходимо включить директиву Requires, чтобы указать эту связь:
```sh
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target
```
Далее вы создадите раздел [Service]. Укажите пользователя и группу, от имени которых вы хотите запустить процесс. Вы предоставите своей учетной записи обычного пользователя право собственности на процесс, поскольку ей принадлежат все соответствующие файлы. Вы передадите право собственности на группу www-data, чтобы Nginx мог взаимодействовать с Gunicorn.

Затем вы выделите рабочий каталог и укажете команду, которую будете использовать для запуска службы. В этом случае вам необходимо указать полный путь к исполняемому файлу Gunicorn, который установлен в нашей виртуальной среде. Затем вы привяжете процесс к сокету Unix, который вы создали в каталоге /run, чтобы процесс мог взаимодействовать с Nginx. Вы записываете все данные в стандартный вывод, чтобы процесс ведения журнала мог собирать журналы Gunicorn. Вы также можете указать любые дополнительные настройки Gunicorn здесь. Например, в данном случае вы указали 3 рабочих процесса:
```sh
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myprojectdir
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application
```
Наконец, вы добавите раздел [Install]. Это сообщит системам, с чем связать эту службу, если вы разрешите ее запуск при загрузке. Вы хотите, чтобы эта служба запускалась, когда обычная многопользовательская система запущена:
```sh
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=`user`
Group=www-data
WorkingDirectory=/home/sammy/myprojectdir
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```
На этом ваш служебный файл systemd завершен. Сохраните и закройте его сейчас.

Теперь вы можете запустить и включить сокет Gunicorn. Это создаст файл сокета в /run/gunicorn.sock сейчас и при загрузке. Когда будет установлено подключение к этому сокету, система автоматически запустит gunicorn.service для его обработки:
```sh
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
#### Проверка наличия файла сокета Gunicorn

Проверьте статус процесса, чтобы узнать, удалось ли ему запуститься:
```sh
sudo systemctl status gunicorn.socket
```
Вы должны получить результат, подобный этому:
```sh
Output
● gunicorn.socket - gunicorn socket
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: enabled)
     Active: active (listening) since Thu 2022-08-04 19:02:54 UTC; 5s ago
   Triggers: ● gunicorn.service
     Listen: /run/gunicorn.sock (Stream)
     CGroup: /system.slice/gunicorn.socket

Apr 18 17:53:25 django systemd[1]: Listening on gunicorn socket.
```
#### Тестирование активации сокета

В настоящее время, если вы только запустили модуль gunicorn.socket, служба gunicorn.service еще не будет активна, поскольку сокет еще не получил никаких подключений. Вы можете проверить это, введя:
```sh
sudo systemctl status gunicorn
```
```sh
Output
○ gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
TriggeredBy: ● gunicorn.socket
```
