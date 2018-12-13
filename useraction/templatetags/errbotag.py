from django import template

register=template.Library()

@register.simple_tag
def changevalue(x):
    if x==0:
        return "启用"
    else:
        return "禁用"