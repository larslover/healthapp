from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    """Safely get attribute from object, return None if missing"""
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
def some_ticked(fields, checklist_dict):
    """Return True if any field in fields is ticked in checklist_dict."""
    return any(checklist_dict.get(f, False) for f in fields)