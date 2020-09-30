from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128)
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=128)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return 'name: {}, username: {}'.format(self.name, self.username)


class PointsType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return 'name: {}'.format(self.name)


class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(PointsType, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return 'user: {}, point type: {}, value: {}'.format(self.user.username, self.type.name, self.value)
