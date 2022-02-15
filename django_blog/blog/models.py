from django.db import models
from django.urls import reverse


class Category(models.Model):
    """ Модель категорий"""

    title = models.CharField(max_length=255, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('categories', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title', ]


class Tag(models.Model):
    """Модель тегов"""

    title = models.CharField(max_length=50, verbose_name='Наименование тега')
    slug = models.SlugField(max_length=50, verbose_name='URL тега', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title', ]

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})


class Post(models.Model):
    """Модель постов"""

    title = models.CharField(max_length=255, verbose_name='Наименование поста')
    slug = models.SlugField(max_length=255, verbose_name='URL поста', unique=True)
    author = models.CharField(max_length=100, verbose_name='Автор')
    content = models.TextField(blank=True, verbose_name='Текст поста')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='posts'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name='Теги',
        related_name='posts'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def get_comment(self):
        return self.comments_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at', ]


class Comments(models.Model):
    """Модель комментариев"""

    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Текст комментария', max_length=5000)
    date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        verbose_name='Родитель',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.post}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
