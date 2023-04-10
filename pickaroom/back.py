import json
import os
from datetime import datetime, timedelta

from django import db
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from pickaroom.models import Booking, Hotel, Room, RoomType


def book(request, hotel_id):
    data = request.POST.dict()

    rooms = data["selected_buttons"].split(",")
    duration = data["duration"]

    start_date = datetime.strptime(data["start_date"], '%Y-%m-%d')
    end_date = start_date + timedelta(days=int(duration))

    room_ids = Room.objects.filter(
        hotel_id=hotel_id,
        room_no__in=rooms
    ).values_list("id", flat=True)

    booked_rooms = Booking.objects.filter(
        rooms__in=room_ids,
        start_date__gte=start_date,
        start_date__lt=end_date
    )

    if booked_rooms.exists():
        messages.warning(
            "Some rooms have already been booked and so is unavailable")
        return 400

    # save the booking to the database
    booking = Booking(
        guest=request.user,
        start_date=start_date,
        duration=duration,
        num_children=data["num_children"],
        num_adults=data["num_adults"]
    )

    booking.save()
    booking.rooms.set(room_ids)
    # send the confirmation
    return 200


def book_delete(request):
    booking = Booking.objects.filter(start_date=request.date,
                                     rooms__in=[request.room_id],
                                     guest_id=request.user)
    if booking.exists():
        booking.delete()
        return 200
    else:
        return 404


def populate_hotels():

    standard = RoomType.objects.create(
        Type="Standard",
        cost=100.00,
        description="A lovely standard double room with ensuite bathroom")
    # Create a hotel with 200 rooms
    grand_hotel = Hotel.objects.create(
        hotel_id="1",
        name='The Grand Hotel',
        floors=5,
        Structuremaplink='https://grandhotel.com/structuremap.png',
        PostCode='12345',
        starRating=5,
        Address='123 Main Street')
    for i in range(200):
        room_number = str(i + 1).zfill(3)
        room_id = f"{grand_hotel.hotel_id}-{room_number}"
        Room.objects.create(
            RoomID=room_id,
            status=True,
            size=2,
            floor=(i % 5) + 1,  # distribute the rooms evenly between 5 floors
            Roomtype=RoomType.objects.first(),
            hotel_id=grand_hotel)
    # Create a hotel with 40 rooms
    cozy_inn = Hotel.objects.create(
        hotel_id="2",
        name='The Cozy Inn',
        floors=2,
        Structuremaplink='https://cozyinn.com/structuremap.png',
        PostCode='54321',
        starRating=3,
        Address='456 Side Street')
    for i in range(40):
        room_number = str(i + 1).zfill(3)
        room_id = f"{cozy_inn.hotel_id}-{room_number}"
        Room.objects.create(
            RoomID=room_id,
            status=True,
            size=2,
            floor=(i % 2) + 1,  # distribute the rooms evenly between 2 floors
            Roomtype=RoomType.objects.first(),
            hotel_id=cozy_inn)

    return 200


def get_bookings():
    return Booking.objects.all()


def get_all_rooms():
    return "done"


def create_rooms(rooms):
    bookable_rooms = []
    floor_nums = rooms.order_by("floor").values_list(
        "floor", flat=True).distinct()

    for floor in floor_nums:
        rooms_in_floor = rooms.filter(floor=floor)
        num_rows = rooms_in_floor.order_by(
            "row").values_list("row", flat=True).distinct()

        rooms_in_rows = []
        for row in num_rows:
            rooms_in_row = rooms_in_floor.filter(row=row)
            rooms_in_rows.append(rooms_in_row)

        bookable_rooms.append(rooms_in_rows)

    return bookable_rooms
