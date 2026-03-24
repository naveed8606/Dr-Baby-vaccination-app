from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path('register/', Registeruser.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logoutview.as_view(), name='logout'),

    # Child
    path('children/', ChildListCreateView.as_view(), name='child-list'),
    path('children/<int:pk>/', ChildDetailView.as_view(), name='child-detail'),

    # Vaccine Names
    path('vaxnames/', VaxNameListCreateView.as_view(), name='vaxname-list'),
    path('vaxnames/<int:pk>/', VaxNameDetailView.as_view(), name='vaxname-detail'),

    # Vaccine Cycles
    path('vaxcycles/', VaxCycleAPIView.as_view(), name='vaxcycle-list'),
    path('vaxcycles/<int:pk>/', VaxCycleDelete_Update.as_view(), name='vaxcycle-detail'),

    # Vaccinations
    path('vax/', VaxAPIView.as_view(), name='vax-list'),
    path('vax/<int:pk>/', VaxDelete_Update.as_view(), name='vax-detail'),
    path('vaccination-dates/<int:child_id>/', vaccination_dates_view, name='vaccination-dates'),

    # Vaccine Names & Programs
    path('vaccine-names/', VaccineListView.as_view(), name='vaccine-names'),
    path('vaccine-programs/', VaccineProgramsListCreateView.as_view(), name='vaccine-programs'),
    path('vaccine-programs/<int:pk>/', VaccineProgramsDetailView.as_view(), name='vaccine-program-detail'),

    # Hospitals
    path('hospitals/', HospitalsAPIView.as_view(), name='hospitals'),

    # Bookings
    path('bookings/', VaccineBookingView.as_view(), name='bookings'),
]
