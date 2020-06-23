from django.db import models
from django.contrib.auth.models import User

#for generating tokens
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.user.username
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = "{} {}".format(self.user.first_name,self.user.last_name)
        print("saving",self.name)
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



