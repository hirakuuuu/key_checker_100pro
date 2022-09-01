from . import views
from django.urls import path

app_name = 'bot'

urlpatterns = [
    path('', views.callback, name='callback'), # djangobot/urls.pyに呼び出され、views.pyのcallback関数を呼び出す
]