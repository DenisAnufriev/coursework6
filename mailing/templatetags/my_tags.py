from django import template

register = template.Library()


@register.filter()
def my_media(val):
    if val:
        return f"/media/{val}"
    else:
        return "Тут ничего нет, к сожалению (("