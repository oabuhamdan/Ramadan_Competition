from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from users.models import Point, Competition, CustomUser


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
def admin_home(request):
    return render(request, "admins/index.html")


@staff_member_required
def get_competition_people(request):
    selected_competition = request.GET.get('selected_comp')
    comp_people = CustomUser.objects.filter(competition_id=selected_competition)
    data = []
    for person in comp_people:
        data.append(
            {
                'username': person.username,
                'name': person.first_name
            }
        )
    return JsonResponse(data, safe=False)

@staff_member_required
def get_user_points(request):
    selected_user_name = request.GET.get('selected_user')
    selected_day = request.GET.get('selected_day')
    user_points = Point.objects.filter(user__username=selected_user_name, record_date=selected_day)
    data = []
    for point in user_points:
        data.append(
            {
                'id': point.id,
                'label': point.type.label,
                'details': point.details,
                'value': point.value,
            }
        )
    return JsonResponse(data, safe=False)
