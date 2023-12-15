
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Job, Applicant
from .forms import JobForm, ApplicantForm

class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'

class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'

    

class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job_create.html'
    success_url = reverse_lazy('job_list')

class ApplicantCreateView(CreateView):
    model = Applicant
    form_class = ApplicantForm
    template_name = 'applicant_create.html'
    success_url = reverse_lazy('job_list')

    
