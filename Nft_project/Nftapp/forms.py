# recruitment/forms.py
from django import forms
from .models import Job, Applicant

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description']

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'cv', 'applied_job']