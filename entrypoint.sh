#!/bin/bash

[ -f "env.sh" ] && source env.sh && echo "env.sh imported"

function get_inner_ip() {
  ifconfig | grep "eth0:" -C 2 | grep "inet " | grep -v "127.0.0.1" | awk -F"netmask" '{print $1}'
}

function get_remote_ip() {
  if [ -z "$GET_SERVER_IP_API" ]
  then
    GET_SERVER_IP_API="https://ddnsip.cn"
  fi
  curl -s -f "$GET_SERVER_IP_API"
}

function get_server_ip(){
  get_remote_ip || get_inner_ip
}

function nodename(){
    get_server_ip | awk -F"." '{print "w"$3"_"$4}'
}

function start() {
    celery multi start `nodename` -A ${SITEAPP} -c $CELERY_CONCURRENCY -Q ${CELERY_QUEUE}  --logfile=$LOG_DIR/${PROJECT}.${CELERY_QUEUE}.worker%I.log --pidfile=/tmp/${PROJECT}.${CELERY_QUEUE}.worker.pid
}

function run() {
    celery -A ${SITEAPP}  worker -Q ${CELERY_QUEUE}
}

function flask() {
    python app.py
}

function stop() {
    celery multi stopwait `nodename`  --logfile=$LOG_DIR/${PROJECT}.${CELERY_QUEUE}.worker%I.log --pidfile=/tmp/${PROJECT}.${CELERY_QUEUE}.worker.pid
}

function restart() {
  stop
  start
}

function killall() {
    pids=`ps -ef | grep celery | grep -v "grep" | grep -v "killall"| awk '{print $2}'`
    if [ -n "$pids" ]
    then
       kill -9 $pids
    fi
}

function shell(){
  ipython
}


$@