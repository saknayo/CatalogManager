from django.conf.urls import url
from django.urls import reverse
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

app_name = 'user'
urlpatterns=[
	url(r'^login/$', views.UserLoginView.as_view(), name='login'),
    url(r'^register/$', CreateView.as_view(
            template_name='user/register.html',
            form_class=UserCreationForm,
            success_url='/user/home'),
            name='register'),
    url(r'^change_password/$', views.change_password, name='change_password'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^home/$', views.home,name='home'),
	url(r'^profile/$', views.profile_redirect,name='profile_redirect'),
	#url(r'^(?P<username>[\d\w_]+)/profile/$', views.ProfileView1),
	url(r'^profile/(?P<username>[\d\w_]+)/$', views.update_profile,name='profile'),
	url(r'^userexport/$', views.userexport , name='userexport'),
]
