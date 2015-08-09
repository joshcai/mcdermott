#!/bin/bash

# these commands are run from the home directory (/home/ubuntu)

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install git
sudo apt-get install memcached
sudo apt-get install python-virtualenv
sudo apt-get install python-dev
sudo apt-get install nginx
sudo apt-get install supervisor

sudo apt-get install libjpeg-dev
sudo apt-get install zlib1g-dev
sudo apt-get install libpng12-dev

git clone https://github.com/mcdermott-scholars/mcdermott.git

cd mcdermott
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py buildwatson
python mcdermott/manage.py collectstatic --noinput

# move these to /etc/environment
export DEBUG=false
export SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)
export ALLOWED_HOSTS='localhost, *.joshcai.com'

# create log file
mkdir -p /home/ubuntu/logs/
touch /home/ubuntu/logs/mcdermott_gunicorn_supervisor.log

# create socket file
mkdir -p /home/ubuntu/mcdermott/run/gunicorn.sock

# create symbolic links 
sudo ln -s /home/ubuntu/mcdermott/install/mcdermott.conf /etc/nginx/sites-enabled/
sudo ln -s /home/ubuntu/mcdermott/install/supervisor_mcd.conf /etc/supervisor/conf.d/

sudo service nginx restart

sudo supervisorctl reread
sudo supervisorctl update

# useful later:
# sudo supervisorctl restart mcdermott
