### [Назад](../README.md)
### Введение

Использование SSH-ключей — простой и надежный способ обеспечения безопасности соединения с сервером.  В отличие от пароля, взломать SSH-ключ практически невозможно. Сгенерировать SSH-ключ очень просто.
### SSH-ключ для Linux/MacOS

#### Откройте терминал и выполните команду:
```sh
ssh-keygen -t rsa
```
#### На консоль будет выведен следующий диалог:
```sh
Enter file in which to save the key (/home/user/.ssh/id_rsa):
```
#### Нажмите на клавишу Enter.  Далее система предложит ввести кодовую фразу для дополнительной защиты SSH-подключения:
```sh
Enter passphrase (empty for no passphrase):
```
Этот шаг можно пропустить. При ответе на этот и следующий вопрос просто нажмите клавишу Enter.

#### После этого ключ будет создан, а на консоль будет выведено следующее сообщение:
```sh
Your identification has been saved in /home/user/.ssh/id_rsa.
Your public key has been saved in /home/user/.ssh/id_rsa.pub.
The key fingerprint is:
476:b2:a8:7f:08:b4:c0:af:81:25:7e:21:48:01:0e:98 user@localhost

The key's randomart image is:

+--[ RSA 2048]----+

|+.o.             |

|ooE              |

|oo               |

|o.+..            |

|.+.+..  S .      |

|....+  o +       |

|  .o ....        |

|  .  .. .        |

|    ....         |

+-----------------+
```
#### Далее выполните в терминале команду:
```sh
cat ~/.ssh/id_rsa.pub
```
На консоль будет выведен ключ.

#### Скопируйте ключ на сервер:
```sh
ssh-copy-id new_sudo_user@your_server_ip
```

#### Откройте файл /etc/ssh/sshd_config и замените строки:
```sh
PermitRootLogin no  # Запрет на вход по ssh для пользователя root
PasswordAuthentication no   # Запрет входа по паролю
```

#### Перезапустите ssh server:
```sh
sudo systemctl restart ssh
```
