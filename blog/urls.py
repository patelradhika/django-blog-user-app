from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000 --> local
    # mydjangosite.com --> online
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('login', views.cust_login, name='login'),
    path('logout', views.cust_logout, name='logout'),
    path('account', views.useraccount, name='useraccount'),
]