from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User 
from django import forms
from theblog.models import Profile

class ProfilePageForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio', 'profile_pic', 'facebook_url', 'twitter_url', 'instagram_url')

		widgets = {
			'bio': forms.Textarea(attrs={'class': 'form-control'}),
			'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
			'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
			'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super(ProfilePageForm, self).__init__(*args, **kwargs)
		self.fields['bio'].label = 'Biografía'
		self.fields['profile_pic'].label = 'Foto de Perfil'
		self.fields['facebook_url'].label = 'Facebook Url'
		self.fields['twitter_url'].label = 'Twitter Url'
		self.fields['instagram_url'].label = 'Instagram Url'


class SignUpForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Correo electrónico')
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Apellido')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'

class EditProfileForm(UserChangeForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Correo Electrónico')
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre')
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Apellido')
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Nombre de usuario')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
        # Ocultar el campo de contraseña
		self.fields['password'].widget = forms.HiddenInput()


class PasswordChangingForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Antigua'}), label='Contraseña Antigua')
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Nueva'}), label='Contraseña Nueva')
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Contraseña'}), label='Confirmar Contraseña')

	class Meta:
		model = User
		fields = ['old_password', 'new_password1', 'new_password2']

