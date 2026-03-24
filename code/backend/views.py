from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth.models import User

from .serializer import *
from .models import *


# ─── Register Parent ───
class Registeruser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {'data': serializer.data, 'token': token.key},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── Login ───
class LoginView(APIView):
    serializer_class = loginserializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            if check_password(password, user.password):
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── Logout ───
class logoutview(APIView):
    def post(self, request):
        logout(request)
        return Response({'msg': 'logout successfully'})


# ─── Child CRUD ───
class ChildListCreateView(generics.ListCreateAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class ChildDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


# ─── Vaccine Names CRUD ───
class VaxNameListCreateView(generics.ListCreateAPIView):
    queryset = VaxName.objects.all()
    serializer_class = VaxNameSerializer


class VaxNameDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VaxName.objects.all()
    serializer_class = VaxNameSerializer


# ─── Vaccine Cycle CRUD ───
class VaxCycleAPIView(generics.ListCreateAPIView):
    queryset = Vax_Cycle.objects.all()
    serializer_class = VaxCycleSerializer


class VaxCycleDelete_Update(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vax_Cycle.objects.all()
    serializer_class = VaxCycleSerializer


# ─── Vax CRUD ───
class VaxAPIView(generics.ListCreateAPIView):
    queryset = Vax.objects.all()
    serializer_class = VaxSerializer


class VaxDelete_Update(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vax.objects.all()
    serializer_class = VaxSerializer


# ─── Vaccination Dates ───
def vaccination_dates_view(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    vaccination_dates = child.get_vaccination_dates()
    vaccination_dates_str = [str(date) for date in vaccination_dates]
    return JsonResponse({'vaccination_dates': vaccination_dates_str})


# ─── Vaccine Names List ───
class VaccineListView(APIView):
    def post(self, request):
        a = VaccineNameSerializer(data=request.data)
        if a.is_valid():
            a.save()
            return Response(a.data)
        return Response(a.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        qs = vaccine_names.objects.all()
        a = VaccineNameSerializer(qs, many=True)
        return Response(a.data)


# ─── Vaccine Programs CRUD ───
class VaccineProgramsListCreateView(generics.ListCreateAPIView):
    queryset = VaccinePrograms.objects.all()
    serializer_class = VaccineProgramSerializer


class VaccineProgramsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VaccinePrograms.objects.all()
    serializer_class = VaccineProgramSerializer


# ─── Hospitals ───
class HospitalsAPIView(APIView):
    def get(self, request):
        hospitals = Hospitals.objects.filter(slots_available__gt=0)
        serializer = HospitalsSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalsSerializer(data=request.data)
        if serializer.is_valid():
            hospital_instance = serializer.save()
            vaccine_names_data = request.data.get('programs_available', [])
            if vaccine_names_data:
                programs_instances = VaccinePrograms.objects.filter(id__in=vaccine_names_data)
                hospital_instance.programs_available.set(programs_instances)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── Vaccine Booking ───
class VaccineBookingView(APIView):
    def post(self, request):
        serializer = VaccineBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        bookings = VaccineBooking.objects.filter(parent=request.user)
        serializer = VaccineBookingSerializer(bookings, many=True)
        return Response(serializer.data)
