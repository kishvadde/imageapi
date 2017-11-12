from django.conf.urls import url,include
from .views import home

app_name = 'home'

urlpatterns = [
    url('^$',home,name='home'),
]