from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
# Create your tests here.
from django.conf import settings

#importando model_mommy para criação de nossos models
from model_mommy import mommy

from simplemooc.courses.models import Course # importando a classe que vai ser testada

# teste custom manage
class CourseManagerTestCase(TestCase):

	def setUp(self):
		# comando mommy.make() para criar o model de teste
		# @param1 <nome-da-app> . @param2 <nome-do-model> ,@param3 nome fixo, ou seja não gerara vaores aleatorios para esse atributo @param4 quantidade de model aleatório que quer criar
		self.courses_django = mommy.make('courses.Course', name='django' , _quantity=10)
		self.courses_php = mommy.make('courses.Course', name='php' , _quantity=10)
		self.client = Client()

	def tearnDown(self):
			Course.objects.all().delete()

	def test_course_search(self):
		search = Course.objects.search('django') # verificando o metodo search de CourseManager pesquisando por 'django' nome fixo na criação do objeto
		self.assertEqual(len(search), 10) # aqui estamos dizendo que depois de criar 10 objetos 
											# a variavel search deve conter 10 objetos instanciados com nome 'django'
		searc =Course.objects.search('php')
		self.assertEqual(len(search), 10)

		# aqui estamos testando pela quantidade de objetos, se criarmos 5 objetos tem que nos treotnar os 5