from django.urls import path
from admin_panel import views


urlpatterns = [
    path('admin/user', views.admin_dashboard, name='admin_dashboard'),
    path('user/list', views.user_list, name='add_user'),
    path('user/inline/update', views.user_inline_update, name="user_inline_update"),
    path('user/delete', views.delete_user, name="delete_user"),
    path('add/train', views.add_train_form, name='add_train'),
]
    

