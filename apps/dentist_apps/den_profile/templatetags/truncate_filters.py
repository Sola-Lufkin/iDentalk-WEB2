# -*- coding: utf8 -*-
from django import template
register = template.Library()

@register.filter("truncate_chars")
def truncate_chars(value, max_length):
    if len(value) <= max_length:
        return value

    truncd_val = value[:max_length]
    if value[max_length] != " ":
        rightmost_space = truncd_val.rfind(" ")
        if rightmost_space != -1:
            truncd_val = truncd_val[:rightmost_space]

    return truncd_val + "..."

# from django import template
# register = template.Library()

# @register.filter("truncate_chars")
# def truncate_chars(value, max_length):
#     if len(value) > max_length:
#         truncd_val = value[:max_length]
#         if not len(value) == max_length+1 and value[max_length+1] != " ":
#             truncd_val = truncd_val[:truncd_val.rfind(" ")]
#         print "filter works"
#         return  truncd_val + "..."
#     return value