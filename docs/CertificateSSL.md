### [Назад](../README.md)
### Подключение SSL сертификата
+ Установка Certbot
    
    Certbot рекомендует использовать snap для установки. Пакеты Snap работают почти во всех дистрибутивах Linux, но для управления пакетами snap требуется, чтобы вы сначала установили snapd. Ubuntu 22.04 поставляется с поддержкой snap из коробки, поэтому вы можете начать с того, что убедитесь, что ваше snap core обновлено:
    ```sh
    sudo snap install core; sudo snap refresh core
    ```
    Если вы работаете на сервере, на котором ранее была установлена более старая версия certbot, вам следует удалить ее, прежде чем двигаться дальше:
    ```sh
    sudo apt remove certbot
    ```
    После этого вы можете установить certbot:
    ```sh
    sudo snap install --classic certbot
    ```
    Наконец, вы можете привязать команду certbot из каталога snap install к своему пути, чтобы вы могли запустить ее, просто набрав certbot. Это необязательно для всех пакетов, но привязки по умолчанию, как правило, менее навязчивы, поэтому они случайно не конфликтуют с какими-либо другими системными пакетами:
    ```sh
    sudo ln -s /snap/bin/certbot /usr/bin/certbot
    ```
+ Получение SSL-сертификата

    Certbot предоставляет множество способов получения SSL-сертификатов с помощью плагинов. Плагин Nginx позаботится о перенастройке Nginx и перезагрузке конфигурации при необходимости. Чтобы использовать этот плагин, введите следующее:
    ```sh
    sudo certbot --nginx -d example.com -d www.example.com
    ```
    При этом запускается certbot с плагином --nginx, используя -d для указания доменных имен, для которых мы хотели бы, чтобы сертификат был действителен.

    При выполнении команды вам будет предложено ввести адрес электронной почты и согласиться с условиями предоставления услуг. После этого вы должны увидеть сообщение о том, что процесс прошел успешно и где хранятся ваши сертификаты:
    ```
    Output
    IMPORTANT NOTES:
    Successfully received certificate.
    Certificate is saved at: /etc/letsencrypt/live/your_domain/fullchain.pem
    Key is saved at: /etc/letsencrypt/live/your_domain/privkey.pem
    This certificate expires on 2022-06-01.
    These files will be updated when the certificate renews.
    Certbot has set up a scheduled task to automatically renew this certificate in the background.

    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    If you like Certbot, please consider supporting our work by:
    * Donating to ISRG / Let's Encrypt: https://letsencrypt.org/donate
    * Donating to EFF: https://eff.org/donate-le
    ```
    Ваши сертификаты скачаны, установлены и загружаются, и ваша конфигурация Nginx теперь автоматически перенаправляет все веб-запросы на https://. Попробуйте перезагрузить свой веб-сайт и обратите внимание на индикатор безопасности вашего браузера. Он должен указывать на то, что сайт защищен должным образом, обычно со значком замка. Если вы протестируете свой сервер с помощью серверного теста SSL Labs, он получит оценку "А".