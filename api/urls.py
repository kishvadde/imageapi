from django.conf.urls import url,include
from django.contrib import admin
from .views import ImageCreate,get_api_key,get_image
from .views import get_images,delete_image,ImageUpdate

app_name = 'api'

urlpatterns = [
    url(r'^create/$',ImageCreate.as_view()),
    url(r'^get-api-key',get_api_key,name='get_api_key'),
    url(r'^images/(?P<image_name>.*.(jpg|png|gif|jpeg|tif))/$',get_image),
    url(r'^images/$', get_images),
    url(r'^update/$',ImageUpdate.as_view()),
    url(r'^delete/$',delete_image),
]
