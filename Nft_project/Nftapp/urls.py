from django.urls import path
from .views import JobListView, JobDetailView, JobCreateView, ApplicantCreateView

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/create/', JobCreateView.as_view(), name='job_create'),
    path('applicants/create/', ApplicantCreateView.as_view(), name='applicant_create'),
]
