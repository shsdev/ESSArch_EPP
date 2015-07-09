#!/bin/bash
CELERY_WORKER1_FILE="/var/log/ESSArch/log/proc/celery_worker1.pid"
if [ -f "$CELERY_WORKER1_FILE" ]
then
    CELERY_WORKER1_PID=`cat $CELERY_WORKER1_FILE`
    echo "Celery worker is running (PID $CELERY_WORKER1_PID)"
else
    sudo ESSArch_EPP/extra/celeryd start
fi

source .env
python ESSArch_EPP/manage.py runserver
