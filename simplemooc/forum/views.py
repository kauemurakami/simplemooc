from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView

from .models import Thread
# Create your views here.

#ListView herda de Template View logo todas as opções das duas classes estarao dispostas
class ForumView(ListView):
	
	model = Thread
	paginate_by = 2 #paginação de 10 em 10
	#template_name = '' 
	template_name = 'forum/index.html'

	# metodo que herda de ForumView, passando uma lista de parametros nomeados 
	# chamamos a função novamente da classe pai (Forum View) retornando o contexto do template
	def get_context_data(self, **kwargs):
		context = super(ForumView,self).get_context_data(**kwargs)
		context['tags'] = Thread.tags.all() # add /chama todas as tags associados a alguma instância dessa classe
		return context

	#obrigatorio passar o nome de um template, ou dentro da classe ou para o as_view()
#variavel index vai receber o resultado do forumview as view e retorna uma função
index = ForumView.as_view() #template name poderia vir aqui
#as_view() retorna uma função semelhante a nossas funções padrões que retornam um http response para renderizar uma template
