### Second assignment with Django
This is the final assignement of the first semester. Goal of 
this project is to make a CMS like medium or something similar. 
People can sign up with their discord or github account. 
People can then write posts, follow people and comment under other users posts. 

## Steps to complete when running the project.
✂ pipenv install --python 3.7.1

✂ pipenv shell

✂ python manage.py migrate

✂ python manage.py createsuperuser

✂ python manage.py runserver 

## Tech stack
* [Python 3.7.1](https://www.python.org/)
* [Django 2.1](https://www.djangoproject.com/)
* [Bulma](https://bulma.io/) 
* [SCSS](https://sass-lang.com/)
* [SQLLite3](https://www.sqlite.org/index.html)
* [django-allauth](https://github.com/pennersr/django-allauth)


#### Database
Database is currently sqlite3 which is not suitable as a production 
database, but is fine for local development. To make the app production 
ready please consult the docs for changing the database engine of your choice.

### Please feel free to contribute 🙏 
