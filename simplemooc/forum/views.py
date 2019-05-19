from django.shortcuts import render , redirect
from django.views.generic import (TemplateView, View, ListView, DetailView)
from .forms import ReplyForm
from .models import Thread
from django.contrib import messages
# Create your views here.

#ListView herda de Template View logo todas as opções das duas classes estarao dispostas
class ForumView(ListView):
	
	paginate_by = 2 #paginação de 10 em 10
	#template_name = '' 
	template_name = 'forum/index.html'

	# uma das opções de customusação do listview
	# p indicar o que voce quer lista , pode-se passar um model como parametro, ou uma queryset
	def get_queryset(self):
		queryset = Thread.objects.all()
		order = self.request.GET.get('order', '') # recebe o parametro get e verifica se há algum parametro nomeado(dic) order
		if order == 'views': # verificando o parametro get
			queryset.order_by('-views') # ordenando deforma decrescente
		elif order == 'answers':
			queryset.order_by('-answers') # ordenando deforma decrescente

		tag = self.kwargs.get('tag', '')# o dic tag ou vazio
		if tag: # verifica se é a url com parametro tag ou a que não tem parametro
			queryset = queryset.filter(tags__slug__icontains=tag) # filtra tags que o sluga contem
		return queryset

	# metodo que herda de ForumView, passando uma lista de parametros nomeados 
	# chamamos a função novamente da classe pai (Forum View) retornando o contexto do template
	def get_context_data(self, **kwargs):
		context = super(ForumView,self).get_context_data(**kwargs)
		context['tags'] = Thread.tags.all() # add /chama todas as tags associados a alguma instância dessa classe
		return context

# herda de outra genericview
class ThreadView(DetailView): # por padrão procura parametros nomeados slug ou pk

	model = Thread
	template_name = 'forum/thread.html'
	
	#contexto do template
	def get_context_data(self, **kwargs):
		context = super(ThreadView, self).get_context_data(**kwargs)
		context['tags'] = Thread.tags.all() # add /chama todas as tags associados a alguma instância dessa classe
		context['form'] = ReplyForm(self.request.POST or None) # tenta validar o formulario / se esta vazio se for none não é valido, só vamos prencher se for um queest  post e estiver preenchido
		return context

	def post(self, request, *args, **kwargs):

		# verificamos se esta logado
		if not self.request.user.is_authenticated:
			messages.error(self.request, 'Faça o Login para responder a um tópico')
			return redirect(self.request.path)

		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		form = context['form']
		if form.is_valid():
			reply = form.save(commit=False) #preenche os dados do formulário no objeto
			reply.thread = self.request.user
			reply.author = self.request.user
			reply.save()
			messages.success(self.request, 'A sua resposta foi enviada com sucesso')
			context['form'] = ReplyForm() # esvaziando formulário 
			
		return self.render_to_response(context)



	#obrigatorio passar o nome de um template, ou dentro da classe ou para o as_view()
#variavel index vai receber o resultado do forumview as view e retorna uma função
index = ForumView.as_view() #template name poderia vir aqui
#as_view() retorna uma função semelhante a nossas funções padrões que retornam um http response para renderizar uma template
thread = ThreadView.as_view()

