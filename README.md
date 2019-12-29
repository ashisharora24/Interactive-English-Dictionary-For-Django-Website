# Interactive-English-Dictionary-For-Django-Website

this app can be directly attached to your django website

you need to follow the below instructions in order to use this

1. download the project
2. place the project directly inside your django project 
3. inside your settings.py  add interactive_english_dictionary under INSTALLED_APPS

example: 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'interactive_english_dictionary',
]


4. create a link in your website:
<a href="/interactive_english_dictionary/">Interactive English Dictionary</a>

5. run makemigrations and migrate commands

6. the application is up and running 