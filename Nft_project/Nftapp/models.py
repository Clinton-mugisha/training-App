# recruitment/models.py
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Applicant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    cv = models.FileField(upload_to='cvs/')
    applied_job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    ranking_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Resume(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    education = models.TextField()
    work_experience = models.TextField()
    skills = models.TextField()
    languages = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to='cvs/')

    def __str__(self):
        return self.full_name

