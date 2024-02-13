# recruitment/forms.py
from django import forms
<<<<<<< HEAD
from .models import Job, Applicant
=======
from .models import Job
>>>>>>> Development


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
<<<<<<< HEAD
    education = forms.ChoiceField(
        choices=[('Diploma', 'Diploma'), ('Degree', 'Degree'), ('Masters', 'Masters'), ('Doctorate', 'Doctorate')],
        label='Education'
    )
    skills = forms.CharField(label='Skills', max_length=255)
    work_experience = forms.ChoiceField(
        choices=[('0-1', '0-1'), ('2-3', '2-3'), ('4-5', '4-5'), ('6-7', '6-7'), ('8-9', '8-9'), ('10+', '10+')],
        label='Work Experience'
    )
    languages = forms.MultipleChoiceField(
        choices=[('English', 'English'), ('Kiswahili', 'Kiswahili'), ('French', 'French'), ('Other', 'Other')],
        widget=forms.CheckboxSelectMultiple,
        label='Languages'
    )
    other_language = forms.CharField(max_length=100, required=False, label='Specify Other Language')

    upload_cv = forms.FileField(label='Upload CV')

    def clean(self):
        cleaned_data = super().clean()
        languages = cleaned_data.get('languages', [])
        other_language = cleaned_data.get('other_language')

        if 'Other' in languages and not other_language:
            raise forms.ValidationError('Please specify the "Other" language.')

        return cleaned_data
=======
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

>>>>>>> Development
