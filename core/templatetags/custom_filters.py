from django import template
from datetime import date

register = template.Library()

@register.filter
def getattr(obj, attr_name):
    return getattr(obj, attr_name, None)

@register.filter
def replace(value, args):
    """Usage: {{ value|replace:"old,new" }}"""
    old, new = args.split(',')
    return value.replace(old, new)

@register.filter
def dict_get(d, key):
    """Safely get a value from a dict, returns None if key doesn't exist"""
    if d is None:
        return None
    return d.get(key)

@register.filter
def age_at_screening(dob, screen_date):
    if not dob or not screen_date:
        return ''
    years = screen_date.year - dob.year
    months = screen_date.month - dob.month
    if screen_date.day < dob.day:
        months -= 1
    if months < 0:
        years -= 1
        months += 12
    return f"{years}y {months}m"
