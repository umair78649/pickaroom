from django.forms import ModelForm
from pickaroom.models import Booking
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone


class DateInput(forms.DateInput):
    input_type = 'date'
    format = "%Y-%m-%d"


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = [
            'start_date', 'duration', 'num_adults',
            'num_children'
        ]

        widgets = {
            'start_date': DateInput(
                format="%Y-%m-%d",
                attrs={
                    "min": str(timezone.now().date()),
                }),
        }



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2'
        ]
