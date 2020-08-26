# StarWarsApi-Django
An API with Django in conjuntion with the SWAPI.

## Requirements:

* Django 3.0.5
* Django RestFramework 3.11.1
* Python-decouple 3.3
* Requests 2.24.0


## Getting started

First create a virtual enviroment with python as following:

* python3 -m venv "venv-name"

And then activate it with:

* source venv-name/bin/activate

If you do not have the python virtual enviroment in your system, install it with:

* pip install virtualenv

Then install of the requirements written in the "requirements.txt" file with pip as following:

* pip install -r requirements.txt

Finally to run the server, on the console:

* python manage.py makemigrations
* python manage.py migrate
* python manage.py runserver 0.0.0.0:8000

To run the unit tests type:

* python manage.py test

And that's it!!

For the documentation on how to use the endpoints refer to the following link:

https://documenter.getpostman.com/view/10760574/TVCZaWYP
