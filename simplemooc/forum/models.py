from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
# Create your models here.

class Thread(models.Model):

	title = models.CharField('Titulo', max_length=100)
	body = models.TextField(u'Mensagem')
	#related_name='cria a referencia para autor para todos os topicos que ele criou'
	author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads')

	views = models.IntegerField('Vizualizações', blank=True, default=0)
	answers = models.IntegerField('Respostas', blank=True, default=0)

	tags = TaggableManager()

	created = models.DateTimeFormat('Criado em', auto_now_add=True)
	modified = models.DateTimeFormat('Modificado em', auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Tópico'
		verbose_name_plural = 'Tópicos'
		ordering = ['-modified']

#model responsavel pela resposta
class Reply(models.Model):

	reply = models.TextField('Mensagem')
	author = models.ForeignKey( settings.AUTH_USER_MODEL,
		verbose_name = 'Autor', related_name = 'replies'
		)
	correct = models.BooleanField('Correta?', blank=True, default=False)

	created = models.DateTimeFormat('Criado em', auto_now_add=True)
	modified = models.DateTimeFormat('Modificado em', auto_now=True)

	def __str__:
		return self.reply[:100] #retorna as primeiras 100 palavras da resposta

	class Meta:
		verbose_name = 'Resposta'
		verbose_name_plural = 'Respostas'
		ordering = ['-correct' , 'created']