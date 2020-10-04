def pages_wording(page_num):
    if page_num == 1:
        return 'صفحة'
    elif page_num == 2:
        return 'صفحتين'
    else:
        return str(page_num) + ' ' + 'صفحات'


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
    details.append('من جزء')
    details.append(items['quran-juz'])
    return points, ' '.join(details)


def get_siam_info(items):
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
    if 'media-summary' in items:
        details.append('وتلخيص')
        points = points + summary_points
    details.append(str(num(duration)))
    details.append('دقائق من')
    details.append(items['media-name'])
    return points, ' '.join(details)


def get_points_and_details(items, key):
    for item in items:
        if item.startswith(key):
            if key == 'quran':
                return get_quran_info(items)
            elif key == 'check_box':
                return get_siam_info(items)
            elif key == 'book':
                return get_book_info(items)
            elif key == 'media':
                return get_media_info(items)


def num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except:
            return 0
