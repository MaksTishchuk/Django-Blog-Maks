from django import template

from blog.models import Category, Tag


register = template.Library()


@register.inclusion_tag('blog/menu_categories.html')
def show_menu_categories(menu_class='menu'):
    """
    Показывать категории мы будем в двух местах - в хедере и футере.
    У них определены свои классы в шаблонах _header and _footer. Поэтому мы
    передаем класс menu_class. По умолчанию стоит класс из хедера.
    """
    categories = Category.objects.all()
    return {'categories': categories, 'menu_class': menu_class}


@register.inclusion_tag('blog/menu_tags.html')
def show_menu_tags(menu_class='menu'):
    """
    Показывать категории мы будем в двух местах - в хедере и футере.
    У них определены свои классы в шаблонах _header and _footer. Поэтому мы
    передаем класс menu_class. По умолчанию стоит класс из хедера.
    """
    tags = Tag.objects.all()
    return {'tags': tags, 'menu_class': menu_class}
