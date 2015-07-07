#!/bin/bash
CELERY_WORKER1_PID=`cat /var/log/ESSArch/log/proc/celery_worker1.pid`
if [ -n "$CELERY_WORKER1_PID" ]; then
    echo "Celery worker is running (PID $CELERY_WORKER1_PID)"
else
    sudo ESSArch_EPP/extra/celeryd start
fi

source .env
python ESSArch_EPP/manage.py runserver
