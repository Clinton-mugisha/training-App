from django.urls import path
from .views import JobListView, JobDetailView, JobCreateView,  create_resume, JobsView,ranked_applicants_view
# RankedApplicantsView

urlpatterns = [
    path('', JobListView.as_view(), name='job_list'),
    path('jobs', JobsView.as_view(), name='jobs'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('jobs/create/', JobCreateView.as_view(), name='job_create'),
    # path('applicants/create/', ApplicantCreateView.as_view(), name='applicant_create'),
    path('job/<int:job_id>/ranked-applicants/', ranked_applicants_view, name='ranked_applicants'),
    path("create-resume/", create_resume, name="create_resume"),
    # path('job/<int:job_id>/ranked-applicants/', RankedApplicantsView.as_view(), name='ranked_applicants'),
]
