from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.utils.http import is_safe_url
from django.views import generic
from django.urls import reverse
from django.db import transaction
from django import forms as djforms
from django.contrib import messages

from .models import Profile
from forms.models import Status,Infos

# Create your views here.
class UserLoginView(LoginView):
    template_name = 'user/login.html'

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('user:login'))

@login_required
def profile_redirect(request):
    url = reverse('user:profile',args=(request.user.username,))
    url = reverse('user:home'   ,args=(request.user.username,))
    #url = '/user/%s/profile' % request.user.username
    return HttpResponseRedirect(url)

class ProfileView(LoginRequiredMixin,generic.DetailView):
    model = Profile
    template_name = 'user/profile.html'

@login_required
def ProfileView1(request,username):
    profile=get_object_or_404(User,username=username)
    return render(request,'user/profile.html',{'user':profile})
    return HttpResponse()
#@login_required
#def update_profile(request, user_name):
#    user = User.objects.get(username=user_name)
#    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#    user.save()


class UserForm(djforms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(djforms.ModelForm):
    class Meta:
        model = Profile
        fields = ('url', 'location', 'company', 'user_level')

@login_required
@transaction.atomic
def update_profile(request,username):
    viewer=request.user
    user  =get_object_or_404(User,username=username)
    if 'next' in request.POST and request.method == 'POST':
        next_url = request.POST.get('next','')
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        if is_safe_url( next_url ) or 1 :
            return HttpResponseRedirect(next_url)
    if user == viewer or viewer.profile.user_level >=7 :
        permisson = viewer.profile.user_level
    else:
        permisson = -1

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse('user:profile',args=(username,)))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
    return render(request, 'user/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'permisson': permisson,
    })

###### user home page (private)
''' 
include profile shortcut,
        apply table list(normal users can only see tables created by themself) ,
        user list(only visable to admin)
'''
@login_required
def home(request,username):
    template_name = 'user/home.html'
    #user=User.objects.get(username=username)
    user  =get_object_or_404(User,username=username)
    if request.user != user :
        raise Http404("User's infomation is protected!")

    if user.profile.user_level>=7 :
        userset=User.objects.order_by('-last_login')[:10]
    else :
        userset=User.objects.filter(username=user.username)

    if user.profile.user_level < 3 :
        infosset=Status.objects.filter(creator=user).order_by("-create_time")[:10]
    else :
        infosset=Status.objects.exclude(creator__isnull=True).exclude(info__isnull=True).order_by("-create_time")[:10]
    #for i in infosset:
    #    username = i.creator.username

    return render(request,template_name,{'userset':userset,'infosset':infosset,})

