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
    path('blog/create', views.createblog, name='createblog'),
    path('blog/post', views.postblog, name='postblog'),
    path('blog/publish', views.publishblog, name='publishblog'),
    path('blog/edit/<int:blogid><returnpage>', views.editblog, name='editblog'),
    path('blog/delete/<int:blogid>', views.deleteblog, name='deleteblog'),
    path('authorpage/<author>', views.authorpage, name='authorpage'),
    path('blogpage/<int:blogid>', views.blogpage, name='blogpage'),
    path('comment/create/<int:blogid>', views.createcomm, name='createcomm'),
    path('comment/edit/<int:comid>', views.editcomm, name='editcomm'),
    path('comment/delete/<int:comid>', views.deletecomm, name='deletecomm'),
    path('approval-list', views.approvallist, name='approvallist'),
    path('comment/approve/<int:comid>', views.approvecomm, name='approvecomm'),
    path('account/delete/<int:userid>', views.deleteaccount, name='deleteaccount'),
]