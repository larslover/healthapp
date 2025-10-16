from django import template

register = template.Library()

@register.filter
def getattr(obj, attr_name):
    return getattr(obj, attr_name, None)

@register.filter
def replace(value, args):
    """Usage: {{ value|replace:"old,new" }}"""
    old, new = args.split(',')
    return value.replace(old, new)

# -----------------------------
# Add this dict_get filter
@register.filter
def dict_get(d, key):
    """Safely get a value from a dict, returns None if key doesn't exist"""
    if d is None:
        return None
    return d.get(key)
