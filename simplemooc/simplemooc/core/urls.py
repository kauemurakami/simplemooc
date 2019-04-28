from django.conf.urls import include, url
from django.urls import path
from simplemooc.core import views
#importes importantes para funções medias
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

	path('', views.home, name='home'), #adicionado pagina inicial observe que estamos fazendo diretamente,
										# pois iportamos as views diratemente de core
	path('contato/', views.contact, name='contact'),
	#path(r'^',include('blog.urls')), #adicionado modularizando diferentes arquivos url
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)