from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Tag, Post, Comments


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(label='Текст поста', widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'views', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', )
    list_filter = ('category', 'tags',)
    readonly_fields = ('views', 'created_at', 'get_photo')
    fields = (
        'title', 'slug', 'category', 'tags', 'content', 'photo', 'get_photo', 'created_at', 'views'
    )

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return '-'

    get_photo.short_description = 'Миниатюра'


class CommentsInline(admin.TabularInline):
    """Комментарии на странице поста"""

    model = Comments
    extra = 1
    readonly_fields = ('name', )


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('id', 'name', 'post', 'parent')
    list_display_links = ('name',)
    search_fields = ('name', 'post__title')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
