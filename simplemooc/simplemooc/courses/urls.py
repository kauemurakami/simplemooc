from django.conf.urls import include, url
from django.urls import path
from simplemooc.courses import views

app_name = 'courses'

urlpatterns = [

	path('', views.index, name='index'),
	#adicionando url's com o slug
	path('<slug:slug>/', views.details, name='details'),#w = conteudos alfanumericos _ e - o que pode coter no slug
	#path('<int:pk>/', views.details, name='details'), aqui estamos passando apenas a pk, ou chave do elemento curso
	#contem um agrupamento de expressão regular significa que é um parametro nomeado para formação de grupos
	#diz que deve entrar qualquer vaor regular inteiro e numero e tera um barra
	path('<slug:slug>/inscricao/', views.enrollment, name='enrollment'), #w = conteudos alfanumericos _ e - o que pode coter no slug
	path('<slug:slug>/cancelar-inscricao/', views.undo_enrollment, name='undo_enrollment'), #w = conteudos alfanumericos _ e - o que pode coter no slug
	path('<slug:slug>/anuncios/', views.announcements, name='announcements'), #w = conteudos alfanumericos _ e - o que pode coter no slug
	path('<slug:slug>/anuncios/<int:pk>', views.show_announcement, name='show_announcement'), #w = conteudos alfanumericos _ e - o que pode coter no slug

]
