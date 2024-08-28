from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_article/', views.add_article, name='add_article'),
    path('edit_article/<slug:slug>/', views.edit_article, name='edit_article'),

    # Authentication URLs
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
