from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tags/', views.tag_index, name='tag_index'),
    path('tags/<str:tag_name>/', views.tag_detail, name='tag_detail'),
    path('posts/create/', views.create_post, name='post_detail'),
    path("simple-form/", views.simple_form_view, name="simple_form"),
    path("post-form/", views.post_form_view, name="post_form"),
    path("test-markdownify/", views.test_markdownify, name="test_markdownify"),

]