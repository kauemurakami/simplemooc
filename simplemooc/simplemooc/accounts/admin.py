from django.contrib import admin
from .models import User
# Register your models here.registra os models para ser reconhecidos pelo Django

# classe que vai representar as opções para personalizar o model admin
class UserAdmin(admin.ModelAdmin):
	# o que vai ser exibido na pagina admin
	list_display = ['name', 'email', 'last_login','is_superuser','username','is_active']
	# criação do campo para pesquisas
	search_fields = ['name', 'username','email']
	# propriedade 

#registra o curso
admin.site.register(User, UserAdmin)

# Register your models here.
