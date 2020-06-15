from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tags(models.Model):
    tagname = models.CharField(max_length = 255)

    def __str__(self):
        return self.tagname

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    branch = models.CharField(max_length = 255)
    gender = models.CharField(max_length = 1)
    #todo:make checks for mobile no.
    mob = models.IntegerField()
    tags = models.ManyToManyField(Tags,blank = True)
    profile_pic = models.ImageField(upload_to = "profiles/",default = 'profiles/default.png')

    def __str__(self):
        return self.user.username



