from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import PasswordReset

User = get_user_model()

#formulário de registro
class RegisterForm(forms.ModelForm):
	
	#recuperando campo senha e confirmação de senha	
	password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				'A confirmação de senha não está correta',
				code='password_mismatch'
				)
		return password2

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False) # apenas retorna o usuario pois o commit esta como false
		# recupero o usuario e
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user
		
	class Meta:
		model = User
		fields = ['username', 'email']

#formulario de edição
class EditAccountForm(forms.ModelForm): # models.Form formulario especifico do modelo e gerar o formulario baseado nos campos existentes no model
	
	#pra saber qual o model que o usuario ira precisar criaremos uma classe meta
	class Meta:
		model = User #define qual model se basear
		fields = ['username','email','name'] #define quais campos do model realmente serão usados

class PasswordResetForm(forms.Form): # um form comum pois não esta associado a nenhum model inicialmente
	email = forms.EmailField(label='Digite seu Email')	

	def clean_email(self): #verificar se o usuario é realemtne valido
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			return email
		raise forms.ValidationError('O email não existe em nosso sistema')
	
	def save(self):
		user = User.objects.get(email=self.cleaned_data['email'])
		key = PasswordReset.generate_hash_key(user.username)
		reset = PasswordReset(key=key, user=user)
		reset.save()
		template_name = 'accounts/password_reset_mail.html'
		subject = 'Criar nova senha '
		context = {'reset' : reset,}
		PasswordReset.send_mail_template(subject, template_name, context, [user.email])