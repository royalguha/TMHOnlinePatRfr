from dataclasses import fields
from import_export import resources
from .models import referral_details

class PersonResource(resources.ModelResource):
    class Meta:
        model = referral_details
        fields = ['id','patient_name','patient_ph','patient_add','posted_on','doc_name','doc_ph','ip_no','admission_date','is_cancel','cancel_remarks']


class filtered_export(resources.ModelResource):

    class Meta:
        model = referral_details
