### [Назад](../README.md)
###  Настройка Celery
/etc/systemd/system/celery.service:
```sh
[Unit]
Description=Celery Service
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/store-server/store
ExecStart=/home/user/store-server/venv/bin/celery -A store worker -l INFO

[Install]
WantedBy=multi-user.target
```
После того, как вы поместили этот файл в /etc/systemd/system, вам следует запустить systemctl daemon-reload, чтобы Systemd подтвердил этот файл. Вам также следует запускать эту команду каждый раз, когда вы его изменяете. Используйте systemctl enable celery.service, если вы хотите, чтобы служба celery автоматически запускалась при (повторной) загрузке системы.