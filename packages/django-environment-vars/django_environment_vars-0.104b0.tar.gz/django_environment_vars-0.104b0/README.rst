=====
TODO
=====

Polls is a Django app to conduct Web-based polls. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_contrib.environment_vars ',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('env/', include('django_contrib.environment_vars.urls'))

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/env/
   to create a poll (you'll TODO).

5. Visit http://127.0.0.1:8000/env/

6. visit demo site https://bygregonline.github.io/react_env_sample/

