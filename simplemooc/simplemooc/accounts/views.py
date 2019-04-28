from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm,
    SetPasswordForm)
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset
from simplemooc.courses.models import Enrollment

User = get_user_model()

# Create your views here.

def register(request):
	template_name = 'accounts/register.html'
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			# user.password não é a senha já é a senha criptografada do usuario no banco entao devemos usar a senha do form
			user = authenticate(username = user.username, password = form.cleaned_data['password1'])
			login(request,user) # coloca o usuario na sessão user fica disponivel em todos os templates como uma session php
			return redirect('core:home')
	else:
		form = RegisterForm()
	context = { 'form' : form
		}
	return render(request, template_name,context)

# usando esse o decarator para verificar se o usuario realmente estiver logado
# sera executado sempre que dashbard for chamado
# o redirecionamento é para o link que esta definido na sua setting URL_REDIRECT
@login_required 
def dashboard(request):
	template_name = 'accounts/dashboard.html'
	return render(request,template_name)

#Não precisamos criar o form de edição de senha pois o django ja fornece, torna-se necessário apenas a criaão da view
@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html'
	context = {}
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			user = form.save()
			from django.contrib.auth import update_session_auth_hash
			update_session_auth_hash(request, user) #atualiza a seção pro usuario não ser desconectado
			context['success'] = True
	else:
		form = PasswordChangeForm(user=request.user)#não é necessario passar
	context['form'] = form
	return render(request, template_name, context)

@login_required
def edit(request):
	template_name = 'accounts/edit.html'
	context = {}
	if request.method == 'POST':
		form = EditAccountForm(request.POST, instance=request.user) # recebe os dados post e cria o formulário baseado nadefinição da classe forms
		if form.is_valid():
			form.save()
			messages.success(request, 'Os dados foram alterados com sucesso')
			return redirect('accounts:dashboard')
	else:
		form = EditAccountForm(instance=request.user)
	context['form'] = form
	return render(request, template_name, context)

# requerindo nova senha
def password_reset(request):
	success = False
	template_name = 'accounts/password_reset.html'
	form = PasswordResetForm(request.POST or None) #or None significa que se request.POST == vazio ele é false então fica em branco
	# por mais que esteja vazio, você tentou preencher, 
	#logo ou o formulario recebera os dados ou ele irá vazio não se mostrando necessario o uso de 
	#condições como no método acima
	if form.is_valid():
		form.save()
		success = True
	context = {'form' : form , 'success':success}
	return render(request, template_name, context)

# confirmando nova senha
def password_reset_confirm(request, key):
	success = False
	template_name = 'accounts/password_reset_confirm.html'
	reset = get_object_or_404(PasswordReset, key=key)
	form = SetPasswordForm(user=reset.user,data=request.POST or None)
	if form.is_valid():
		form.save()
		success = True
	context = {'form' : form , 'success':success}
	return render(request, template_name, context)