import re # importando o re do regex
from django.db import models
from django.core import validators #para usar a função de validação para o username
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,UserManager
from django.conf import settings

# Create your models here.
class User(AbstractBaseUser,PermissionsMixin):

	username = models.CharField('Nome de usuário', max_length=30, unique=True, 
		validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),'Nome de usuário só pode conter letras, números ou @ . + - _','invalid')]
		)
	email = models.EmailField('E-mail',unique=True)
	name = models.CharField('Name',max_length=60, blank=True)
	is_active = models.BooleanField('Está ativo?',blank=True, default=True) # para verificar se pode logar ou não
	is_staff = models.BooleanField('É da equipe?',blank=True, default=False)
	date_joined = models.DateTimeField('Data de entrada', auto_now_add=True) #quando o model for salvo pela primeira vez será a hora atual
	
	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.name or self.username

	def get_short_name(self):
		return self.username

	def full_name(self):
		return str(self)

	class Meta:
		verbose_name = 'Usuário'
		verbose_name_plural = 'Usuários'

#cria chave unica randomica para recuperação de senha
class PasswordReset(models.Model):
	from simplemooc.core.utils import generate_hash_key
	from simplemooc.core.mail import send_mail_template

	#user associado, solicitante
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário',on_delete=models.PROTECT,related_name='resets') # associa o usuario

	key = models.CharField('Chave', max_length=100, unique=True)
	created_at = models.DateTimeField('Criado em', auto_now_add=True) # vamos usar um intervalo de prazo pra um controle
	confirmed = models.BooleanField('Confirmado?', blank=True, default=False)

	def __str__(self):
		return '{0}em{1}'.format(self.user,self.created_at)

	class Meta:
		verbose_name = 'Nova senha'
		verbose_name_plural = 'Novas Senhas'
		#ordering = {'-created_at'} # ordena em ordem decrescente por criação de nova senha
