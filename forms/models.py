from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class Infos(models.Model):
	#info_id=models.IntegerField(default=0,name='info_id')#
	#pub_date = models.DateTimeField('date published')
	report_time =models.IntegerField(default=0,name='上报时间')#上报时间
	zb_name     =models.CharField(max_length=200,name='支部名称')#支部名称
	dy_type     =models.CharField(max_length=200,name='党员类别')#党员类别
	type_id     =models.IntegerField(default=0,name='类别编号')#类别编号
	name        =models.CharField(max_length=200,name='姓名')#姓名
	gender      =models.CharField(max_length=200,name='性别')#性别
	birth_date  =models.DateField(default="1888-11-23",name='出生年月')#出生年月
	id_num      =models.CharField(max_length=200,null=True,name='身份证号')#身份证号
	nationality =models.CharField(max_length=200,null=True,name='民族')#名族
	birth_area  =models.CharField(max_length=200,null=True,name='籍贯')#籍贯
	job_class   =models.CharField(max_length=200,null=True,name='职级')#职级
	job         =models.CharField(max_length=200,null=True,name='职务')#职务
	job_name    =models.CharField(max_length=200,null=True,name='职称')#职称
	whcd        =models.CharField(max_length=200,null=True,name='文化程度')#文化程度
	xw          =models.CharField(max_length=200,null=True,name='学位')#学位
	job_time    =models.CharField(max_length=200,null=True,name='工作时间')#工作时间
	dzbtlrd_time=models.CharField(max_length=200,null=True,name='支部讨论入党时间')#支部讨论入党时间
	dzbtlzz_time=models.CharField(max_length=200,null=True,name='支部讨论转正时间')#支部讨论转正时间
	rewards     =models.CharField(max_length=200,null=True,name='获奖情况')#获奖情况
	rdzys_num   =models.CharField(max_length=200,null=True,name='入党志愿书编号')#入党志愿书编号

	zbsj         =models.CharField(max_length=200,null=True,name='支部书记')#
	jsrxm        =models.CharField(max_length=200,null=True,name='介绍人姓名')#
	sqs_time     =models.CharField(max_length=200,null=True,name='申请书时间')#
	ty_time      =models.CharField(max_length=200,null=True,name='推优时间')#
	qrrdjjfz_time=models.CharField(max_length=200,null=True,name='确认入党积极分子的时间')#
	dxjy_time    =models.CharField(max_length=200,null=True,name='党校结业时间')#
	hd_time      =models.CharField(max_length=200,null=True,name='函调时间')#
	gs_time      =models.CharField(max_length=200,null=True,name='公示时间')#
	fzdxpxb      =models.CharField(max_length=200,null=True,name='发展对象培训班')#
	dsyj_time    =models.CharField(max_length=200,null=True,name='导师意见时间')#
	daoshi       =models.CharField(max_length=200,null=True,name='导师')#

#class Reward(models.Model):
#	info=models.ForeignKey(Infos,on_delete=models.CASCADE)#获奖情况
#	name=models.CharField(max_length=100)

class Status(models.Model):
	""" save time,submit time,submit status
	    audit time,audit status """
	info          = models.OneToOneField(Infos, on_delete=models.CASCADE)
	creator       = models.ForeignKey(User , null=True, on_delete=models.CASCADE)
	submit_status = models.CharField(null=True , max_length=200)
	audit_status  = models.CharField(null=True , max_length=200)

	create_time   = models.DateTimeField(null=True,name='create_time')
	save_time     = models.DateTimeField(null=True,name='save_time',auto_now=True)
	submit_time   = models.DateTimeField(null=True,name='submit_time')
	audit_time    = models.DateTimeField(null=True,name='audit_time')

@receiver(post_save, sender=Infos)
def create_info_status(sender, instance, created, **kwargs):
    if created:
        Status.objects.create(info=instance,create_time=timezone.now())## should assosite with the user

@receiver(post_save, sender=Infos)
def save_info_status(sender, instance, **kwargs):
    try :
        instance.status.save()
    except ObjectDoesNotExist:
    	create_info_status(sender,instance,True)


class Historys(models.Model):
	'''record of editting,submitting and auditting on info'''
	info        =models.ForeignKey(Infos, on_delete=models.CASCADE)
	edit_user   =models.ForeignKey(User , on_delete=models.CASCADE)
	edit_time   =models.DateTimeField(null=True,name='edit_time')
	edit_content=models.CharField(null=True,max_length=500)



