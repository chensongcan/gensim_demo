#!/bin/sh

DAEMON="python main.py"
NAME=train_model
ERRFILE="train_model.log"
PIDFILE="train_model.pid"

case "$1" in
    start)
        echo "Start $NAME..."
        nohup $DAEMON >> $ERRFILE 2>&1 &
        echo $! > $PIDFILE
        echo "$NAME is running."
        ;;
    stop)
        echo "Stopping $NAME..."
        pid=`cat $PIDFILE`
        kill $pid
        rm $PIDFILE
        echo "$NAME exits."
        ;;
esac

exit 0
