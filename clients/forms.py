from django import forms
from django.contrib.auth.models import User
from .models import Client


"""""""""
constans
"""""""""
ERROR_MESSAGES_USER = {'required': 'El username es requerido',
		'unique' : 'El username ya existe',
		'invalid':	'El username es incorrecto'}
ERROR_MESSAGES_PASSWORD = {'required': 'La password es requerida'}
ERROR_MESSAGES_EMAIL = {'required': 'El campo email es requerido',
		'invalid': 'correo no valido'}



""""
function global para refactorizar clean_new_password
"""
def must_be_gt(value_password):
	if len(value_password)<3:
		raise forms.ValidationError('el password debe contener 5 caracteres')


"""""""""
class
"""""""""

class LoginUserForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=20, widget = forms.PasswordInput())

	def __init__(self, *args, **kwargs):
		super(LoginUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update( {'id': 'username_login' , 'class':'input_login' } )
		self.fields['username'].widget.attrs.update( {'id': 'password_login', 'class': 'input_login' } )


class CreateUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20, error_messages = ERROR_MESSAGES_USER)
	password = forms.CharField(max_length=20, error_messages= ERROR_MESSAGES_PASSWORD, widget = forms.PasswordInput())
	email = forms.CharField(error_messages= ERROR_MESSAGES_EMAIL)

	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({'id': 'username_create' })
		self.fields['password'].widget.attrs.update({'id': 'password_create' })
		self.fields['email'].widget.attrs.update({'id': 'email_create' })

	class Meta:
		model = User
		fields = ('username', 'password', 'email')


class EditUserForm(forms.ModelForm):
	username = forms.CharField(max_length=20, error_messages = ERROR_MESSAGES_USER)
	email = forms.CharField(error_messages= ERROR_MESSAGES_EMAIL)
	class Meta:
		model = User
		fields = ('username','email', 'first_name', 'last_name')


class EditPasswordForm(forms.Form):
	password = forms.CharField(max_length=20, error_messages= ERROR_MESSAGES_PASSWORD,
		widget = forms.PasswordInput())
	new_password = forms.CharField(max_length=20, error_messages= ERROR_MESSAGES_PASSWORD,
	 widget = forms.PasswordInput(), validators = [must_be_gt])
	repeat_password = forms.CharField(max_length=20, error_messages= ERROR_MESSAGES_PASSWORD,
	 widget = forms.PasswordInput(), validators = [must_be_gt])

	def clean(self):
		clean_data = super(EditPasswordForm,self).clean()
		password1 = clean_data.get('new_password')
		password2 = clean_data.get('repeat_password')
		if password1 != password2:
			raise forms.ValidationError('Las password no son los mismos')

	"""
	def clean_new_password(self):
		value_password = self.cleaned_data['new_password']
		if len(value_password)<5:
			raise forms	.ValidationError('el password debe contener 5 caracteres')
	"""

class EditClientForm(forms.ModelForm):
	class Meta:
		model = Client
		#fields = ('bio', 'job')
		exclude = ['user']
