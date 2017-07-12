from django import template
from posts.models import Category

register = template.Library()

@register.inclusion_tag('categories.html')
def show_cat():
    categories = Category.objects.all()
    return { 'cats' : categories }
