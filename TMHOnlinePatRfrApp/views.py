from dataclasses import fields
from pyexpat import model
from re import template
from zlib import DEF_BUF_SIZE
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.http import HttpResponse
from .resources import PersonResource,filtered_export
from datetime import date, datetime
import csv
from django.utils import timezone
import pytz
from TMHOnlinePatRfrApp.models import referral_details
from .forms import referral_form,refer_confirm_form,cancel_remark_form
from django.utils import timezone




# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method=="POST":
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                messages.error(request,"Invalid Credentials!")
        else:
            messages.error(request,"Invalid Credentials!")

    form = AuthenticationForm()
    return render(request,"login.html",{"loginform":form})

@login_required
def home(request):
    if request.method=="POST":
        form = referral_form(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.empid = request.user.profile.empid
            form.instance.posted_by = request.user.first_name + request.user.last_name
            form.save()
            return redirect("home")
        
    else:
        ref_det=referral_details.objects.filter(date = date.today()).order_by('-posted_on')
        #ref_det=referral_details.objects.raw("SELECT * FROM TMHOnlinePatRfrApp_referral_details")
        #ref_det=referral_details.objects.raw("SELECT * FROM TMHOnlinePatRfrApp_referral_details WHERE date BETWEEN")
    return render(request,"index.html",{"refrform":referral_form,"ref_det":ref_det,"refrconfirmform":refer_confirm_form,"cancel_remark_form":cancel_remark_form})
#class based update view for marketing head user
class DataUpdateView(UpdateView):
    
    template_name = "update.html"
    model = referral_details
    fields = "__all__"
    fields = ['ip_no','admission_date','admission_time','discharge_date_time','confirm']
    success_url = "/home"

    def post(self, request, *args, **kwargs):
        admission_date = request.POST['admission_date']
        admission_time = request.POST['admission_time']
        #date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        admn_date_time = datetime.strptime((admission_date+admission_time), '%Y-%m-%d%H:%M:%S')
        
        #admndate = datetime.date(datetime.strptime(admission_date, '%Y-%m-%d'))
        #admntime = datetime.time(datetime.strptime(admission_time)) 
        
        #if(admndate>admntime):
         #   print(admndate-admntime)
        posted_on = referral_details.objects.filter(id=kwargs['pk'])
        for x in posted_on:
            y = x.posted_on
        posted_date = datetime.date(y)
        posted_time = datetime.time(y)
        posted_datetime = timezone.localtime(y)
        admn_datetime = pytz.utc.localize(admn_date_time)
        local_dt = timezone.localtime(y)
        admn_datetime=admn_datetime.replace(tzinfo=None)
        local_dt=local_dt.replace(tzinfo=None)
        #if(posted_date > admndate):
         #   print("entry posted after admission has taken place")
        #elif(posted_date < admndate):
         #   print("Admission taken after posted date ")
        #elif(posted_date==admndate):
         #   print("admission and posted on same date")
          #  if(posted_time > admntime):
           #     print("posted time after admission time")
            #else:
             #   print("ok")

        if(local_dt>admn_datetime):
            referral_details.objects.filter(id=kwargs["pk"]).update(patient_current_status='1')
            print("posted after admission")
        elif(admn_datetime>local_dt):
            print("admitted afterb posted date")
        else:
            print("error")
       
        print(kwargs["pk"],local_dt,admn_datetime,admn_datetime-local_dt)



        return super().post(request, *args, **kwargs)
   # def form_valid(self, form, **kwargs):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
 #       admission_date = form.cleaned_data.get('admission_date')
 
 #       admission_time = form.cleaned_data.get('admission_time')
        

  #      datetime = referral_details.objects.filter(id=kwargs)

   #     for i in datetime:
    
    #        print(i.patient_ph)
       
       
     #   return super().form_valid(form)




class edit(UpdateView):
    
    template_name = "update.html"
    model = referral_details
    
    fields = ['patient_name','patient_ph','patient_add','doc_name','doc_ph','ip_no','admission_date','admission_time','discharge_date_time','patient_current_status','confirm']
    success_url = "/home"

class cancel(UpdateView):
    template_name = "cancel.html"
    model = referral_details
    fields = ['is_cancel','cancel_remarks']
    success_url = "/home"

def export(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Referral_Details.xls"'
    return response


def export_filtered(request):
    if request.method == "POST":
        from_date=request.POST['from']
        to_date=request.POST['to']


        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(['id','patient_name','patient_ph','patient_add','posted_on','doc_name','doc_ph','ip_no','admission_date','empid','posted_by','cancel_remarks'])

        dets = referral_details.objects.filter(date__range=[from_date,to_date]).values_list('id','patient_name','patient_ph','patient_add','posted_on','doc_name','doc_ph','ip_no','admission_date','empid','posted_by','cancel_remarks')
        for det in dets:
            writer.writerow(det)

        return response
    else:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(['id','patient_name','patient_ph','patient_add','posted_on','doc_name','doc_ph','ip_no','admission_date','empid','posted_by','cancel_remarks'])

        dets = referral_details.objects.all().values_list('id','patient_name','patient_ph','patient_add','posted_on','doc_name','doc_ph','ip_no','admission_date','empid','posted_by','cancel_remarks')
        for det in dets:
            writer.writerow(det)

        return response




def filter(request):
    if request.method=="POST":
        from_date = request.POST['from']
        to_date = request.POST['to']
        var = referral_details.objects.filter(date__range=[from_date,to_date]).order_by('-posted_on')
    
    return render(request,"index.html",{"refrform":referral_form,"ref_det":var,"refrconfirmform":refer_confirm_form})


#def cancel(request,**kwargs):
 #   if request.method=="POST":
  #      pass
   # else:

    #    remarks = request.GET['remarks']
     #   referral_details.objects.filter(id=kwargs["pk"]).update(is_cancel=1,cancel_remarks=remarks)
      #  return redirect("/home")


        
