from django.contrib import admin
#importar model que queremos cadastrar no admin
from .models import Course, Enrollment, Announcement ,Comment ,Lesson, Material
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

# inline model admin
# isso possibilita que, quando formos inserir uma aula, possamos também inserir um material no memso contexto
class MaterialInlineAdmin(admin.TabularInline):
	model = Material


#custom admin 
class LessonAdmin(admin.ModelAdmin):
	# O que vai ser exibido no nosso admin aula
	list_display = ['name', 'number', 'course','release_date']
	# Campos de pesquisa
	search_fields = ['name', ' description']
	# filtragem lateral ordenando pela data
	list_filter = ['created_at']

	# recupera a lista de conteudos que devem ser adicionadas no contexto de adicionar uma aula(Lesson)
	# no nosso caso é o Material que esta referenciado como model em MaterialInlineAdmin
	# isso nos gera uma lista de formularios materiais
	inlines = [MaterialInlineAdmin]


#registra o models no admin
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register([Enrollment,Announcement,Comment, Material])

