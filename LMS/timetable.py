from functools import cmp_to_key

from LMS.models import DAY_OF_WEEK


def sort_day(day_class):
    cmp_attrs = ['start_time', 'end_time', 'start_week', 'end_week', 'unit.code']

    def get_attr(obj, attr):
        attrs = attr.split('.')
        for at in attrs:
            obj = getattr(obj, at)

        return obj

    def cmp(l, r):
        for attr in cmp_attrs:
            a_l = get_attr(l, attr)
            a_r = get_attr(r, attr)

            if a_l > a_r:
                return 1
            elif a_l < a_r:
                return -1

        return 0

    day_class.sort(key=cmp_to_key(cmp))


def generate_timetable(units):
    timetable = {}
    for n, _ in DAY_OF_WEEK:
        timetable[n] = []

    for u in units:
        for c in u.class_set.all():
            timetable[c.day].append(c)

    for _, c in timetable.items():
        sort_day(c)

    t = []

    for n, v in DAY_OF_WEEK:
        t.append((v, timetable[n]))

    return t
