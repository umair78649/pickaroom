from django.db import models
from pickaroom.utils import generate_reference_no
from django.utils.timezone import now, timedelta


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    features = models.TextField(null=True, blank=True)

    structure_map_link = models.CharField(
        max_length=100, null=True, blank=True)
    post_code = models.CharField(max_length=10)
    star_rating = models.PositiveSmallIntegerField()
    address = models.TextField(max_length=200)
    image = models.ImageField(blank=True, null=True,
                              upload_to="images/")

    class Meta:
        ordering = ["name"]
        unique_together = ["name", "post_code"]

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image:
            return self.image.url

    @property
    def features_as_list(self):
        features = self.features.replace("\r", "").split("\n\n")
        return features


class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(
        "pickaroom.Hotel", on_delete=models.CASCADE, null=True)
    room_type = models.ForeignKey(
        "pickaroom.RoomType", on_delete=models.CASCADE, null=True)
    floor = models.PositiveSmallIntegerField()
    room_no = models.CharField(max_length=10, verbose_name="room number")
    row = models.PositiveSmallIntegerField()
    column = models.PositiveSmallIntegerField()
    size = models.PositiveSmallIntegerField()

    cost = models.FloatField(default=0)


    class Meta:
        ordering = ["hotel", "floor", "row", "column"]
        unique_together = ["hotel", "room_type",
                           "room_no", "row", "column", "floor"]

    def __str__(self):
        return f"{self.hotel.name} ({self.room_no})"


class Booking(models.Model):
    reference_no = models.CharField(
        unique=True, max_length=20, default=generate_reference_no)
    guest = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    rooms = models.ManyToManyField("pickaroom.Room")
    start_date = models.DateField(default=now)
    duration = models.PositiveSmallIntegerField(default=1)
    num_adults = models.PositiveSmallIntegerField(default=1)
    num_children = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-start_date", "-duration"]

    def __str__(self):
        return self.reference_no

    @property
    def end_date(self):
        return self.start_date + timedelta(self.duration)

    @property
    def booked_rooms(self):
        rooms = self.rooms.all().values_list("room_no", flat=True)
        return ", ".join(rooms)

    @property
    def total_price(self):
        room_costs = sum(self.rooms.all().values_list("cost", flat=True))
        return room_costs * self.duration
