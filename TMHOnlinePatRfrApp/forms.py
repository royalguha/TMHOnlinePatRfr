from dataclasses import field, fields
from pyexpat import model
from django.forms import ModelForm
from django import forms
from .models import referral_details

class dateinput(forms.DateInput):
    input_type = "date"


class referral_form(ModelForm):
    CHOICES = (
        
        ('Cash','Cash'),
        ('Insurance','Insurance'),
        ('Corporate','Corporate'),
        
    )

    patient_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = referral_details
        fields = ['patient_name','patient_ph','patient_add','doc_name','doc_ph','speciality','patient_type','payer_details'] 
        widgets = {
            'admission_date':dateinput(),
            'doc_name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'patient_name': forms.TextInput(attrs={'placeholder': 'Enter Patient Name'}),
            'patient_ph': forms.TextInput(attrs={'placeholder': 'Enter Patient Phone'}),
            'patient_add': forms.TextInput(attrs={'placeholder': 'Enter Patient Address'}),
            'doc_ph': forms.TextInput(attrs={'placeholder': 'Enter Phone Number'}),
            'speciality': forms.TextInput(attrs={'placeholder': 'Enter Speciality Name'}),
            'payer_details': forms.TextInput(attrs={'placeholder': 'Enter Payer Name'}),
            
            
            
        }
        


class refer_confirm_form(ModelForm):
    class Meta:
        model = referral_details
        fields = ['admission_date','confirm']
        widgets = {
            'admission_date':dateinput(),
            
        }


class cancel_remark_form(ModelForm):
    class Meta:
        model = referral_details
        fields = ['is_cancel','cancel_remarks']
        