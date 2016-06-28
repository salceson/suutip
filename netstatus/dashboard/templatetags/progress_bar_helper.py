from django import template

register = template.Library()


@register.simple_tag
def progress_bar_width(this_count, obj_count, max_value):
    return "%.2f" % (float(this_count) / float(obj_count) * float(max_value))
