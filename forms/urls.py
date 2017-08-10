from django.conf.urls import url
from . import views

app_name = 'forms'
urlpatterns=[
	url(r'^create/$',views.create_view,name='create'),
	url(r'^edit/(?P<pk>\d+)/$',views.edit_view,name='edit'),
	url(r'^index/$', views.index_view,name='index')
]
