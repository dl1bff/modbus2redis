# modbus2redis
Periodically read data from a Modbus device and store it in Redis.




install:

addgroup --system m2redis
adduser --system --ingroup m2redis m2redis
usermod --groups dialout m2redis

cp modbus2redis.conf /etc
cp modbus2redis.py /usr/local/bin
cp modbus2redis.service /etc/systemd/system

systemctl enable modbus2redis.service

systemctl start modbus2redis.service




