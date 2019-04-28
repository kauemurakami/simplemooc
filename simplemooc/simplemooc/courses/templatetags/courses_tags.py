from django import template
# usado para registrar as tags
register = template.Library()

from simplemooc.courses.models import Enrollment
# importando as inscrições


# decorator para registrar
@register.inclusion_tag('courses/templatetags/my_courses.html')
# função que recebe @param1 um usuario e retorna suas inscrições
def my_courses(user):
	# recupera o objeto curso verificando se o usuario logado é um usuario ligado a algum curso
	enrollments = Enrollment.objects.filter(user=user)
	context = { 'enrollments' : enrollments ,}
	return context
	
@register.inclusion_tag('courses/templatetags/my_courses_dashboard.html')
def my_courses_dash(user):
	# recupera o objeto curso verificando se o usuario logado é um usuario ligado a algum curso
	enrollments = Enrollment.objects.filter(user=user)
	context = { 'enrollments' : enrollments ,}
	return context
"""
# um modo de enviar uma custom tag mais simples que a anterior
@register.simple_tag
def load_my_courses(user):
	return Enrollment.objects.filter(user=user)
"""