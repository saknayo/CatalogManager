from django.shortcuts import redirect,get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Infos,Status,Historys
from django import forms
import re
from collections import OrderedDict

# Create your views here.
class InfosForm(forms.ModelForm):
	class Meta:
		model  = Infos
		fields = '__all__'

def submission_export(queryset,filename='mydata.csv'):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow( [ smart_str(field.name) for field in queryset[0] ] )
    for obj in queryset:
	    writer.writerow( [ smart_str(field.value()) for field in obj ] )
    #writer.writerow([
    #    smart_str(u"InfoID"),
    #    smart_str(u"Creator"),
    #    smart_str(u"Create_time"),
    #])
    #for obj in queryset:
    #    writer.writerow([
    #        smart_str(obj.pk),
    #        smart_str(obj.status.creator.username),
    #        smart_str(obj.status.create_time),
    #    ])
    return response 

def get_selected_ids(post_dict):
	id_p=re.compile(r'info_(?P<id>\d+)$')
	return [int(id_p.search(k).group('id')) for k in post_dict if id_p.search(k)]
@login_required
def index_view(request):
	template_name='forms/index.html'
	if request.user.profile.user_level <7 :
		return HttpResponse("Permission forbiden!")

	infosset=Infos.objects.exclude(status__creator__isnull=True)
	infos_dict={i.pk:InfosForm(instance=i) for i in infosset}
	infos_dict=OrderedDict(sorted(infos_dict.items(),reverse=True))
	selected_ids=get_selected_ids(request.POST)
	selected_infos=[infos_dict[i.pk] for i in infosset if i.pk in selected_ids ]

	if request.method == 'POST' :
		if 'download' in request.POST :
			if selected_ids:
				return submission_export(selected_infos,filename='selected_{}.csv'.format(len(selected_infos)))
			else :
				return submission_export(list(infos_dict.values()))
		elif 'delete' in request.POST :
			for i in selected_ids :
				instance=Infos.objects.get(pk=i)
				instance.delete()
			return redirect('forms:index')

	return render(request,template_name,{'infosset':infos_dict,})


class UserAppForm(forms.ModelForm):
	"""docstring for UserAppForm"""
	class Meta:
		model  = Infos
		fields = ('上报时间','支部名称','党员类别','类别编号',
				  '姓名','性别','身份证号','民族','籍贯',
				  '职级','职务','职称','文化程度','学位','工作时间',
				  '支部讨论入党时间','支部讨论转正时间','获奖情况','入党志愿书编号',
					)

class UserAppSubForm(forms.ModelForm):
	class Meta:
		model=Infos
		fields=(				
			'支部书记','介绍人姓名','申请书时间','推优时间','确认入党积极分子的时间',
			'党校结业时间','函调时间','公示时间','发展对象培训班','导师意见时间','导师',
			)

@login_required
def create_view(request):
	template_name="forms/create.html"
	if request.method == 'POST' :
		new_user_form=UserAppForm(request.POST)
		if new_user_form.is_valid() or True :
			new_infos=new_user_form.save(commit=False)
			#new_infos.info_id=len(Infos.objects.all())+1
			new_infos.save()
			new_infos.status.creator=request.user
			new_infos.status.save()

			his=Historys.objects.create(info=new_infos,edit_user=request.user,edit_time=timezone.now(),edit_content='create')
			his.save()

			new_user_form.save_m2m()
			return redirect(reverse('forms:edit',args=(new_infos.pk,)))
	else:
		new_user_form=UserAppForm()

		if request.user.profile.user_level < 3 :
			exist_submission=Status.objects.filter(creator=request.user)
			if exist_submission:
				template_name = 'forms/muti_submission_error.html'

	return render(request,template_name,{'user_form':new_user_form,})

@login_required
def edit_view(request,pk):
	if 'edit' in request.POST :
		template_name='forms/edit.html'
	else :
		template_name='forms/view.html'

	info=get_object_or_404(Infos,pk=pk)
	permisson = request.user.profile.user_level
	if permisson < 3 :
		if request.user != info.status.creator :
			raise Http404("User's infomation is protected!")
	if request.method == 'POST' and 'info_submit' in request.POST :
		user_form=UserAppForm(request.POST,instance=info)
		user_sub_form=UserAppSubForm(request.POST,instance=info)

		if user_form.is_valid() and user_sub_form.is_valid():
			user_form.save()
			user_sub_form.save()

			his=Historys.objects.create(info=info,edit_user=request.user,edit_time=timezone.now(),edit_content='edit')
			his.save()
		
			return redirect(reverse('forms:edit',args=(info.pk,)))
	else:
		user_form=UserAppForm(instance=info)
		user_sub_form=UserAppSubForm(instance=info)

	#for h in Historys.objects.all():
	#	h.full_clean()
	historyset=Historys.objects.filter(info=info).order_by('-edit_time')
	return render(request,template_name,
				{
					'user_form'    :user_form,
					'user_sub_form':user_sub_form,
					'permisson'    :permisson,
					'historyset'   :historyset,
					})
