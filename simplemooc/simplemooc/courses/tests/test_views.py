from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
# Create your tests here.
from django.conf import settings
from simplemooc.courses.models import Course # importando a classe que vai ser testada

#testando formularios
class ContactCourseTestCase(TestCase):
	
	def	setUp(self): # criando um curso
		self.course = Course.objects.create(name='Django', slug='django')

	def tearnDown(self):
		self.course.delete()

	#criando formulário de teste de erro
	def test_contact_form_error(self):
		data = {'name': 'Fulano de tal', 'email':'' ,'message':'' } # dadosq ue serao enviados para o formulário aqui voce pode formçar erros
		client = Client()
		path = reverse('courses:details', args=[self.course.slug])
		response = client.post(path, data)
		self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.') 
		self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.') 

	#criando formulário de teste de sucesso
	def test_contact_form_success(self):
		data = {'name': 'Kauê Tomaz', 'email':'kaue22@gmail.com' ,'message':'Oi' , } # dadosq ue serao enviados para o formulário aqui voce pode formçar erros
		client = Client()
		path = reverse('courses:details', args=[self.course.slug])
		response = client.post(path, data)
		self.assertEqual(len(mail.outbox ),1) # quantos email tem, tem de ter 1, no ambiente de teste os emails ficam em outbox
		self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL]) 
		
