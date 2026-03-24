from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class loginserializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = '__all__'


class VaxNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaxName
        fields = '__all__'


class VaxCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vax_Cycle
        fields = '__all__'


class VaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vax
        fields = '__all__'


class VaccineNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = vaccine_names
        fields = '__all__'


class VaccineProgramSerializer(serializers.ModelSerializer):
    vaccines = VaccineNameSerializer(many=True, read_only=True)

    class Meta:
        model = VaccinePrograms
        fields = '__all__'


class HospitalsSerializer(serializers.ModelSerializer):
    programs_available = VaccineProgramSerializer(many=True, read_only=True)

    class Meta:
        model = Hospitals
        fields = '__all__'


class VaccineBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineBooking
        fields = '__all__'
