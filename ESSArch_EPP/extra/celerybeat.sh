#!/bin/bash
# =========================================================
#  celerybeat - Starts the Celery periodic task scheduler.
# =========================================================
#
# :Usage: /etc/init.d/celerybeat {start|stop|force-reload|restart|try-restart|status}
# :Configuration file: /etc/default/celerybeat or /etc/default/celeryd
#
# See http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html#generic-init-scripts
#
# chkconfig: - 84 15
#
### BEGIN INIT INFO
# Provides:          celerybeat
# Required-Start:    $all
# Required-Stop:     $network $local_fs $remote_fs $portmap
# Default-Start:     2 3 5
# Default-Stop:      0 1 6
# Short-Description: celery periodic task scheduler
### END INIT INFO
#
# Cannot use set -e/bash -e since the kill -0 command will abort
# abnormally in the absence of a valid process ID.
#set -e
LOCK_FILE=/var/lock/celerybeat
VERSION=10.0
echo "celery init v${VERSION}."

if [ $(id -u) -ne 0 ]; then
    echo "Error: This program can only be used by the root user."
    echo "       Unpriviliged users must use 'celery beat --detach'"
    exit 1
fi


# May be a runlevel symlink (e.g. S02celeryd)
if [ -L "$0" ]; then
    SCRIPT_FILE=$(readlink "$0")
else
    SCRIPT_FILE="$0"
fi
SCRIPT_NAME="$(basename "$SCRIPT_FILE")"

export LD_LIBRARY_PATH=/ESSArch/pd/python/lib:/ESSArch/pd/libxslt/lib:/ESSArch/pd/libxml/lib:/ESSArch/pd/libmpeg2/lib:/usr/local/lib
#export DJANGO_SETTINGS_MODULE=config.settings
export PYTHONPATH=/ESSArch/pd/python/lib/python2.7/site-packages/ESSArch_EPP:/ESSArch/pd/python/lib/python2.7/site-packages/ESSArch_EPP/workers:/ESSArch/config

# /etc/init.d/celerybeat: start and stop the celery periodic task scheduler daemon.

# Make sure executable configuration script is owned by root
_config_sanity() {
    local path="$1"
    local owner=$(ls -ld "$path" | awk '{print $3}')
    local iwgrp=$(ls -ld "$path" | cut -b 6)
    local iwoth=$(ls -ld "$path" | cut -b 9)

    if [ "$(id -u $owner)" != "0" ]; then
        echo "Error: Config script '$path' must be owned by root!"
        echo
        echo "Resolution:"
        echo "Review the file carefully and make sure it has not been "
        echo "modified with mailicious intent.  When sure the "
        echo "script is safe to execute with superuser privileges "
        echo "you can change ownership of the script:"
        echo "    $ sudo chown root '$path'"
        exit 1
    fi

    if [ "$iwoth" != "-" ]; then  # S_IWOTH
        echo "Error: Config script '$path' cannot be writable by others!"
        echo
        echo "Resolution:"
        echo "Review the file carefully and make sure it has not been "
        echo "modified with malicious intent.  When sure the "
        echo "script is safe to execute with superuser privileges "
        echo "you can change the scripts permissions:"
        echo "    $ sudo chmod 640 '$path'"
        exit 1
    fi
    if [ "$iwgrp" != "-" ]; then  # S_IWGRP
        echo "Error: Config script '$path' cannot be writable by group!"
        echo
        echo "Resolution:"
        echo "Review the file carefully and make sure it has not been "
        echo "modified with malicious intent.  When sure the "
        echo "script is safe to execute with superuser privileges "
        echo "you can change the scripts permissions:"
        echo "    $ sudo chmod 640 '$path'"
        exit 1
    fi
}

scripts=""

#if test -f /etc/default/celeryd; then
#    scripts="/etc/default/celeryd"
#    _config_sanity /etc/default/celeryd
#    . /etc/default/celeryd
#fi

if test -f /ESSArch/config/celeryd; then
    scripts="/ESSArch/config/celeryd"
    #_config_sanity /ESSArch/app/config/celeryd
    . /ESSArch/config/celeryd
fi


EXTRA_CONFIG="/etc/default/${SCRIPT_NAME}"
if test -f "$EXTRA_CONFIG"; then
    scripts="$scripts, $EXTRA_CONFIG"
    _config_sanity "$EXTRA_CONFIG"
    . "$EXTRA_CONFIG"
fi

echo "Using configuration: $scripts"

CELERY_BIN=${CELERY_BIN:-"celery"}
DEFAULT_USER="celery"
DEFAULT_PID_FILE="/var/run/celery/beat.pid"
DEFAULT_LOG_FILE="/var/log/celery/beat.log"
DEFAULT_LOG_LEVEL="INFO"
DEFAULT_CELERYBEAT="$CELERY_BIN beat"

CELERYBEAT=${CELERYBEAT:-$DEFAULT_CELERYBEAT}
CELERYBEAT_LOG_LEVEL=${CELERYBEAT_LOG_LEVEL:-${CELERYBEAT_LOGLEVEL:-$DEFAULT_LOG_LEVEL}}

# Sets --app argument for CELERY_BIN
CELERY_APP_ARG=""
if [ ! -z "$CELERY_APP" ]; then
    CELERY_APP_ARG="--app=$CELERY_APP"
fi

CELERYBEAT_USER=${CELERYBEAT_USER:-${CELERYD_USER:-$DEFAULT_USER}}

