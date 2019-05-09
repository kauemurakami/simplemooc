from django.shortcuts import render
from django.generic import TemplateView, View, ListView
# Create your views here.

class ForumView(TemplateView):
	
	model = Thread
	paginate_by = 10 #paginação de 10 em 10
	#template_name = '' 

	#obrigatorio passar o nome de um template, ou dentro da classe ou para o as_view()
#variavel index vai receber o resultado do forumview as view e retorna uma função
index = ForumView.as_view(template_name = 'forum/index.html')
#as_view() retorna uma função semelhante a nossas funções padrões que retornam um http response para renderizar uma template
