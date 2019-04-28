from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Course , Enrollment, Announcement
from .forms import ContactCourse , CommentForm
from django.contrib.auth.decorators import login_required
# Create your views here. 
# index de courses
def index(request): 
	courses = Course.objects.all() #retornar todos os objetos cadastrados no banco de dados
	template_name = 'courses/index.html'
	context = { 'courses': courses} # variaveis que vao substituir valores dentro dele no caso um dicionario
	# disponibilizando assim courses no contexto da view index.html de app courses
	return render(request, template_name, context)

def details(request, slug): #slug é a variavel que é criada na criação d ocurso definindo um url
	course = get_object_or_404(Course, slug=slug)
	if request.method == 'POST': #verifica se a requisição é post ou get com o metodo .method
		form = ContactCourse(request.POST) # dicionario com todos os campos inseridos no formulario
		if form.is_valid():
			is_valid = True  # verifica se o formulario recebido é valido
			form.send_mail(course,)
			print(form.cleaned_data)
			# ou acesando pelos indices
			print(form.cleaned_data['email'])
			print(form.cleaned_data['name'])
			form = ContactCourse() # limpando o formulario
	else:
		form = ContactCourse()
		is_valid = False
	context = {	
		'course' : course,
		'form' : form ,
		'is_valid' : is_valid
		}
	template_name = 'courses/details.html'
	return render(request, template_name, context)

@login_required
def enrollment(request,slug):
	course = get_object_or_404(Course, slug=slug)
	# @param1 filter no caso o usuario atual  @param2 curso
	# @var1 recebe a tupla caso seja criada @var2 retorna um bool se foi criada ou não
	enrollment, created = Enrollment.objects.get_or_create(user=request.user,course=course)
	if created:
		enrollment.active()
		messages.success(request, 'Você foi inscrito no curso com suceso') #@param 2 mesnagem
	else:
		messages.info(request,'Você já está inscrito no curso') 
	# estas mensagens serão passadas para a pagina que estiver sendo redirecionada pelo redirect()
	# o message para para o template por padrão com a variavel messages que foram configuradas na view
	return redirect('accounts:dashboard')

#cancelar inscrição
@login_required
def undo_enrollment(request, slug):
	#recupera o curso com o @param slug
	course = get_object_or_404(Course, slug=slug)
	#verifica se existe a inscrição do usuario atual no curso em questão
	enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
	if request.method == 'POST':
		enrollment.delete()
		messages.success(request, 'Sua inscrição foi cancelada')
		return redirect('accounts:dashboard')
	context = { 'enrollment': enrollment, 'course':course,}
	template_name = 'courses/undo_enrollment.html'
	return render(request, template_name, context)

#anuncios
@login_required
def announcements(request, slug):
	course = get_object_or_404(Course, slug=slug)
	#verifica se o usuario é um staff ou não (admin)
	if not request.user.is_staff: 
		enrollment = get_object_or_404(Enrollment, user=request.user,course=course) # busca a inscrição do aluno
		#ou retorna a inscriçõa ou erro caso não esteja inscrito  no curso
		if not enrollment.is_aproved():
			messages.error(request, 'Sua inscrição está pendente')
			return redirect('accounts:dashboard')
	template_name = 'courses/announcements.html'
	context = {'course':course , 'announcements':course.announcements.all(), }
	return render(request, template_name, context)

@login_required
def show_announcement(request, slug, pk):
	course = get_object_or_404(Course, slug=slug)
	#recupera formulario CommentForm
	#verifica se o usuario é um staff ou não (admin)
	if not request.user.is_staff: 
		enrollment = get_object_or_404(Enrollment, user=request.user,course=course) # busca a inscrição do aluno
		#ou retorna a inscriçõa ou erro caso não esteja inscrito  no curso
		if not enrollment.is_aproved():
			messages.error(request, 'Sua inscrição está pendente')
			return redirect('accounts:dashboard')
	announcements = get_object_or_404(course.announcements.all(), pk=pk)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False) # recebe e cria o objeto MAS NÃO SALVA obs commit=FALSE
		comment.user = request.user
		comment.announcement = announcements
		comment.save()
		form = CommentForm()
		messages.success(request,'Comentário enviado com sucesso')
	template_name = 'courses/show_announcement.html'
	context = {'course':course, 'announcement': announcement, 'form': form,}
	return render(request, template_name, context)

"""com busca apartir da pk
def details(request, pk): #pk é a variavel agrupada da expressão regular no url
	course = get_object_or_404(Course,pk=pk)
	context = {
		'course' :course
	}
	template_name = 'courses/details.html'
	return render(request, template_name, context)
	"""


