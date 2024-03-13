from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
from theblog.models import Profile, Venta, Post

#recuperar contraseña
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class CreateProfilePageView(CreateView):
	model = Profile
	form_class = ProfilePageForm
	template_name = "registration/create_user_profile_page.html"
	#fields = '__all__'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
	model = Profile
	template_name = 'registration/edit_profile_page.html'
	fields = ['bio', 'profile_pic', 'facebook_url', 'twitter_url', 'instagram_url']
	#success_url = reverse_lazy('edit_profile_page')
	
	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['bio'].label = 'Biografía'
		form.fields['profile_pic'].label = 'Cambiar foto perfil'
		return form
	def get_success_url(self):
		return reverse_lazy('edit_profile_page', kwargs={'pk': self.object.pk})

class ShowProfilePageView(DetailView):
	model = Profile
	template_name = 'registration/user_profile.html'

	def get_context_data(self, *args, **kwargs):
		#users = Profile.objects.all()
		context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
		page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
		context["portafolio"] = Post.objects.all()
		context["ventas_list"] = Venta.objects.all()
		context["page_user"] = page_user
		return context

class PasswordChangeView(PasswordChangeView):
	form_class = PasswordChangingForm
	template_name = 'password_change.html'
	fields = ('username', 'first_name', 'last_name', 'email')
	success_url = reverse_lazy('password_success')
	#success_url = reverse_lazy('home')

def password_success(request):
	return render(request, 'registration/password_success.html', {})

class UserRegisterView(generic.CreateView):
	form_class = SignUpForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
	form_class = EditProfileForm
	template_name = 'registration/edit_profile.html'
	success_url = reverse_lazy('home')

	def get_object(self):
		return self.request.user
	
def password_reset_request(request):
	if request.method == 'POST':
		password_form = PasswordResetForm(request.POST)

		if password_form.is_valid():
			data = password_form.cleaned_data['email']
			user_email = User.objects.filter(Q(email=data))

			if user_email.exists():
				for user in user_email:
					subject = 'Password Request'
					email_template_name = 'templates\registration\password_message.txt'
					parameters = {
						'email': user_email,
						'domain': '127.0.0.1:8000',
						'site_name': 'PostScribers',
						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
						'tokken': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					email = render_to_string(email_template_name, parameters)
					try:
						send_mail(subject, email, '', [user.email], fail_silently=False)

					except:
						return HttpResponse('Invalid header ')
					
					return redirect('')
	else:
		password_form = PasswordResetForm()
    
	context ={
		'password_form': password_form,
	}
	return render(request, 'users/password_reset.html', context)