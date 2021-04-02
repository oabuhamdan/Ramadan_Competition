from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


# Create your models here.
class CustomUser(User):
    total_points = models.FloatField(default=0.0)

    def __str__(self):
        return 'name: {}'.format(self.first_name)

    @staticmethod
    def get_points(username):
        points = Point.objects.filter(user__username=username).order_by('record_date')
        result = {}
        total_daily = {}
        for point in points:
            date_string = point.record_date.strftime("%d-%m-%Y")
            if date_string in result:
                result[date_string].append(point)
                total_daily[date_string] = total_daily[date_string] + point.value
            else:
                result[date_string] = [point]
                total_daily[date_string] = point.value
        return result, total_daily


class AllowedPointTypes(models.TextChoices):
    Number = 'number', 'Number'
    CheckBox = 'check_box', 'Check Box'
    BookForm = 'book', 'Book Form'
    QuranForm = 'quran', 'Quran Form'
    MediaForm = 'media', 'Media Form'
    Form = 'other', 'Other'


class Sections(models.TextChoices):
    Default = 'default', 'Default'
    Prayers = 'prayers', 'Prayers'
    LifeStyle = 'life_style', 'Life Style'
    Educational = 'educational', 'Educational'
    Personal = 'personal', 'Personal'


class PointsType(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.CharField(max_length=32, choices=Sections.choices, default=Sections.Default)
    label = models.CharField(max_length=128, default='', blank=False, null=False)
    description = models.CharField(max_length=256, default='')
    score = models.IntegerField(default=0)
    form_type = models.CharField(max_length=32, choices=AllowedPointTypes.choices, default=AllowedPointTypes.Number)
    form_html = models.TextField(default='Default value is populated in the HTML template')

    def __str__(self):
        return 'label: {}'.format(self.label)


class Point(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='point', null=True)
    type = models.ForeignKey(PointsType, on_delete=models.CASCADE, related_name='type', null=True)
    value = models.FloatField()
    details = models.CharField(max_length=256, default='')
    record_date = models.DateField(default=now)

    def __str__(self):
        return 'user: {}, point type: {}, value: {}, date: {}'.format(self.user, self.type.form_type, self.value,
                                                                      self.record_date)
