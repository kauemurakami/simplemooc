from django.conf.urls import include, url
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from simplemooc.accounts import views

app_name = 'accounts'

urlpatterns = [
	path( '', views.dashboard , name='dashboard' ),	
	path( 'entrar/', LoginView.as_view(template_name='accounts/login.html') , name='login' ),
	path( 'cadastrar-se/', views.register , name='register' ),
	path( 'editar/', views.edit , name='edit' ),
	path( 'sair/', LogoutView.as_view(next_page='core:home') , name='logout' ),
	path( 'editar-senha/', views.edit_password , name='edit_password' ),
	path( 'nova-senha/', views.password_reset , name='password_reset' ),
	path('confirmar-nova-senha/<key>/', views.password_reset_confirm, name='password_reset_confirm')
	
	#adicionando url's com o slug
]
