from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Job, Applicant, Resume
from .forms import JobForm, ApplicantForm, ResumeForm
from .ml_module import train_model, rank_resumes # Import the ml_module functions

class RankResumesView(View):
    template_name = 'rank_resumes.html'

    def get(self, request, *args, **kwargs):
        # Fetch the job description from the database or any other source
        job_description = Job.objects.get(pk=1).description  # Assuming you have a job with ID 1

        # Train the model
        rf_classifier, tfidf_vectorizer, label_encoder = train_model()

        # Get all applicants for the specified job
        applicants = Applicant.objects.filter(applied_job_id=1)  # Assuming the job ID is 1

        # Rank resumes
        ranking_scores = rank_resumes(job_description, rf_classifier, tfidf_vectorizer, label_encoder, applicants)

        # Prepare the data to pass to the template
        context = {
            'applicants': applicants,
            'ranking_scores': ranking_scores,
        }

        # Render the template with the data
        return render(request, self.template_name, context)

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
            languages = form.cleaned_data['languages']
            upload_cv = form.cleaned_data['upload_cv']

            # Check if 'Other' is selected in languages
            other_language = form.cleaned_data.get('other_language', None)
            if 'Other' in languages and other_language:
                # Do something with the other_language, for example, print it
                print(f"Other Language Specified: {other_language}")

            # Create and save the Resume instance
            resume = Resume(
                full_name=full_name,
                phone_number=phone_number,
                email=email,
                education=education,
                skills=skills,
                work_experience=work_experience,
                languages=languages,
                other_language=other_language,
                upload_cv=upload_cv
            )
            resume.save()

            # You can add a success message or redirect to a thank-you page
            return HttpResponse("Thank you for submitting your resume!")

    else:
        form = ResumeForm()

    return render(request, 'create_resume.html', {'form': form})



# def create_resume(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             # You can add a success message or redirect to a thank-you page
#             return HttpResponse("Thank you for submitting your resume!")
#     else:
#         form = ResumeForm()

#     return render(request, 'create_resume.html', {'form': form})


# def create_resume(request):
#     if request.method == 'POST':
#         form = ResumeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # You can add a success message or redirect to a thank-you page
#             return redirect('thank_you_page')
#     else:
#         form = ResumeForm()

#     return render(request, 'create_resume.html', {'form': form})