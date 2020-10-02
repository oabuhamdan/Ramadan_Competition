from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import TruncMonth, TruncDate
from django.utils.timezone import now
from itertools import groupby
from operator import attrgetter


# Create your models here.
class CustomUser(User):
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return 'name: {}'.format(self.first_name)

    def get_points(self):
        points = Point.objects.all().order_by('record_date')
        result = {}
        for point in points:
            date_string = point.record_date.strftime("%m-%Y")
            if date_string in result:
                result[date_string].append(point)
            else:
                result[date_string] = [point]

        return result


class PointsType(models.Model):
    name = models.CharField(max_length=64)
    default_value = models.IntegerField()

    def __str__(self):
        return 'name: {}'.format(self.name)


class Point(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='point', null=True)
    type = models.ForeignKey(PointsType, on_delete=models.CASCADE, related_name='type', null=True)
    value = models.IntegerField()
    record_date = models.DateField(default=now)

    def __str__(self):
        return 'user: {}, point type: {}, value: {}, date: {}'.format(self.user.first_name, self.type.name, self.value,
                                                                      self.record_date)
