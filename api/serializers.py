from rest_framework import serializers
from .models import UserProfile,User

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class send_mail_serializer(serializers.Serializer):
    regno = serializers.CharField(required = True,max_length = 8)

class UserProfileSerializer(serializers.ModelSerializer):
    user = StringSerializer(many=False)
    tags = StringSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserOnboardingSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    regno = serializers.IntegerField()
    profile_pic = serializers.ImageField(required = False,allow_null=True, allow_empty_file=True, use_url=True)
    class Meta:
        model = UserProfile
        fields = ['mob','password','password2','regno','profile_pic']

    def save(self):
        user = User.objects.get(username = self.validated_data['regno'])
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
        