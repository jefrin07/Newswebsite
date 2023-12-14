from django.urls import path
from django.contrib.auth import views as auth_views  # Import auth_views from django.contrib.auth
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),  # Ensure consistency with trailing slash
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', views.user_logout, name='logout'),
    path('create-post/', views.create_post, name='createpost'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('update/<int:post_id>/', views.update_post, name='update_post'),
    path('pending/', views.pending_posts, name='pending_posts'),
    path('reject/<int:post_id>/', views.reject_post, name='reject_post'),
    path('post-status/', views.post_status, name='post_status'),
    path('all_users/', views.view_all_users, name='all_users'),
    path('search/', views.searchBar, name='search')
    
]
