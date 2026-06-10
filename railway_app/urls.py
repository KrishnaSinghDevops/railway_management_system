from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/train/', views.search_train, name='search_train'),
    path('book/ticket/<int:train_id>/', views.book_ticket, name='book_ticket'),
    path('my/bookings/', views.my_bookings, name='my_bookings'),
    path('get/stations/', views.get_station, name='get_stations'),

]

