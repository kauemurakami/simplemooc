from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.urls import reverse
# Create your tests here.

# Seria a classe responsavel por testar a view home na nossa app core
# Quando criamos um testcase teremos de criar métodos que tenham o padrão test_<complemento>
class HomeViewTest(TestCase): # herdando de TestCase

	def test_home_status_code(self):
		client = Client() # recebemos o cliente
		response = client.get(reverse('core:home')) # recupera resposta dele para um get na pagina setada
		self.assertEqual(response.status_code, 200) # verifica a igualdade do status da response enviada se é == 200

	def test_home_template_used(self):
		client = Client() # recebemos o cliente
		response = client.get(reverse('core:home')) # recupera resposta dele para um get na pagina setada
		self.assertTemplateUsed(response, 'home.html') # verifica se o template utilizado é home
		self.assertTemplateUsed(response, 'home.html') # verifica se o template utilizado é home
