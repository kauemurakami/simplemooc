from django.contrib import admin
#importar model que queremos cadastrar no admin
from .models import Course, Enrollment, Announcement ,Comment 
# Register your models here.registra os models para ser reconhecidos pelo Django


# classe que vai representar as opções para personalizar o model admin
class CourseAdmin(admin.ModelAdmin):
	# o que vai ser exibido na pagina admin
	list_display = ['name', 'slug', 'start_date','created_at']
	# criação do campo para pesquisas
	search_fields = ['name', 'slug']
	# propriedade 
	prepopulated_fields = {'slug':('name',)} # aqui p slug vai ser baseado no nome do curso e sofrerá os replaces
											 # necessários para satisfazer o tipo slug


#registra o curso
admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment,Announcement,Comment])
