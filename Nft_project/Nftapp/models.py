# recruitment/models.py
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Resume(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    education = models.CharField(max_length=255)
    skills = models.TextField()
    work_experience = models.TextField()
<<<<<<< HEAD
    languages = models.TextField()
    other_language = models.CharField(max_length=100, blank=True, null=True)  # Add this field
    upload_cv = models.FileField(upload_to='cv_uploads/')
=======
    upload_cv = models.FileField(upload_to='cv_uploads/')
    applied_job = models.ForeignKey(Job, on_delete=models.CASCADE)
>>>>>>> Development

    def __str__(self):
        return self.full_name
