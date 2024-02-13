# recruitment/forms.py
from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description"]


# class ApplicantForm(forms.ModelForm):
#     class Meta:
#         model = Applicant
#         fields = ["name", "email", "cv", "applied_job"]


class ResumeForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    phone_number = forms.CharField(label='Phone number', max_length=15)
    email = forms.EmailField(label='Email')
    education = forms.CharField(
        label="Education",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "cols": 70,}),
    )
    skills = forms.CharField(
        label="Skills",
        widget=forms.Textarea(attrs={"rows": 3, "cols": 70,}),
    )
    work_experience = forms.ChoiceField(
        choices=[('0-1', '0-1'), ('2-3', '2-3'), ('4-5', '4-5'), ('6-7', '6-7'), ('8-9', '8-9'), ('10+', '10+')],
        label='Work Experience'
    )
    # New field for applied_job
    applied_job = forms.ModelChoiceField(queryset=Job.objects.all(), label='Select Job')

    upload_cv = forms.FileField(label='Upload CV')


