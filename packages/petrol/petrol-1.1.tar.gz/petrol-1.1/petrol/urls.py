from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [

    #path('',views.index ),
    path("upload/" , views.upload ,name='upload'),
    url(r"^$" , views.index , ),
    #path(r"output" , views.output , name = 'output'),
    url(r"download" , views.download , name = 'download'),
    url(r"example/" , views.example , name = 'example'),
    url(r"app/" , views.app , name = 'app'),
]