# Set CELERY_CREATE_DIRS to always create log/pid dirs.
CELERY_CREATE_DIRS=${CELERY_CREATE_DIRS:-0}
CELERY_CREATE_RUNDIR=$CELERY_CREATE_DIRS
CELERY_CREATE_LOGDIR=$CELERY_CREATE_DIRS
if [ -z "$CELERYBEAT_PID_FILE" ]; then
    CELERYBEAT_PID_FILE="$DEFAULT_PID_FILE"
    CELERY_CREATE_RUNDIR=1
fi
if [ -z "$CELERYBEAT_LOG_FILE" ]; then
    CELERYBEAT_LOG_FILE="$DEFAULT_LOG_FILE"
    CELERY_CREATE_LOGDIR=1
fi

export CELERY_LOADER

CELERYBEAT_OPTS="$CELERYBEAT_OPTS -f $CELERYBEAT_LOG_FILE -l $CELERYBEAT_LOG_LEVEL"

if [ -n "$2" ]; then
    CELERYBEAT_OPTS="$CELERYBEAT_OPTS $2"
fi

CELERYBEAT_LOG_DIR=`dirname $CELERYBEAT_LOG_FILE`
CELERYBEAT_PID_DIR=`dirname $CELERYBEAT_PID_FILE`

# Extra start-stop-daemon options, like user/group.

CELERYBEAT_CHDIR=${CELERYBEAT_CHDIR:-$CELERYD_CHDIR}
if [ -n "$CELERYBEAT_CHDIR" ]; then
    DAEMON_OPTS="$DAEMON_OPTS --workdir=$CELERYBEAT_CHDIR"
fi


export PATH="${PATH:+$PATH:}/usr/sbin:/sbin"

check_dev_null() {
    if [ ! -c /dev/null ]; then
        echo "/dev/null is not a character device!"
        exit 75  # EX_TEMPFAIL
    fi
}

maybe_die() {
    if [ $? -ne 0 ]; then
        echo "Exiting: $*"
        exit 77  # EX_NOPERM
    fi
}

create_default_dir() {
    if [ ! -d "$1" ]; then
        echo "- Creating default directory: '$1'"
        mkdir -p "$1"
        maybe_die "Couldn't create directory $1"
        echo "- Changing permissions of '$1' to 02755"
        chmod 02755 "$1"
        maybe_die "Couldn't change permissions for $1"
        if [ -n "$CELERYBEAT_USER" ]; then
            echo "- Changing owner of '$1' to '$CELERYBEAT_USER'"
            chown "$CELERYBEAT_USER" "$1"
            maybe_die "Couldn't change owner of $1"
        fi
        if [ -n "$CELERYBEAT_GROUP" ]; then
            echo "- Changing group of '$1' to '$CELERYBEAT_GROUP'"
            chgrp "$CELERYBEAT_GROUP" "$1"
            maybe_die "Couldn't change group of $1"
        fi
    fi
}

check_paths() {
    if [ $CELERY_CREATE_LOGDIR -eq 1 ]; then
        create_default_dir "$CELERYBEAT_LOG_DIR"
    fi
    if [ $CELERY_CREATE_RUNDIR -eq 1 ]; then
        create_default_dir "$CELERYBEAT_PID_DIR"
    fi
}


create_paths () {
    create_default_dir "$CELERYBEAT_LOG_DIR"
    create_default_dir "$CELERYBEAT_PID_DIR"
}


wait_pid () {
    pid=$1
    forever=1
    i=0
    while [ $forever -gt 0 ]; do
        kill -0 $pid 1>/dev/null 2>&1
        if [ $? -eq 1 ]; then
            echo "OK"
            forever=0
        else
            kill -TERM "$pid"
            i=$((i + 1))
            if [ $i -gt 60 ]; then
                echo "ERROR"
                echo "Timed out while stopping (30s)"
                forever=0
            else
                sleep 0.5
            fi
        fi
    done
}


stop_beat () {
    echo -n "Stopping ${SCRIPT_NAME}... "
    if [ -f "$CELERYBEAT_PID_FILE" ]; then
        wait_pid $(cat "$CELERYBEAT_PID_FILE")
        if [ -n "$LOCK_FILE" ] ; then
            rm -f $LOCK_FILE
        fi
    else
        echo "NOT RUNNING"
    fi
}

_chuid () {
    su -m "$CELERYBEAT_USER" -c "$CELERYBEAT $*"
}

start_beat () {
    echo "Starting ${SCRIPT_NAME}..."
    _chuid $CELERY_APP_ARG $CELERYBEAT_OPTS $DAEMON_OPTS --detach \
                --pidfile="$CELERYBEAT_PID_FILE"
    if [ -n "$LOCK_FILE" ] ; then
        touch $LOCK_FILE
    fi
}



case "$1" in
    start)
        check_dev_null
        check_paths
        start_beat
    ;;
    stop)
        check_paths
        stop_beat
    ;;
    reload|force-reload)
        echo "Use start+stop"
    ;;
    restart)
        echo "Restarting celery periodic task scheduler"
        check_paths
        stop_beat
        check_dev_null
        start_beat
    ;;
    create-paths)
        check_dev_null
        create_paths
    ;;
    check-paths)
        check_dev_null
        check_paths
    ;;
    *)
        echo "Usage: /etc/init.d/${SCRIPT_NAME} {start|stop|restart|create-paths}"
        exit 64  # EX_USAGE
    ;;
esac

exit 0
