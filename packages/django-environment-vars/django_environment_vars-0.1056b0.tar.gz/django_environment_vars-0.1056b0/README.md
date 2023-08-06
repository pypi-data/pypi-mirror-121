
# how to use

Installl
```

pip install django-environment-vars

```
1. Add config files


```
  INSTALLED_APPS = [...
          'django_contrib.environment_vars ',
      ]


```

2. Include the app URLconf in your project urls.py like this::


```
path('env/', include('django_contrib.environment_vars.urls'))

```


3. Start the development server and visit http://127.0.0.1:8000/env/


4. Or Visit demo site https://bygregonline.github.io/react_env_sample/

