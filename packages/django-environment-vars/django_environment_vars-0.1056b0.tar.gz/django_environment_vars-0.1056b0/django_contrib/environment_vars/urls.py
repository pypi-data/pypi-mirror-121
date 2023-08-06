from django.urls import path
from . import views

urlpatterns = (
     path('u', views.update_environment_variables),
    path('vars/', views.show_environment_variables),
    path('vars/<str:format>/', views.show_environment_variables, name='env-variables'),
    path('vars/<str:format>/<str:filename>', views.show_environment_variables, name='env-variables-filenme'),





)