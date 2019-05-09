from django.conf.urls import include, url
from django.urls import path
from simplemooc.forum import views

urlpatterns = [

	path('', views.index, name='index'), 

]