from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'
urlpatterns=[
	url(r'^login/$', views.UserLoginView.as_view()),
	url(r'^home/(?P<username>[\d\w_]+)/$', views.home,name='home'),
	url(r'^profile/$', views.profile_redirect,name='profile_redirect'),
	#url(r'^(?P<username>[\d\w_]+)/profile/$', views.ProfileView1),
	url(r'^profile/(?P<username>[\d\w_]+)/$', views.update_profile,name='profile'),
]
