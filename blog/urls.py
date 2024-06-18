from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_create'),
    path('posts/<int:post_id>/comments/', views.get_post_comments, name='get_post_comments'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('comments/unapproved/', views.un_comments, name='unapproved_comments'),
    path('comments/<int:comment_id>/approve/', views.approve_comment, name='approve_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
