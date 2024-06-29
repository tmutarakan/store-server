### [Назад](../README.md)
### Настройка Redis
Необходимо внести одно важное изменение в конфигурационный файл Redis, который был сгенерирован автоматически во время установки.

Откройте этот файл в предпочитаемом вами текстовом редакторе:
```sh
sudo nano /etc/redis/redis.conf
```
Внутри файла найдите директиву supervised. Эта директива позволяет вам объявить систему инициализации для управления Redis как службой, предоставляя вам больший контроль над ее работой. По умолчанию директива supervised имеет значение no. Поскольку вы используете Ubuntu, которая использует systemd init system, измените это на systemd:
```sh
. . .

# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd

. . .

```
Это единственное изменение, которое вам нужно внести в конфигурационный файл Redis на данный момент, поэтому сохраните и закройте его, когда закончите.

Затем перезапустите службу Redis, чтобы отразить изменения, внесенные вами в файл конфигурации:
```sh
sudo systemctl restart redis.service
```