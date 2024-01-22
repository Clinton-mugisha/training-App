# recruitment/forms.py
from django import forms
from .models import Job, Applicant, Resume


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description"]


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ["name", "email", "cv", "applied_job"]


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = "__all__"

    WORK_EXPERIENCE_CHOICES = [
        ("0-1", "0-1 years"),
        ("2-3", "2-3 years"),
        ("4-5", "4-5 years"),
        ("6-7", "6-7 years"),
        ("8-9", "8-9 years"),
        ("10+", "10 or more years"),
    ]

    EDUCATION_CHOICES = [
        ("diplomacy", "Diplomacy"),
        ("bachelors", "Bachelor's Degree"),
        ("masters", "Master's Degree"),
        ("doctorate", "Doctorate"),
        ("other", "Other"),
    ]

    LANGUAGES_CHOICES = [
        ("english", "English"),
        ("kiswahili", "Kiswahili"),
        ("french", "French"),
        ("other", "Other"),
    ]

    work_experience = forms.ChoiceField(
        choices=WORK_EXPERIENCE_CHOICES,
        widget=forms.RadioSelect,
    )

    education = forms.ChoiceField(
        choices=EDUCATION_CHOICES,
        widget=forms.RadioSelect,
    )

    education_other = forms.CharField(
        label="Specify Other Education",
        required=False,
    )

    skills = forms.CharField(
        label="Skills",
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    languages = forms.MultipleChoiceField(
        choices=LANGUAGES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    languages_other = forms.CharField(
        label="Specify Other Languages",
        required=False,
    )
