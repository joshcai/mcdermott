### McDermott Network

---

Base app for authentication and API requests

To run this app do:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

After someone pushes, you may need to run:

```
# If a dependency is added:
pip install -r requirements.txt
# If a model is changed:
python manage.py makemigrations
python manage.py migrate
```

To access the admin interface, run:

```
python manage.py createsuperuser
```

and point your browser to `http://localhost:8000/admin/`. You can also use this account to login to the app.

To seed the database with some default users (NOTE: this will delete all original users), run:

```
python manage.py seed
```

You can edit the initial data seeded in `core/management/commands/seed.py`.