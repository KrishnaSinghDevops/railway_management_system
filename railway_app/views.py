from django.shortcuts import render, redirect
from railway_management.decorators import user_required
import random

from datetime import datetime
from django.contrib import messages
from .models import Train, Booking
from common.common_util import *

@user_required
def dashboard(request):

    query = """
    SELECT COUNT(*) AS TOTAL_TRAINS
    FROM TRAINS
    """

    result = select_query(query)

    total_trains = 0

    if result:
        total_trains = result[0]['TOTAL_TRAINS']

    context = {
        'username': request.session.get('USERNAME'),
        'total_trains': total_trains
    }

    return render(request, 'dashboard.html', context)

@user_required
def search_train(request):
    trains = []
    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        trains = Train.objects.filter(SOURCE_STATION__icontains=source, DESTINATION_STATION__icontains=destination)
    return render(request, 'search_train.html', {
        'trains': trains
    })

@user_required
def book_ticket(request, train_id):
    train = Train.objects.get(TRAIN_ID=train_id)
    if request.method == 'POST':
        passenger_name = request.POST.get('passenger_name')
        passenger_age = request.POST.get('passenger_age')
        passenger_gender = request.POST.get('passenger_gender')
        journey_date = request.POST.get('journey_date')
        if train.AVAILABLE_SEATS <= 0:
            return JsonResponse({
                "status": 400,
                "message": "No Seats Available"
            })

        pnr = "PNR" + str(random.randint(100000, 999999))
        seat_number = "S" + str(train.TOTAL_SEATS - train.AVAILABLE_SEATS + 1)

        Booking.objects.create(

            PNR_NUMBER=pnr,
            USER_ID=request.session.get('USER_ID'),
            TRAIN_ID=train.TRAIN_ID,
            JOURNEY_DATE=journey_date,
            PASSENGER_NAME=passenger_name,
            PASSENGER_AGE=passenger_age,
            PASSENGER_GENDER=passenger_gender,
            SEAT_NUMBER=seat_number,
            STATUS='CONFIRMED',
            CREATED_AT=datetime.now(),
            BOOKED_BY =  request.session.get('USERNAME')


        )

        train.AVAILABLE_SEATS -= 1
        train.save()
        messages.success(request, f'Ticket Booked Successfully | PNR : {pnr}')
        return JsonResponse({
            "status": 200,
            "msg": f"Ticket Booked Successfully",
            "pnr": pnr
        })
    return render(request, 'book_ticket.html', {'train': train})
@user_required
def my_bookings(request):

    user_id = request.session.get('USER_ID')

    bookings = Booking.objects.filter(
        USER_ID=user_id
    ).order_by('-BOOKING_ID')

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })
from django.http import JsonResponse
from django.db import connection

@user_required
def get_station(request):
    stations = []
    with connection.cursor() as cursor:
        cursor.execute(""" SELECT DISTINCT SOURCE_STATION FROM TRAINS
            UNION
            SELECT DISTINCT DESTINATION_STATION FROM TRAINS""")
        rows = cursor.fetchall()
    for row in rows:
        stations.append(row[0])
    return JsonResponse(stations, safe=False)