from django import template
# Модуль re (Regular Expression) предоставляет функциональность для работы с регулярными выражениями.
import re

register = template.Library()

@register.filter
def censor(value):
    unwanted_words = ['центра', 'кабмина', 'расставил', 'заявил']  # список нежелательных слов
    # Заменяем нежелательные слова на символ '*'
    for word in unwanted_words:
        value = re.sub(r'\b%s\b' % re.escape(word), '*' * len(word), value, flags=re.IGNORECASE)

    return value