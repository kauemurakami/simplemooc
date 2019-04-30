from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Course, Enrollment

# reutilizameremos o código sempre que formos verificar se um usuario está inscrito no curso
# funciona da mesma maneira que o @login_required
def enrollment_required(view_func):
	# @param 1 request , @param2 args @param3 dic de valores
	def _wrapper(request, *args, **kwargs):
		slug = kwargs['slug']
		course = get_object_or_404(Course, slug=slug) # recebe um curso comparando os slugs ou retorna um erro
		has_permission = request.user.is_staff # verifica se o usuario logado é staff (administrador)
		if not has_permission: # caso o usuario não seja um administrado ...
			try: # tente 
				# recebe a inscrioção do usuário inscrito se o usuario logado estiver cadastrado no curso passado
				enrollment = Enrollment.objects.get(user = request.user, course=course)
			except Enrollment.DoesNotExist: # não existe e retorno a message de erro abaixo
				message = 'Desculpe, mas você não tem permissão para acesar essa página'
			else:
				if enrollment.is_aproved(): # verifica se o usaurio da inscrição esta com o status=1 (aprovada)
					has_permission = True
				else: # retorna uma mensagem de erro que sua situação pode estar pendente
					message = 'A sua inscrição no curso ainda esta pendente'

		# a duplicidade deste if no caso, é dado caso o usuario seja staff
		# neste if não seria necessario passar pela busca de uma inscrição
		if not has_permission:
			messages.error(request, message)
			return redirect('accounts:dashboard')
		request.course = course # inclui o atributo course ao request ,
		# toda view que usar esse decorator tera um course disponivel no request
		return view_func(request, *args, **kwargs) # retorna a função com os parametros preenchidos ...
		# da view que deve ser executada
	return _wrapper # retornando função _wrapper
