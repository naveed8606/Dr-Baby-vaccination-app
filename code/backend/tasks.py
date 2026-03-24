from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import send_mail
from babyvaccinepro import settings
from .models import *


@shared_task(bind=True)
def send_mail_based_on_dates(self):
    """Send vaccination reminder emails based on baby's vaccination schedule."""
    recently_registered_user = User.objects.order_by('-date_joined').first()

    if recently_registered_user:
        recent_user_email = recently_registered_user.email
        children = Child.objects.filter(parent=recently_registered_user)

        for child in children:
            # Map health review dates to corresponding program IDs
            health_review_program_mapping = {
                (child.date_of_birth + timedelta(days=40)): [1],
                (child.date_of_birth + timedelta(days=67)): [2],
                (child.date_of_birth + timedelta(days=70)): [3],
                (child.date_of_birth + timedelta(days=89)): [4],
                (child.date_of_birth + timedelta(days=180)): [5],
                (child.date_of_birth + timedelta(days=304)): [6],
                (child.date_of_birth + timedelta(days=363)): [7],
            }

            for rev_date, program_ids in health_review_program_mapping.items():
                if rev_date == timezone.localtime(timezone.now()).date():
                    user = child.parent
                    mail_subject = "Health Review Date Reminder"

                    programs = VaccinePrograms.objects.filter(id__in=program_ids)

                    message = (
                        f"Hi {user.username}, This is a reminder for a health "
                        f"review appointment today for {child.first_name}.\n"
                    )

                    if programs.exists():
                        for program in programs:
                            message += "\nVaccines Are:\n"
                            for vaccine_info in program.vaccines.all():
                                message += f"  - {vaccine_info.vaccine}\n"
                    else:
                        message += "No relevant vaccination programs found."

                    send_mail(
                        subject=mail_subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[recent_user_email],
                        fail_silently=True,
                    )

    return "done"
