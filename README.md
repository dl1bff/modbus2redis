# modbus2redis
Periodically read data from a Modbus device and store it in Redis.




install (Debian, Raspbian):

```

pip install pymodbus redis


addgroup --system m2redis
adduser --system --ingroup m2redis m2redis
usermod --groups dialout m2redis

cp modbus2redis.conf /etc
cp modbus2redis.py /usr/local/bin
chmod 755 /usr/local/bin/modbus2redis.py
cp modbus2redis.service /etc/systemd/system

systemctl enable modbus2redis.service

systemctl start modbus2redis.service
```


If the Redis server is not on the local machine:  use "spiped"

```
apt-get install spiped

addgroup --system spiped
adduser --system --ingroup spiped spiped

mkdir /etc/spiped
chgrp spiped /etc/spiped
chmod 710 /etc/spiped

dd if=/dev/urandom of=/etc/spiped/redis.key bs=32 count=1

chown spiped:spiped /etc/spiped/redis.key
chmod 400 /etc/spiped/redis.key

cp spiped-transmit.service /etc/systemd/system

systemctl enable spiped-transmit.service

systemctl start spiped-transmit.service

```


