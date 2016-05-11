from django.conf.urls import url

from . import views

app_name = 'lists'

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
]