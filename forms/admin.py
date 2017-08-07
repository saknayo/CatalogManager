from django.contrib import admin

from .models import Infos,Status,Historys
# Register your models here.
class InfosAdmin(admin.ModelAdmin):
	fieldsets=[
		#('党员信息'            ,{'fields':['report_time','zb_name','dy_type','type_id']}),
		('党员信息'            ,{'fields':['上报时间','支部名称','党员类别','类别编号']}),
		#('personal infomation',{'fields':['name','gender','birth_date','id_num','nationality','birth_area']}),
		('personal infomation',{'fields':['姓名','性别','birth_date','身份证号','民族','籍贯']}),
	]
admin.site.register(Infos,InfosAdmin)