from django.core.management.base import BaseCommand
import json
from api.models import User,UserProfile

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('file_name',type=str,help = "the student data json file")

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}') as file:
            student_list = json.load(file)
        count=0
        for student in student_list:
            branch = student['Branch']
            gender = student['Gender']
            mob = student['mobile']
            regno = student['Regno']
            name = student['Name']
            email = student['email']
            user = User.objects.create_user(regno,email,regno)
            user.is_active = False
            user.save()

            UserProfile.objects.create(user = user,branch = branch,gender = gender,mob = mob)
            print("user",regno,"created successfully")
            count=count+1

        print(count,"user created successfully")
