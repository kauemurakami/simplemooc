from django.conf.urls import include, url
from django.urls import path
from simplemooc.courses import views

urlpatterns = [

	path('', views.index, name='index'), 

]