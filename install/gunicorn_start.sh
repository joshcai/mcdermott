#!/bin/bash

NAME="mcdermott"                                  # Name of the application
DJANGODIR=/home/ubuntu/mcdermott                  # Django project directory
SOCKFILE=/home/ubuntu/mcdermott/run/gunicorn.sock  # we will communicte using this unix socket
USER=ubuntu                                        # the user to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=mcdermott.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=mcdermott.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-