from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Child(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_vaccination_dates(self):
        """Returns a list of vaccination dates based on the child's date of birth."""
        schedule_days = [40, 67, 70, 89, 180, 304, 363]
        return [self.date_of_birth + timedelta(days=d) for d in schedule_days]


class vaccine_names(models.Model):
    vaccine = models.CharField(max_length=100)

    def __str__(self):
        return self.vaccine


class VaccinePrograms(models.Model):
    program_name = models.CharField(max_length=200)
    vaccines = models.ManyToManyField(vaccine_names, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.program_name


class VaxName(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vax_Cycle(models.Model):
    cycle_name = models.CharField(max_length=100)
    age_in_days = models.IntegerField()
    vaccines = models.ManyToManyField(VaxName, blank=True)

    def __str__(self):
        return self.cycle_name


class Vax(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine = models.ForeignKey(VaxName, on_delete=models.CASCADE)
    date_given = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.child.first_name} - {self.vaccine.name}"


class Hospitals(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    slots_available = models.IntegerField(default=0)
    programs_available = models.ManyToManyField(VaccinePrograms, blank=True)

    def __str__(self):
        return self.name


class VaccineBooking(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_email = models.EmailField()
    hospital = models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    vaccine_program = models.ForeignKey(VaccinePrograms, on_delete=models.SET_NULL, null=True)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.parent.username} at {self.hospital.name}"
