# Generated by Django 5.0 on 2024-01-22 09:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Nftapp", "0005_resume"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resume",
            name="achievements_awards",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="certifications_training",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="hobbies_interests",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="professional_memberships",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="professional_summary",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="projects",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="publications_presentations",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="references",
        ),
        migrations.RemoveField(
            model_name="resume",
            name="volunteer_experience",
        ),
    ]