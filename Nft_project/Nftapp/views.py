from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render
from django.views import View
from .models import Job, Applicant
from .forms import JobForm, ApplicantForm
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from django.http import HttpResponse
from .ml_module import train_model, rank_resumes  # Import the ml_module functions

class RankResumesView(View):
    template_name = 'rank_resumes.html'

    def get(self, request, *args, **kwargs):
        # Fetch the job description from the database or any other source
        job_description = Job.objects.get(pk=1).description  # Assuming you have a job with ID 1

        # Load and train the model
        rf_classifier, tfidf_vectorizer, label_encoder = train_model()

        # Get all applicants
        applicants = Applicant.objects.all()

        # Rank resumes
        ranking_scores = rank_resumes(job_description, rf_classifier, tfidf_vectorizer, label_encoder, applicants)

        return HttpResponse("Ranking complete. Check the Admin panel to view the updated ranking scores.")






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
