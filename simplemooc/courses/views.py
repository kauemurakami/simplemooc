from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Course , Enrollment, Announcement, Lesson 
from .forms import ContactCourse , CommentForm
from .decorators import enrollment_required
from django.contrib.auth.decorators import login_required
# Create your views here. 
# index de courses
def index(request): 
	courses = Course.objects.all() #retornar todos os objetos cadastrados no banco de dados
	template_name = 'courses/index.html'
	context = { 'courses': courses} # variaveis que vao substituir valores dentro dele no caso um dicionario
	# disponibilizando assim courses no contexto da view index.html de app courses
	return render(request, template_name, context)

def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)
            form = ContactCourse()
    else:
        form = ContactCourse()
    context['form'] = form
    context['course'] = course
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
@enrollment_required
def announcements(request, slug):
	course = request.course
	template_name = 'courses/announcements.html'
	context = {'course':course , 'announcements':course.announcements.all(), }
	return render(request, template_name, context)

@login_required
@enrollment_required # trazendo o course dentro do request sempre que for usado
def show_announcement(request, slug, pk):
	course = request.course
	announcement = get_object_or_404(course.announcements.all(), pk=pk)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False) # recebe e cria o objeto MAS NÃO SALVA obs commit=FALSE
		comment.user = request.user
		comment.announcement = announcement
		comment.save()
		form = CommentForm()
		messages.success(request,'Comentário enviado com sucesso')
		return redirect('/cursos/'+slug+'/anuncios/'+str(pk))
	template_name = 'courses/show_announcement.html'
	context = {'course':course, 'announcement': announcement, 'form': form,}
	return render(request, template_name, context)

#listagem de aulas
@login_required
@enrollment_required
def lessons(request, slug):
	course = request.course
	template_name = 'courses/lessons.html'
	lessons = course.release_lessons()
	if request.user.is_staff:
		lessons = course.lessons.all()
	context = { 'course':course, 'lessons':lessons ,}
	return render(request, template_name, context)

# aula
@login_required
@enrollment_required
def lesson(request, slug, pk):
	course = request.course
	lesson = get_object_or_404(Lesson, pk=pk ,course=course) # inseguro pois o usuario pode manipular a url
	if not request.user.is_staff and not lesson.is_avaible(): # verifica se é staff e se a aula nao estadisponivel
		messages.error(request, 'Está aula não está disponível')
		redirect('courses/lessons.html', slug=course.slug)
	template_name = 'courses/lesson.html'
	context = { 'course':course, 'lesson':lesson ,}
	return render(request, template_name, context)


# material
@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('courses:lesson', slug=course.slug, pk=lesson.pk)
    if not material.is_embedded():
        return redirect(material.file.url)
    template = 'courses/material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material,
    }
    return render(request, template, context)

"""com busca apartir da pk
def details(request, pk): #pk é a variavel agrupada da expressão regular no url
	course = get_object_or_404(Course,pk=pk)
	context = {
		'course' :course
	}
	template_name = 'courses/details.html'
	return render(request, template_name, context)
	"""


