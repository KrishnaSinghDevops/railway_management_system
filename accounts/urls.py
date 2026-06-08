from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_page, name='login_page'),
    path('accounts/login', views.login_user, name='login_user'),
    path('create/user', views.register_page, name='register_page'),
    path('save/user', views.register_save, name='register_save'),
    path('logout/', views.logout_user, name='logout_user'),

]
