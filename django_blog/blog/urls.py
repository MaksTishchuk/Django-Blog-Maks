from django.urls import path
from .views import PostListView, PostsByCategory, PostsByTag, PostDetailView, Search, AddComment

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='categories'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('review/<str:slug>/', AddComment.as_view(), name='add_comment'),
]
