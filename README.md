### McDermott Network
[![Build Status](https://travis-ci.org/mcdermott-scholars/mcdermott.svg?branch=master)](https://travis-ci.org/mcdermott-scholars/mcdermott)
---

To run this app do:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

You will also need to install `memcached` for `sorl-thumbnail` to work. Look for instructions on how to install that onto your OS (for Ubuntu/Debian `sudo apt-get install memcached` should work). Also, when installing Pillow from pip make sure there is support for JPEG and ZLIB (PNG/ZIP). If it's not available, you will have to uninstall Pillow, enter the following commands (on Ubuntu/Debian), and reinstall Pillow:

```
sudo apt-get install libjpeg-dev
sudo apt-get install zlib1g-dev
sudo apt-get install libpng12-dev
```

If you can't get it to work, change `THUMBNAIL_DEBUG` to False in `mcdermott/settings.py`, which should ignore errors from that (you won't be able to see any thumbnails though). 

After someone pushes, you may need to run:

```
# If a dependency is added:
pip install -r requirements.txt
# If a model is changed:
python manage.py makemigrations
python manage.py migrate
# If another model is registered with Watson:
python manage.py buildwatson
```

To access the admin interface, run:

```
python manage.py createsuperuser
```

and point your browser to `http://localhost:8000/admin/`. You can also use this account to login to the app.

To seed the database with some default users, run:

```
python manage.py seed
```

You can edit the initial data seeded in `core/management/commands/seed.py`.
