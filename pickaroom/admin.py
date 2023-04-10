from pickaroom.models import Hotel, Booking, Room, RoomType
from django.contrib import admin


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ["name", "post_code", "star_rating"]
    list_filter = ["star_rating"]
    search_fields = ["name", "post_code", "address", "features"]
    ordering = ["name"]


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    ordering = ["name"]
    search_fields = ["name", "description"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["hotel", "room_type", "floor", "room_no", "cost"]
    search_fields = ["hotel__name"]
    ordering = ["hotel", "floor", "row", "column"]
    list_select_related = ["hotel", "room_type"]
    list_filter = ["room_type", "floor"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["reference_no", "guest", "booked_rooms", "start_date", "total_price"]
    search_fields = ["guest__first_name", "guest__last_name"]
    ordering = ["-start_date", "-duration"]
    list_select_related = ["guest"]
    list_filter = ["duration", "start_date", "num_adults", "num_children"]
    readonly_fields = ["reference_no"]
    filter_horizontal = ["rooms"]