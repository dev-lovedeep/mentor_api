from rest_framework import serializers
from .models import UserProfile,User
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text


def user_of_email_token(uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return user


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value



class UserProfileSerializer(serializers.ModelSerializer):
    user = StringSerializer(many=False)
    tags = StringSerializer(many=True)
    # full_name = serializers.CharField()
    class Meta:
        model = UserProfile
        fields = '__all__'



class UserOnboardingSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    uidb64 = serializers.CharField()
    email_token = serializers.CharField()
    regno = serializers.IntegerField()
    profile_pic = serializers.ImageField(required = False,allow_null=True, allow_empty_file=True, use_url=True)
    class Meta:
        model = UserProfile
        fields = ['mob','password','password2','regno','profile_pic','uidb64','email_token']

    def save(self):
        # this is the user whose data is to be changed
        user = User.objects.get(username = self.validated_data['regno'])
        print("user",user)

        uidb64 = self.validated_data['uidb64']
        email_token = self.validated_data['email_token']
        email_token_user  = user_of_email_token(uidb64, email_token)
        print(email_token_user)
        #if the user whose data is to be changed 
        # and the one who is trying to change(the token user)
        # is not same then return error msg
        if user!=email_token_user:
            raise serializers.ValidationError({"error":"bad request."})

        if user.is_active:
            raise serializers.ValidationError({"error":"user already onboarded"})
        user_profile = UserProfile.objects.get(user = user)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        profile_pic = self.validated_data['profile_pic']
        if profile_pic:
            user_profile.profile_pic = profile_pic

        if password!=password2:
            raise serializers.ValidationError("password must match.")
        user.set_password(password)
        user_profile.mob = self.validated_data['mob']
        user.save()
        user_profile.save()

        return user 
        

class NewUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    regno = serializers.IntegerField()
    class Meta:
        model = UserProfile
        fields = ['mob','branch','gender','name','email','regno']