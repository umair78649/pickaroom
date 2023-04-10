from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from pickaroom import views

urlpatterns = [
    path('hotel/<int:hotel_id>/', views.hotel, name="hotel"),
    path('booking/<int:hotel_id>/', views.booking, name="booking"),
    path('delete-booking', views.delete_booking, name="delete-booking"),
    path('populate/', views.populate, name="populate"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('get_bookings/', views.get_bookings, name='get_bookings'),
    path('get_rooms/', views.get_rooms, name='get_rooms'),
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
