from django.urls import path
from . import views
from . import admin_views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_f, name='logout'),
    path('tags/', views.tag_index, name='tag_index'),
    path('posts/', views.post_index, name='posts'),
    path('tags/<str:tag_name>/', views.tag_detail, name='tag_detail'),
    path('dashboard/', admin_views.index, name='dashboard'),
    path('dashboard/posts/', admin_views.post_index, name='admin_post'),
    path('dashboard/posts/create/', admin_views.create_post, name='admin_post_create'),
    path('dashboard/posts/<int:post_id>/published/<str:is_published>', admin_views.published_post, name='admin_post_published'),
    path('dashboard/posts/<int:post_id>/update', admin_views.update_post, name='admin_post_update'),
    path('dashboard/posts/<int:post_id>/delete', admin_views.delete_post, name='admin_post_delete'),
    path('dashboard/tags/', admin_views.tag_index, name='admin_tag'),
    path('dashboard/tags/create/', admin_views.create_tag, name='admin_tag_create'),
    path('dashboard/tags/<int:id>/update/', admin_views.update_tag, name='admin_tag_update'),
    path('dashboard/tags/<int:id>/delete/', admin_views.delete_tag, name='admin_tag_delete'),
    path('posts/create/', views.create_post, name='post_detail'),
    path("simple-form/", views.simple_form_view, name="simple_form"),
    path("post-form/", views.post_form_view, name="post_form"),
    path("post/<int:post_id>", views.post_detail, name="post"),
    path("test-markdownify/", views.test_markdownify, name="test_markdownify"),
]