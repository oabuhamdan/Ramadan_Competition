from django.db import models

# Create your models here.
from users.models import Competition, CustomUser


class CompetitionArchive(models.Model):
    comp_id = models.CharField(max_length=30, primary_key=True, default='')
    name = models.CharField(max_length=30, default='')
    excel_file_link = models.CharField(default='', max_length=256)
    excel_file_date = models.DateField(default=None, blank=True, null=True)


class UserArchive(models.Model):
    username = models.CharField(max_length=150, primary_key=True, default='')
    name = models.CharField(max_length=150, default='')
    competition_id = models.CharField(max_length=30, default='')
    archive_date = models.DateField(default=None, blank=True, null=True)
    json_data = models.JSONField(default=dict)
    total_points = models.FloatField(default=0.0)
