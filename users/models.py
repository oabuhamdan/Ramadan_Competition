from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Competition(models.Model):
    id = models.CharField(max_length=30, primary_key=True, default='')
    name = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.name


class CustomUser(User):
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, related_name='competition_user', null=True)
    total_points = models.FloatField(default=0.0)

    def __str__(self):
        return 'المسابقة: {}, الاسم: {}'.format(self.competition.name, self.first_name)

    @staticmethod
    def get_points(username):
        points = Point.objects.filter(user__username=username).order_by('-record_date')
        result = {}
        total_daily = {}
        for point in points:
            date = point.record_date
            if date in result:
                result[date].append(point)
                total_daily[date] = total_daily[date] + point.value
            else:
                result[date] = [point]
                total_daily[date] = point.value
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
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, related_name='competition_point', null=True)
    id = models.AutoField(primary_key=True)
    section = models.CharField(max_length=32, choices=Sections.choices, default=Sections.Default)
    label = models.CharField(max_length=128, default='', blank=False, null=False)
    description = models.CharField(max_length=256, default='')
    score = models.IntegerField(default=0)
    upper_bound = models.IntegerField(default=20)
    form_type = models.CharField(max_length=32, choices=AllowedPointTypes.choices, default=AllowedPointTypes.Number)
    form_html = models.TextField(default='Default value is populated in the HTML template')

    def __str__(self):
        return 'المسابقة: {}, العنوان: {}'.format('' if self.competition is None else self.competition.name, self.label)


class Point(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='point', null=True)
    type = models.ForeignKey(PointsType, on_delete=models.SET_NULL, related_name='type', null=True)
    value = models.FloatField()
    details = models.CharField(max_length=256, default='')
    record_date = models.IntegerField(default=1)

    def __str__(self):
        return 'المستخدم: {}, النقطة: {}, القيمة: {}, التاريخ: {}'.format(
            '' if self.user is None else self.user.first_name, self.type.label,
            self.value,
            self.record_date)


class Group(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='competition_group', null=True)
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, related_name='competition_group', null=True)
    fellows = models.ManyToManyField(CustomUser)
