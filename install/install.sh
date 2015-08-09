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

# move these to /etc/environment
export DEBUG=false
export SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 64 | head -n 1)
export ALLOWED_HOSTS='localhost, *.joshcai.com'

# gunicorn config
sudo chmod u+x mcdermott/install/gunicorn_start.sh

python mcdermott/manage.py collectstatic --noinput
sudo service nginx restart

