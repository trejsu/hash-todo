import datetime

from django import template

register = template.Library()


@register.filter(name='moment')
def moment(date):
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)

    if date == today:
        return 'Today'
    if date == (today - one_day):
        return 'Yesterday'
    if date == (today + one_day):
        return 'Tomorrow'
    if today < date < (today + datetime.timedelta(days=7)):
        return date.strftime('%A')
    return date.strftime("%d %b")
