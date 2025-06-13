### [Назад](../README.md)
### Nginx и Gunicorn
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
User=www-data
Group=www-data
WorkingDirectory=/var/www/html/store-server/store
ExecStart=/var/www/html/store-server/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          store.wsgi:application
```
Наконец, вы добавите раздел [Install]. Это сообщит системам, с чем связать эту службу, если вы разрешите ее запуск при загрузке. Вы хотите, чтобы эта служба запускалась, когда обычная многопользовательская система запущена:
```sh
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/html/store-server/store
ExecStart=/var/www/html/store-server/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          store.wsgi:application

[Install]
WantedBy=multi-user.target
```
На этом ваш служебный файл systemd завершен. Сохраните и закройте его сейчас.

Теперь вы можете запустить и включить сокет Gunicorn. Это создаст файл сокета в /run/gunicorn.sock сейчас и при загрузке. Когда будет установлено подключение к этому сокету, система автоматически запустит gunicorn.service для его обработки:
```sh
sudo systemctl enable gunicorn.socket --now
```
#### Проверка наличия файла сокета Gunicorn

Проверьте статус процесса, чтобы узнать, удалось ли ему запуститься:
```sh
systemctl status gunicorn.socket
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
systemctl status gunicorn
```
```sh
Output
○ gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
TriggeredBy: ● gunicorn.socket
```

#### Настройте Nginx для передачи прокси-сервера Gunicorn

Теперь, когда Gunicorn настроен, вам нужно настроить Nginx для передачи трафика процессу.

Начните с создания и открытия нового серверного блока в каталоге доступных сайтов Nginx:
```sh
sudo nano /etc/nginx/sites-available/store-server
```
Внутри откройте новый серверный блок. Вы начнете с указания, что этот блок должен прослушивать обычный порт 80 и что он должен отвечать на доменное имя или IP-адрес вашего сервера:
```sh
server {
    listen 80;
    server_name server_domain_or_IP;
}
```
Далее вы скажете Nginx игнорировать любые проблемы с поиском значка. Вы также скажете ему, где найти статические ресурсы, которые вы собрали в своем каталоге ~/myprojectdir/static. Все эти файлы имеют стандартный префикс URI “/static”, поэтому вы можете создать блок расположения в соответствии с этими запросами:
```sh
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/html/store-server/store;
    }
}
```
Наконец, создайте блок location / {}, соответствующий всем остальным запросам. Внутри этого местоположения вы включите стандартный файл proxy_params, входящий в комплект установки Nginx, а затем передадите трафик непосредственно в сокет Gunicorn:
```sh
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/html/store-server/store;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
Сохраните и закройте файл, когда закончите. Теперь вы можете включить файл, связав его с каталогом сайтов с поддержкой:
```sh
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```
Проверьте конфигурацию Nginx на наличие синтаксических ошибок, набрав:
```sh
sudo nginx -t
```
Если сообщений об ошибках не поступало, продолжайте и перезапустите Nginx, набрав:
```sh
sudo systemctl restart nginx
```