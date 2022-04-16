from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True)
    empid = models.IntegerField(unique=True,blank=True)
    mobile = models.CharField(max_length=13,blank=True)
    dept = models.CharField(max_length=50,blank=True)
    last_modified = models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return str(self.user.first_name+" "+self.user.last_name)

class role_master(models.Model):
    CHOICES_ROLE = (
        
        ('1','ACCOUNTS'),
        ('2','MARKETING HEAD'),
        ('3','MARKETING EXECUTIVE'),
        
    )
    empid = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=10,choices=CHOICES_ROLE,default=0)
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.empid.first_name+" "+self.empid.last_name)

class referral_details(models.Model):
    CHOICES = (
        ('','Click to Select'),
        ('Cash','Cash'),
        ('Insurance','Insurance'),
        ('Corporate','Corporate'),
        
    )

    CHOICES_STATUS = (
        ("1",'ON HOLD FOR APPROVAL'),
        ("2",'B'),
        ("3",'C'),
        ("4",'D'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=50,verbose_name="Patient Name")
    patient_ph = models.CharField(max_length=10,blank=True,verbose_name="Patient Phone")
    patient_add = models.CharField(max_length=60,blank=True,null=True,verbose_name='Patient Address')
    posted_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    doc_name = models.CharField(max_length=30,null=True,blank=False,verbose_name="Referred by")
    doc_ph = models.CharField(max_length=10,blank=False,verbose_name="Referred by Phone",default="")
    ip_no = models.CharField(null=True,blank=False,max_length=120,verbose_name="IP")
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    patient_type = models.CharField(max_length=50,choices=CHOICES,blank=False,default="")
    payer_details = models.CharField(max_length=120,blank=True,default="")
    speciality = models.CharField(max_length=100,blank=False,default="")   
    last_modified = models.DateTimeField(auto_now_add=True,blank=True)
    admission_date = models.DateField(blank=True,null=True,verbose_name="Admission Date")
    admission_time = models.TimeField(blank=False,null=True,verbose_name="Admission Time")
    discharge_date_time = models.DateTimeField(blank=True,null=True,verbose_name="Discharge Date/Time")
    confirm = models.BooleanField(blank=True,default=0,verbose_name="Click to Confirm Admission")
    is_cancel = models.BooleanField(default=0,blank=False)
    cancel_remarks = models.TextField(max_length=300,default=" ")
    empid = models.CharField(max_length=10,default=0)
    posted_by = models.CharField(max_length=50,default=0)
    patient_current_status = models.CharField(max_length=100,choices=CHOICES_STATUS,blank=True,default="")
    remarks = models.CharField(max_length=100,null=True,blank=True)

    def  __str__(self):
        return str(self.patient_name)

    @property
    def today(self):
        return date.today()