from django.core.management.base import BaseCommand
from django.conf import settings
from company.models import Company
from usermanagement.models import User
from jobs.models import Status,Settings
# from usermanagement.seed_data_files.Skills import SKILLS
#
# def add_skills():
#
#     try:
#
#         Skill.objects.bulk_create(
#             [Skill(id=skill[0], skill=skill[1]) for skill in SKILLS ]
#         )
#         print("Skills Data added.")
#     except:
#         print("Skills Data already saved")

def add_date_configaration_jpa() :
    try :
        Settings.objects.create(key = "grace_field",
                                value = "45")
        print("date configarationg saved")

    except :
        print("date configarationg already saved")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Running setup...")
        if Company.objects.filter(company_name=settings.DEFAULT_COMPANY).exists() :
           company= Company.objects.get(company_name=settings.DEFAULT_COMPANY)
        else:
            company= Company.objects.create(company_name=settings.DEFAULT_COMPANY)
            print("creating default company")
            print("created company")

        if User.objects.filter(email=settings.DEFAULT_EMAIL).exists():
            print("Admin already present")
        else:
            print("Creating SuperUser")
            user = User.objects.create(email=settings.DEFAULT_EMAIL,
                                       password=settings.DEFAULT_PASSWORD,
                                       first_name='Admin', last_name='admin', is_super_user=True)

            user.set_password(settings.DEFAULT_PASSWORD)
            user.save()
            company.created_by = user
            company.updated_by = user
            company.save()
            print("Admin created Successfully")
            print("setup successfull")

        if Status.objects.all().exists() == False:
            print("Creating Status")
            status1 = Status.objects.create(status=settings.DEFAULT_STATUS1 ,future_state = 2,status_value=1)
            status1.save()
            status2 = Status.objects.create(status=settings.DEFAULT_STATUS2 , level = [2],status_value=1)
            status2.save()
            status3 = Status.objects.create(status=settings.DEFAULT_STATUS3 , future_state = 3 , level = [2],status_value=1)
            status3.save()
            status4 = Status.objects.create(status=settings.DEFAULT_STATUS4 , future_state = 4 , level = [3],status_value=1)
            status5 = Status.objects.create(status=settings.DEFAULT_STATUS5 , future_state = 5 , level = [4],status_value=1)
            status6 = Status.objects.create(status=settings.DEFAULT_STATUS6 ,   level = [2,3,4,5],status_value=1)
            status7 = Status.objects.create(status=settings.DEFAULT_STATUS7 , future_state = 6 , level = [3,4,5],status_value=1)
            status8 = Status.objects.create(status=settings.DEFAULT_STATUS8  , level = [6],status_value=1)
            status4.save()
            status5.save()
            status6.save()
            status7.save()
            status8.save()

            status9 = Status.objects.create(status="Active",status_value=2)
            status10 = Status.objects.create(status="Hold",status_value=2)
            status11 = Status.objects.create(status="Closed",status_value=2)
            status9.save()
            status10.save()
            status11.save()

            print("Status created")
        else:
            print("Status object already present")

        print("setup successful")



    add_date_configaration_jpa()
