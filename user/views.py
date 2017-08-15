from django.shortcuts import get_object_or_404, render,render_to_response, redirect
from django.contrib.auth import logout,update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
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
    url = reverse('user:home')   
    #url = '/user/%s/profile' % request.user.username
    return HttpResponseRedirect(url)

@login_required
def change_password(request):
    template_name='user/change_password.html'
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, template_name, {
        'form': form
    })

@login_required
def set_password(request,username):
    template_name='user/set_password.html'
    if request.user.profile.user_level >= 7 and request.user.username != username:
        user=User.objects.get(username=username)
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('user:home')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = SetPasswordForm(user)
        return render(request, template_name, {
            'form': form
        })

class ProfileView(LoginRequiredMixin,generic.DetailView):
    model = Profile
    template_name = 'user/profile.html'


#@login_required
#def update_profile(request, user_name):
#    user = User.objects.get(username=user_name)
#    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#    user.save()


class UserForm(djforms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')

class ProfileForm(djforms.ModelForm):
    class Meta:
        model = Profile
        #fields = ('url', 'location', 'company', 'user_level')
        fields = ( 'user_level',)

@login_required
@transaction.atomic
def update_profile(request,username):
    viewer=request.user
    user  =get_object_or_404(User,username=username)

    if user == viewer or viewer.profile.user_level >=7 :
        permisson = viewer.profile.user_level
    else:
        permisson = -1
        
    if 'next' in request.POST and request.method == 'POST':
        next_url = request.POST.get('next','')
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        if is_safe_url( next_url ) or 1 :
            return HttpResponseRedirect(next_url)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            #return HttpResponseRedirect(reverse('user:profile',args=(username,)))
            return HttpResponseRedirect(reverse('user:home'))
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
def home(request):
    template_name = 'user/home.html'
    #user=User.objects.get(username=username)
    user  = request.user

    if user.profile.user_level>=7 :
        userset=User.objects.order_by('-last_login')
    else :
        userset=User.objects.filter(username=user.username)

    if user.profile.user_level < 3 :
        infosset=Status.objects.filter(creator=user).order_by("-create_time")
    else :
        infosset=Status.objects.exclude(creator__isnull=True).exclude(info__isnull=True).order_by("-create_time")
    #for i in infosset:
    #    username = i.creator.username

    return render(request,template_name,{'userset':userset,'infosset':infosset,})

class UserForm2(djforms.ModelForm):
    class Meta:
        model = User  
        fields=('username','password')

def register(request):
    if request.method == 'POST':
        uf = UserForm2(request.POST, prefix='user')
        #upf = UserProfileForm(request.POST, prefix='userprofile')
        if uf.is_valid() :#* upf.is_valid():
            user = uf.save()
            #userprofile = upf.save(commit=False)
            #userprofile.user = user
            #userprofile.save()
            return redirect('user:login')
    else:
        uf = UserForm2(prefix='user')
        #upf = UserProfileForm(prefix='userprofile')
    return render(request,'user/register.html', 
                                                { 'userform':uf,},
                                                    #userprofileform=upf),
                                               )
@login_required
def userexport(request):
    import csv
    from django.utils.encoding import smart_str
    queryset=User.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Username"),
        smart_str(u"Location"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.username),
            smart_str(obj.first_name),
        ])
    return response 
