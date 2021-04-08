from django.template.defaulttags import register
from users.models import CustomUser, PointsType, Point


def save_to_db(request):
    user = CustomUser.objects.filter(username=request.user.username).first()
    items = request.POST.dict()
    total = 0.0
    record_date = items['record-date']
    for key, value in items.items():
        if value == 'on':
            pt_points, pt_object, pt_details = get_points_and_details(key, items)
            total = total + pt_points
            Point.objects.create(user=user, type=pt_object, value=pt_points, details=pt_details,
                                 record_date=record_date)

    user.total_points = user.total_points + total
    user.save()


def pages_wording(page_num):
    if page_num == 1:
        return 'صفحة'
    elif page_num == 2:
        return 'صفحتين'
    else:
        return str(page_num) + ' ' + 'صفحات'


def media_wording(duration):
    if 3 <= duration <= 10:
        return 'دقائق من'
    else:
        return 'دقيقة من'


def get_quran_info(items):
    page_num = num(items['quran-read-pages'])
    details = []
    if 'quran-memorize' in items:
        details.append('حفظ')
        factor = num(items['quran-score-memorize'])
    else:
        details.append('قراءة')
        factor = num(items['quran-score-read'])

    points = page_num * factor
    if 'quran-tafseer' in items:
        details.append('وتفسير')
        points = points + page_num * num(items['quran-score-tafseer'])
    details.append(pages_wording(page_num))
    details.append('من الجزء')
    details.append(items['quran-juz'])
    return points, ' '.join(details)


def handle_checkbox_points(items):
    points = num(items['check_box-score'])
    details = ''
    return points, details


def get_book_info(items):
    read_points = num(items['book-score-read'])
    summary_points = num(items['book-score-summary'])
    start_page = num(items['book-start-page'])
    finish_page = num(items['book-finish-page'])
    page_num = finish_page - start_page + 1
    details = ['قراءة']
    points = read_points * page_num
    if 'book-summary' in items:
        details.append('وتلخيص')
        points = points + (summary_points * page_num)

    print('BOOK', points)
    details.append(pages_wording(page_num))
    details.append('من كتاب')
    details.append(items['book-name'])
    return points, ' '.join(details)


def get_media_info(items):
    summary_points = num(items['media-score-summary'])
    duration = num(items['media-duration'])
    points = duration * num(items['media-score-' + items['media-type']])
    details = ['مشاهدة']
    if 'media-summary' in items and duration > 240:
        details.append('وتلخيص')
        points = points + summary_points
    details.append(str(num(duration)))
    details.append(media_wording(duration))
    details.append(items['media-name'])
    return points, ' '.join(details)


def get_pt_details(pt_points, pt_object):
    return '{} نقاط من {}'.format(pt_points, pt_object.label)


def get_points_and_details(pt_info, items):
    pt_id = pt_info.split('-')[1]
    pt_object = PointsType.objects.filter(id=pt_id).first()
    pt_points = num(items[pt_info + '-score'])
    pt_details = get_pt_details(pt_points, pt_object)
    return pt_points, pt_object, pt_details


def num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except:
            return 0


arabic_section_names = {
    'default': 'العبادات والطاعات',
    'prayers': 'الجانب العبادي',
    'life_style': 'الجانب الحياتي',
    'educational': 'الجانب الثقافي',
    'personal': 'الجانب الشخصي'
}


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_arabic_section_name(key):
    return arabic_section_names.get(key)

