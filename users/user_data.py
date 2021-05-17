import json

from django.core.serializers.json import DjangoJSONEncoder

from admins.models import UserArchive
from users.models import Point


class UserArchiveData:
    @staticmethod
    def get_user_points_grouped_by_date_as_json(username):
        user = UserArchive.objects.filter(username=username).first()
        data_json = user.json_data
        return data_json

    @staticmethod
    def get_user_points_by_date(username, date):
        user_points = UserArchiveData.get_user_points_grouped_by_date_as_json(username)
        user_points = json.loads(user_points)
        return user_points[date]


class UserData:
    @staticmethod
    def get_user_points_by_date(username, date):
        user_points = Point.objects.filter(user__username=username, record_date=date)
        points = []
        for point in user_points:
            points.append(
                {
                    'id': point.id,
                    'label': point.type.label,
                    'details': point.details,
                    'value': point.value,
                }
            )
        return points

    @staticmethod
    def get_user_points_grouped_by_date_as_json(username):
        data = {}
        for day in range(30, 0, -1):
            user_points_by_date = UserData.get_user_points_by_date(username, day)
            if len(user_points_by_date) > 0:
                data[day] = {'points': user_points_by_date,
                             'total_day': sum([point['value'] for point in user_points_by_date])}

        data = json.dumps(data, cls=DjangoJSONEncoder)
        return data
