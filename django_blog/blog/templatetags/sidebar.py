from django import template

from blog.models import Post, Tag

register = template.Library()


@register.inclusion_tag('blog/popular_posts.html')
def get_popular_posts(cnt_posts=3):
    """
    Показывать популярные посты мы будем в сайдбаре. По умолчанию 3.
    """
    posts = Post.objects.order_by('-views')[:cnt_posts]
    return {'posts': posts}


@register.inclusion_tag('blog/tags.html')
def get_tags():
    """
    Показывать теги в сайдбаре.
    """
    tags = Tag.objects.all()
    return {'tags': tags}
