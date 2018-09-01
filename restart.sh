#!/bin/bash

function restart {
port=$1
pid=$(ps -ef |grep gunicorn |grep -v grep |grep $port |awk '{print $3}' |sort |uniq |awk '{if($NF != 1) print $0}')

echo "restarting port ${port}..."

while [ ! -z ${pid} ]
do
    kill -9 ${pid}
    echo "port ${port} killed..."
    pid=$(ps -ef |grep gunicorn |grep -v grep |grep $port |awk '{print $3}' |sort |uniq |awk '{if($NF != 1) print $0}')
done

gunicorn -c config.py -b 0.0.0.0:${port} phxweb.wsgi:application -D
sleep 3
pid=$(ps -ef |grep gunicorn |grep -v grep |grep $port |awk '{print $3}' |sort |uniq |awk '{if($NF != 1) print $0}')
if [ ! -z ${pid} ];then
    echo "port ${port} restarted ok."
    ps -ef |grep gunicorn |grep -v grep |grep $port
else
    echo "port ${port} restarted failed. pls check!"
fi
}

restart 5050
sleep 1
restart 5000
