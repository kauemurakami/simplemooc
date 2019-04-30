from django.urls import reverse
from simplemooc.accounts.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.dispatch   import receiver
from simplemooc.core.mail import send_mail_template


# curso custom
class CourseManager(models.Manager):
	#metodo pra facilitar filtros de pesquisas para consultas sql no caso pelo nome e descricao

	# a , entre os args significa um AND name__icontains = query , descrip...
			#para fazermos um OU devemos usar a função de models models.Q() | models.Q() | indicando o ou
	def search(self, query):
		return self.get_queryset().filter(models.Q(name__icontains=query)|models.Q(description__icontains=query))
		# get_queryset fornece os registros do banco de dados para este model
		# self.all() é apenas um atalho para self.get_queryset.all() para retornar todos os objetos
		# name é o atributo name definido na classe Course usando __iconstains verifica se contém alguma coincidencia de caracteres

# Create your models here.
#todos os modelos devem herdar models.Model
class Course(models.Model):
	"""docstring for Course"""

	#para que possamos utilizar os métodos da classe Course manager criaremos um objeto CourseManager()
	objects = CourseManager()

	#criando atributos
	name = models.CharField('Nome', max_length=100)
	#param1 a nivel de usuario 'texto utilitario para formulários e exibições'
	#@param2 max de caracteres
	
	slug = models.SlugField('Atalho') # tipo Slug é uma modificação do CharField
	# usaremos mais tarde pra acessar nossas url' ser usados em url's

	description = models.TextField('Descricao', blank = True)
	# um campo de charfield's mas sem tamanho máximo, usado pra campos maiores
	# @param2 infroma se o campo pode ficar em branco ou não / se é obrigatorio ou não
	
	# descrição mais longa
	about = models.TextField('Sobre o curso', blank = True)

	start_date = models.DateField('Data de Inicio', null = True, blank = True)
	# @param2 diferente de blank, significa que a nível de banco de dados ele pode ser null
	# @param3 define se o campo é obrigatório ou não
	
	#varaivel para imagens
	image = models.ImageField(upload_to = 'courses/images' ,verbose_name = 'Imagem', null = True, blank =True) 
	# @param1 é o local onde o arquivo será salva, caminho
	# inicialmente precisamos definir um MEDIA_ROOT EM NOSSO settings.py
	# o arquivo media root sera concatenado com nosso parâmetro verboso de upload_to
	# @param2 verbosa_name é o nome verboso da var
	
	created_at = models.DateTimeField('Criado em', auto_now_add = True)
	# @param2 toda vez que um arquivo for criado sera colocado automaticamente a data atual
	updated_at = models.DateTimeField('Atulizado em', auto_now = True)
	# @param2 toda vez que ele for salvo, a data sera alterada para a data atual
	
	#criando uma exibição melhorada para o usuario admin
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('courses:details', args=[self.slug])

	# consulta para retornar todas as aulas do curso disponiveis
	def release_lessons(self):
		today = timezone.now().date()
		return self.lessons.filter(release_date__lte=today) # filter __gte = MAIOR OU IGUAL


	#aqui melhoramos o modo como apresentamos o nome da nossa classe e o nome do seu objeto no admin panel
	class Meta:
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		#este atributo gere a ordenação nesse caso estamos ordenando pelo nome asc
		#se quisessemos ordenar pelo nome desc seria -name
		ordering = ['name']

# classe Aula
class Lesson(models.Model):
	name = models.CharField('Nome', max_length=100)
	description = models.TextField('Descricao', blank=True)
	number = models.IntegerField('Número (ordem)', blank=True, default=0) 	# numero para ordenação das aulas
	release_date = models.DateField('data de liberação',blank=True, null=True)

	# ligação com o curso
	course = models.ForeignKey(Course, verbose_name='Curso', on_delete=models.PROTECT, related_name='lessons')

	created_at = models.DateTimeField('Criado em',auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def __str__(self):
		return self.name

	# verifica se a aula ja esta disponivel de acordo com a data
	def is_avaible(self):
		if self.release_date:
			today = timezone.now().date()
			return self.release_date <= today
		return False

	class Meta:
		verbose_name= 'Aula'
		verbose_name_plural = ' Aulas'
		ordering=['-number']

# classe de conteudos/materiais
class Material(models.Model):
	name = models.CharField('Nome', max_length=100)
	embededd = models.TextField('Video Embededd', blank=True) # servir para colocar videos do youtube/vmeo/coisas em flash
	file = models.FileField(upload_to='lessons/materials', blank=True, null=True) # pasta de destino dos arquivos materiais

	# ligação com lição
	lesson = models.ForeignKey(Lesson, verbose_name='aula', on_delete=models.PROTECT, related_name='materials')

	def is_embededd(self):
		return bool(self.embededd)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Material'
		verbose_name_plural = 'Materiais'

# Inscrição no curso
class Enrollment(models.Model):
	# consjunto de opções uma tupla de tuplas 
	STATUS_CHOICES = {
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	}
	# possui um usuario como chave estrangeira
	# @param1 classe que irá para a relação @param2 atributo obrigatorio partir de 2.0, 
	# @param3 verbose name @param4 atributo que será criado na classe/model que recebe a FK...
	# para fazer uma busca relativa a essa classe (no caso Enrollments) 
	# para determinar a relação com a classe
	# ex usuario da classe Enrollment com o Usuario da classe Usuario
	user = models.ForeignKey(settings.AUTH_USER_MODEL, 
		verbose_name='Usuário',on_delete=models.PROTECT ,related_name='enrollments')
	course = models.ForeignKey(Course,
		verbose_name='Curso', on_delete=models.PROTECT,related_name='enrollments')
 	# status da inscrição, 1-liberada ou 2-não liberada etc, relacionada por um num int
	status = models.IntegerField('Situação', choices=STATUS_CHOICES, default=0, blank=True)
	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def active(self):
		self.status = 1
		self.save()

	def is_aproved(self):
		return self.status == 1
		

	class Meta:
 		verbose_name = 'Inscrição'
 		verbose_name_plural = 'Inscrições'
 		unique_together = (('user','course'),) #indices de unicidade ou seja, apenas um usuario, podera estar inscrito em um curso apenas uma vez
 							

#model de anuncio
class Announcement(models.Model):

	#fk para curso
	course = models.ForeignKey(Course, on_delete=models.PROTECT ,verbose_name='Curso', related_name='announcements')
	title = models.CharField('Titulo', max_length=100)
	content = models.TextField('Conteúdo')

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Anúncio'
		verbose_name_plural ='Anúncios'
		ordering = ['-created_at'] #ordenando em forma de pilha

#classe de comentarios
class Comment(models.Model):
	# reletad_name é o nome da relação que ira existir entre as duas tabelas, significa que um announcement pode
	# ter varios comentarios
	announcement = models.ForeignKey(Announcement, verbose_name='Anúncio', on_delete=models.PROTECT, related_name = 'comments')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT ,verbose_name='Usuário')
	comment = models.TextField('Comentário')
	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'
		ordering= ['created_at'] # forma de fila

# post_save
@receiver(models.signals.post_save, sender = Announcement, dispatch_uid='post_save_announcement') #sender classe de chamada, indica qual o model
def post_save_announcement(instance, created, **kwargs):
	if created:
		subject = instance.title
		context = { 'announcement': instance ,}
		template_name = 'courses/announcement_mail.html'
		enrollments = Enrollment.objects.filter(course=instance.course, status=1)
		for enrollment in enrollments:
			recipient_list = [enrollment.user.email]
			send_mail_template(subject, template_name,context, recipient_list)
