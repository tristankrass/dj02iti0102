### Second assignment with Django
This is the final assignement of the first semester. Goal of
this project is to make a CMS like medium or something similar.
People can sign up with their discord or github account.
People can then write posts, follow people and comment under other users posts.

## Steps to get the project up and running.
####NB! You should have docker pre-installed on your machine.
First navigate to the root folder of the cloned folder.

Build initial image from a Dockerfile

✂ `docker build .`

Make migrations inside the container

✂ `docker-compose run web python /code/manage.py migrate`

Make superuser for the admin inside the container

✂ `docker-compose run web python /code/manage.py createsuperuser`

Last step

✂ `docker-compose up -d --build`

Type in `docker ps` and you should see two containers running:
    1 for django
    2 for postreSQL
---

Django should now be 🏃 on  http://127.0.0.1:8000/

---
# Database (Updated )
Database is now running on postreSQL and is configured via Docker.

## Tech stack
* [Python 3.7.1](https://www.python.org/)
* [Django 2.1](https://www.djangoproject.com/)
* [Bulma](https://bulma.io/)
* [SCSS](https://sass-lang.com/)
* [SQLLite3](https://www.sqlite.org/index.html)
* [django-allauth](https://github.com/pennersr/django-allauth)

### Please feel free to contribute 🙏

Initial project was provided by @rrebase.