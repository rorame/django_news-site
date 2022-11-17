from django import template
from django.db.models import Count, F
from news.models import Category

register = template.Library()


# декоратор функции
@register.simple_tag()
def get_categories():
    return Category.objects.all()


# пока отключил
@register.inclusion_tag('news/list_categories.html')
def show_categories():
    # categories = Category.objects.all()
    # categories = Category.objects.annotate(cnt=Count('get_news'))
    # добавляем фильтр новостей (считаем только те новости, которые опубликованы)
    categories = Category.objects.annotate(cnt=Count('get_news', filter=F('get_news__is_published')))
    return {"categories": categories}
