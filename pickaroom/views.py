from django.contrib import messages
from django.contrib.auth import login as user_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from pickaroom import back
from pickaroom.forms import BookingForm, RegisterForm
from pickaroom.models import Booking, Hotel, Room


# @login_required
def home(request):
    hotels = Hotel.objects.order_by("name")

    context = {
        'hotels': hotels
    }

    return render(request, "index.html", context)


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_login(request, user)
            messages.success(request, 'REGISTRATION SUCCESSFUL!')
            return redirect('login')

    context = {
        'form': form
    }

    return render(request, "register.html", context)


@login_required
def hotel(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)

    context = {
        "hotel": hotel
    }

    return render(request, "hotel_detail.html", context)


@login_required
def get_bookings(request):
    return JsonResponse({"bookings": back.get_bookings()})


@login_required
def get_rooms(request):
    return JsonResponse({"rooms": back.get_all_rooms()})


@login_required
def booking(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)

    if request.method == "POST":
        back.book(request, hotel_id)
        return redirect('/')

    elif request.method == "GET":
        rooms = Room.objects.filter(hotel_id=hotel_id)
        booked_rooms = Booking.objects.filter(
            rooms__hotel_id=hotel_id,
        ).values_list("rooms", flat=True)
        booked_room_ids = list(
            booked_rooms.values_list("rooms__room_no", flat=True))

        bookable_rooms = back.create_rooms(rooms)
        form = BookingForm()

        context = {
            'form': form,
            "hotel": hotel,
            "bookable_rooms": bookable_rooms,
            "booked_rooms": booked_rooms,
            "booked_room_ids": booked_room_ids
        }

        return render(request, "booking.html", context)

@login_required
def delete_booking(request):
    data = request.POST.dict()
    hotel_id = data.get('hotelId')
    room_no = data.get('roomNo')
    deleted = False

    if request.method == 'POST':
        booking = Booking.objects.filter(rooms__room_no=room_no, rooms__hotel_id=hotel_id)
        booking.delete()
        deleted = True
    
    return JsonResponse({'deleted': deleted},safe=True)
        
@login_required
def populate(request):
    back.populate_hotels()
    response = redirect('/')
    return response


@login_required
def availability(request, hotel_id):
    if request.method == 'POST':
        pass
        # update the field value in the database
    return JsonResponse({'message': 'Field value updated'})
