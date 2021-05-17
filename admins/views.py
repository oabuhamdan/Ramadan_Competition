import datetime
from io import BytesIO

import pandas as pd
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from admins.models import *
from users.models import Point
from users.user_data import UserData


@staff_member_required
def admin_home(request):
    return render(request, "admins/index.html")


@staff_member_required
def delete_selected_points(request):
    ids = request.POST.dict()['selected_points'].split(',')[1:]
    for pt_id in ids:
        Point.objects.filter(id=pt_id).delete()
    return HttpResponse(status=200)


@staff_member_required
def delete_points(request):
    competitions = Competition.objects.all()
    return render(request, 'admins/delete_points.html', {'competitions': competitions})


@staff_member_required
def get_competition_people(request):
    selected_competition = request.GET.get('selected_comp')
    comp_people = CustomUser.objects.filter(competition_id=selected_competition)
    archive_people = UserArchive.objects.filter(competition_id=selected_competition)
    data = []
    for person in comp_people:
        data.append(
            {
                'username': person.username,
                'name': person.first_name,
                'archive_date': archive_people.filter(username=person.username).first().archive_date,
            }
        )
    return JsonResponse(data, safe=False)


@staff_member_required
def get_user_points(request):
    selected_user_name = request.GET.get('selected_user')
    selected_day = request.GET.get('selected_day')
    data = UserData.get_user_points_by_date(selected_day, selected_user_name)
    return JsonResponse(data, safe=False)


def render_template_for_competition(request, html_template):
    competitions = CompetitionArchive.objects.all()
    return render(request, html_template, {'competitions': competitions})


def archive_points(usr_id):
    user = CustomUser.objects.filter(username=usr_id).first()
    data = UserData.get_user_points_grouped_by_date_as_json(user.username)
    UserArchive.objects.update_or_create(username=usr_id, name=user.first_name, competition_id=user.competition.id,
                                         defaults={'archive_date': datetime.datetime.now,
                                                   'json_data': data,
                                                   'total_points': user.total_points
                                                   })


def archive_points_action(request):
    ids = request.POST.dict()['selected_users'].split(',')[1:]
    for usr_id in ids:
        try:
            archive_points(usr_id)
        except Exception as e:
            print(e)
    return HttpResponse(status=200)


@staff_member_required
def archive_users_points(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if not is_ajax:
        return render_template_for_competition(request, 'admins/archive_points.html')
    else:
        return archive_points_action(request)


def generate_excel_file_action(comp_id):
    users = UserArchive.objects.filter(competition_id=comp_id)
    CompetitionArchive.objects.filter(comp_id=comp_id).update(excel_file_date=datetime.date.today())
    names = [user.name for user in users]
    total = [user.total_points for user in users]
    filled_dates = [len(json.loads(user.json_data).keys()) if len(user.json_data) > 0 else 0 for user in users]
    s1 = pd.Series(names, name='الاسم')
    s2 = pd.Series(total, name='المجموع')
    s3 = pd.Series(filled_dates, name='عدد الأيام المعبأة')
    df = pd.concat([s1, s2, s3], axis=1)
    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='openpyxl')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        # Set up the Http response.
        filename = comp_id + '.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


@staff_member_required
def generate_excel_file(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if not is_ajax:
        return render_template_for_competition(request, 'admins/generate_excel_file.html')
    else:
        return generate_excel_file_action(request.GET.get('comp_id'))
