from django import template
from django.http import QueryDict
from urllib.parse import urlencode
from django.template.defaultfilters import stringfilter

register = template.Library()

# Нормально работающий тег, который заменяет параметры url
@register.simple_tag(takes_context=True)
def replace_query_param(context, param, value):
    request = context['request']
    query_params = request.GET.copy()
    query_params.setlist(param, [value])
    return request.path + '?' + query_params.urlencode()