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
            # for splitting the name into first and last name
            name_arr = name.split(" ", 1)
            first = name_arr[0]
            last = name_arr[1] if len(name_arr) > 1 else ""

            user = User.objects.create_user(regno,email,regno,first_name = first,last_name = last)
            user.is_active = False
            user.save()


            UserProfile.objects.create(user = user,branch = branch,gender = gender,mob = mob)
            print("user",regno,"created successfully")
            count=count+1

        print(count,"user created successfully")
