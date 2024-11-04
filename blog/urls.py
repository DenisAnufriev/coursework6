from django.urls import path
from django.views.decorators.cache import cache_page
from blog.views import BlogListView, BlogCreateView, BlogDeleteView, BlogUpdateView, toggle_activity, BlogDetailView
from blog.apps import BlogConfig

app_name = BlogConfig.name

# urlpatterns = [
#     path('', BlogListView.as_view(), name='blog_list'),
#     path('view/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
#     path('create/', BlogCreateView.as_view(), name='blog_create'),
#     path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
#     path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
#     path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
# ]