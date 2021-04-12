from datetime import datetime

from django.contrib import messages
from django.db.models import Sum
from django.template.defaulttags import register

from users.models import CustomUser, PointsType, Point


def populate_flash_message(request, created, edited, record_date):
    created_text = ''
    edited_text = ''
    for c in created:
        created_text = created_text + '<li>{}</li>'.format(c)
    for e in edited:
        edited_text = edited_text + '<li>{}</li>'.format(e)
    if created_text is not '':
        messages.success(request,
                         record_date + ' - رمضان / لقد تم احتساب النقاط التالية:' + '<ul>{}</ul>'.format(created_text))
    if edited_text is not '':
        messages.info(request,
                      record_date + ' - رمضان / لقد تم تعديل النقاط التالية:' + '<ul>{}</ul>'.format(edited_text))


def save_to_db(request):
    user = CustomUser.objects.filter(username=request.user.username).first()
    items = request.POST.dict()
    record_date = items['record-date']
    created = []
    edited = []
    for key, value in items.items():
        if value == 'on':
            pt_points, pt_object, pt_details = get_points_and_details(key, items)
            point, is_created = Point.objects.update_or_create(user=user, type=pt_object, record_date=record_date,
                                                               defaults={'value': pt_points, 'details': pt_details, })
            if is_created:
                created.append(point.details)
            else:
                edited.append(point.details)
    populate_flash_message(request, created, edited, record_date)
    user.total_points = int(Point.objects.filter(user=user).aggregate(Sum("value"))['value__sum'])
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
    if pt_info.split('-')[0] == 'number':
        pt_points *= pt_object.score
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


daily_message = {
    datetime(2021, 4,
             12).date(): 'قوة الإمداد على قدر قوة الاستعداد والاستمداد، فاستعن بالله واعزم وخطط للفوز بهذا الشهر الكريم',
    datetime(2021, 4,
             13).date(): 'قوة الإمداد على قدر قوة الاستعداد والاستمداد، فاستعن بالله واعزم وخطط للفوز بهذا الشهر الكريم',
    datetime(2021, 4,
             14).date(): 'قوة الإمداد على قدر قوة الاستعداد والاستمداد، فاستعن بالله واعزم وخطط للفوز بهذا الشهر الكريم',
    datetime(2021, 4,
             15).date(): 'احتسب كل طاعة تقوم بها .. فلن تؤجر إلا على ما احتسبت، لذا عليك أن تعلم ثواب العبادات؛ لكي تحتسبها',
    datetime(2021, 4,
             16).date(): ' المحافظة على صلاة التراويح إلى أن ينصرف الإمام ليُكتب لك قيام رمضان بحول الله وقوته',
    datetime(2021, 4,
             17).date(): ' المحافظة على صلاة التراويح إلى أن ينصرف الإمام ليُكتب لك قيام رمضان بحول الله وقوته',
    datetime(2021, 4, 18).date(): '',
    datetime(2021, 4, 19).date(): '',
    datetime(2021, 4, 20).date(): '',
    datetime(2021, 4, 21).date(): '',
    datetime(2021, 4, 22).date(): '',
    datetime(2021, 4, 23).date(): '',
}


def get_ramadan_daily_message():
    return daily_message[datetime.today().date()]
