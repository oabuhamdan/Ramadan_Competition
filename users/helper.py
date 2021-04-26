from datetime import datetime

from django.contrib import messages
from django.db.models import Sum
from django.template.defaulttags import register

from users.models import CustomUser, Point


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
            pt_points, pt_id, pt_details = get_points_and_details(key, items)
            point, is_created = Point.objects.update_or_create(user=user, type_id=pt_id, record_date=record_date,
                                                               defaults={'value': pt_points, 'details': pt_details, })
            if is_created:
                created.append(point.type.label)
            else:
                edited.append(point.type.label)
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


def get_pt_details(pt_info, items):
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
    pt_details = get_pt_details(pt_info, items)
    return pt_points, pt_id, pt_details


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
    datetime(2021, 4, 18).date(): 'الحرص على أعمال البر .. ومن أعظمها برَّ الوالدين، فلابد أن تحرص على برهما في رمضان كي تتنزل عليك الرحمة',
    datetime(2021, 4, 19).date(): 'البقاء بعد صلاة الفجر الى الشروق عدد ........يوم لتحصل على عدد ........حجة وعمرة كما في الحديث الصحيح',
    datetime(2021, 4, 20).date(): 'الحرص على الدعاء عند الإفطار فهو مستجاب',
    datetime(2021, 4, 21).date(): 'الحرص على الدعاء عند الإفطار فهو مستجاب',
    datetime(2021, 4, 22).date(): 'المحافظة على عدد .......ركعة قيام الثلث الأخير من الليل؛ فهو وقت مبارك تُقضى فيه الحاجات وتُستجاب في الدعوات',
    datetime(2021, 4, 23).date(): 'الصدقة بمبلغ ............ كل يوم في رمضان',
    datetime(2021, 4, 24).date(): 'لا تجعل لسانك يفتر عن ذكر الله لحظه قدر المستطاع',
    datetime(2021, 4, 25).date(): 'استشعر أن هذا رمضان هو آخر رمضان في حياتك وتصوم صيام مودع، و تُصلي صلاة مودع، وتجتهد فيه اجتهاداً عظيما',
    datetime(2021, 4, 26).date(): 'الدعاء كل ليلة بأن تكون من المعتوقين من النار في هذه الليلة، وهكذا كل ليلة واستشعر في آخر ليلة أن الله يقول لك :قد اعتقتك من النار',
    datetime(2021, 4, 27).date(): 'الدعاء في السجود والقيام للمظلومين، والمأسورين، والمكروبين، و المهمومين من أمة محمد صلى الله عليه وسلم أجمعين',
    datetime(2021, 4, 28).date(): 'المحافظة على مجالس الذكر والحرص عليها',
    datetime(2021, 4, 29).date(): 'الحرص على الاستغفار في السحر',
    datetime(2021, 4, 30).date(): 'التقليل من ساعات البقاء في الأسواق',
    datetime(2021, 5, 1).date(): 'الاعتياد على التبكير إلى المسجد يدل على عظيم الشوق والأنس بالعبادة ومناجاة الخالق',
    datetime(2021, 5, 2).date(): 'تحرى ليلة القدر في العشر الأواخر من هذا الشهر الكريم',
    datetime(2021, 5, 3).date(): 'تحرى ليلة القدر في العشر الأواخر من هذا الشهر الكريم',
    datetime(2021, 5, 4).date(): 'اجعل الليلة الواحدة مقسمة بين الصلاة وقراءة القرآن والدعاء والابتهال إلى الله سبحانه وتعالى',
    datetime(2021, 5, 5).date(): 'استحضار النية على استغلال هذه الأيام بالعمل والعبادة، واستحضار عظمة هذه العشر، خاصة أن فيها ليلة القدر',
    datetime(2021, 5, 6).date(): 'استحضار النية على استغلال هذه الأيام بالعمل والعبادة، واستحضار عظمة هذه العشر، خاصة أن فيها ليلة القدر',
    datetime(2021, 5, 7).date(): 'الاجتهاد في العبادة في الليالي الوترية، وهناك الكثير من المسلمين ينشغلون بتحري ليلة القدر عن الاجتهاد في العبادة، فمن يقوم بالاجتهاد في كل ليلة من الليالي العشر يدرك ليلة القدر',
    datetime(2021, 5, 8).date(): 'الاجتهاد في العبادة في الليالي الوترية، وهناك الكثير من المسلمين ينشغلون بتحري ليلة القدر عن الاجتهاد في العبادة، فمن يقوم بالاجتهاد في كل ليلة من الليالي العشر يدرك ليلة القدر',
    datetime(2021, 5, 9).date(): 'من أهم الأعمال التي تقوم بها في هذه الليالي أن تحاسب نفسك على ذنوبك، وأن تشعر بتقصيرك، وأن تشجع نفسك على ترك كل الذنوب واغتنام هذه الفرصة حتى يتوب الله عليك',
    datetime(2021, 5, 10).date(): 'من أهم الأعمال التي تقوم بها في هذه الليالي أن تحاسب نفسك على ذنوبك، وأن تشعر بتقصيرك، وأن تشجع نفسك على ترك كل الذنوب واغتنام هذه الفرصة حتى يتوب الله عليك',
    datetime(2021, 5, 11).date(): 'كل عام وأنتم بخير ، عيد فطر مبارك',
    datetime(2021, 5, 12).date(): 'كل عام وأنتم بخير ، عيد فطر مبارك',
    datetime(2021, 5, 13).date(): 'كل عام وأنتم بخير ، عيد فطر مبارك',
    datetime(2021, 5, 14).date(): 'كل عام وأنتم بخير ، عيد فطر مبارك',
}


def get_ramadan_daily_message():
    return daily_message[datetime.today().date()]
