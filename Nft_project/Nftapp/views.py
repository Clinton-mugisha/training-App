# Nftapp/views.py
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Job, Resume
from .forms import JobForm, ResumeForm

from .ml_utils import load_data, create_overall_infos_column, apply_text_preprocessing, calculate_cosine_similarity_matrix, rank_candidates


def ranked_applicants_view(request, job_id):
    # Get the job based on job_id
    job = get_object_or_404(Job, pk=job_id)

    # Load data, create overall_infos column, and apply text preprocessing
    df = load_data()
    df = create_overall_infos_column(df)
    cleaned_infos = apply_text_preprocessing(df)

    # Calculate cosine similarity matrix
    similarity_matrix = calculate_cosine_similarity_matrix(cleaned_infos)

    # Rank candidates
    top_candidates = rank_candidates(similarity_matrix)

    # Get additional information for the top candidates (name, email, and score)
    candidates_info = []
    for candidates in top_candidates:
        candidates_info.append([(df.loc[candidate[0], 'full_name'], df.loc[candidate[0], 'email'], candidate[1]) for candidate in candidates])

    context = {'job': job, 'top_candidates': candidates_info}
    return render(request, 'ranked_applicants.html', context)

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

# class ApplicantCreateView(CreateView):
#     model = Applicant
#     form_class = ApplicantForm
#     template_name = 'applicant_create.html'
#     success_url = reverse_lazy('job_list')

def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the form data
            full_name = form.cleaned_data['full_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            education = form.cleaned_data['education']
            skills = form.cleaned_data['skills']
            work_experience = form.cleaned_data['work_experience']
            upload_cv = form.cleaned_data['upload_cv']



            # Save the form data, including the applied_job association
            applied_job = form.cleaned_data['applied_job']
            
            # Create and save the Resume instance
            resume = Resume(
                full_name=full_name,
                phone_number=phone_number,
                email=email,
                education=education,
                skills=skills,
                work_experience=work_experience,
                upload_cv=upload_cv,
                applied_job=applied_job
            )
            resume.save()

            # You can add a success message or redirect to a thank-you page
            return HttpResponse("Thank you for submitting your resume!")

    else:
        form = ResumeForm()

    return render(request, 'create_resume.html', {'form': form})