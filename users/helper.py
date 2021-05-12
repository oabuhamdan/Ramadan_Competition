from django.contrib import messages
from django.db.models import Sum
from django.template.defaulttags import register

from users.models import CustomUser, Point, PointsType


def populate_flash_message(request, created, edited, error, record_date):
    created_text = ''
    edited_text = ''
    error_text = ''
    for c in created:
        created_text = created_text + '<li>{}</li>'.format(c)
    for e in edited:
        edited_text = edited_text + '<li>{}</li>'.format(e)
    for er in error:
        error_text = error_text + '<li>{}</li>'.format(er)
    if created_text is not '':
        messages.success(request,
                         record_date + ' - رمضان / لقد تم احتساب النقاط التالية:' + '<ul>{}</ul>'.format(created_text))
    if edited_text is not '':
        messages.info(request,
                      record_date + ' - رمضان / لقد تم تعديل النقاط التالية:' + '<ul>{}</ul>'.format(edited_text))
    if error_text is not '':
        messages.warning(request,
                         record_date + ' - رمضان / لم يتم احتساب النقاط التالية:' + '<ul>{}</ul>'.format(error_text))


def save_to_db(request):
    user = CustomUser.objects.filter(username=request.user.username).first()
    items = request.POST.dict()
    record_date = items['record-date']
    created = []
    edited = []
    error = []
    for key, value in items.items():
        if value == 'on':
            pt_points, pt_id, pt_details = get_points_and_details(key, items)
            pt_type = PointsType.objects.filter(id=pt_id).first()
            if pt_type.is_active and pt_points <= pt_type.upper_bound * pt_type.score:
                point, is_created = Point.objects.update_or_create(user=user, type_id=pt_id, record_date=record_date,
                                                                   defaults={'value': pt_points,
                                                                             'details': pt_details, })
                if is_created:
                    created.append(point.type.label)
                else:
                    edited.append(point.type.label)
            else:
                error.append(pt_type.label)
    populate_flash_message(request, created, edited, error, record_date)
    user.total_points = int(Point.objects.filter(user=user).aggregate(Sum("value"))['value__sum'])
    user.save()


def handle_checkbox_points(items):
    points = num(items['check_box-score'])
    details = ''
    return points, details


def get_point_details(pt_info, items):
    if pt_info.split('-')[0] == 'number':
        count = num(items[pt_info + '-count'])
        pt_points = num(items[pt_info + '-score'])
        return 'عدد {} * {} نقطة لكل منها'.format(count, pt_points)
    else:
        return ''


def get_points_and_details(pt_info, items):
    pt_id = pt_info.split('-')[1]
    pt_points = num(items[pt_info + '-score'])
    if pt_info.split('-')[0] == 'number':
        count = num(items[pt_info + '-count'])
        pt_points *= count
    pt_details = get_point_details(pt_info, items)
    return pt_points, pt_id, pt_details


def num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except:
            return 0


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def get_ramadan_daily_message():
    return 'كل عام وأنتم بخير ، عيد فطر مبارك'
