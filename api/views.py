from rest_framework import status,generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from api.emails.tokens import account_activation_token
from django.utils.encoding import force_bytes,force_text
from django.shortcuts import HttpResponse
from .models import UserProfile
from .serializers import UserProfileSerializer,UserOnboardingSerializer,NewUserSerializer,user_of_email_token
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value

# api 
# call:http://localhost:8000/api/signup/20198042
# return:{"error":"what ever the msg be"} or{"success":"confirmation mail send"}
def api_signup_view(request,regno):
    
    try:
        user = User.objects.get(username = regno)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    response = {}
    if not user:
        response['error'] = "invalid registratino no."
        return JsonResponse(response)
    if user.is_active:
        response['error'] = "account already exist with this registratino no."
        return JsonResponse(response)
    #mailing process start here
    #todo:change current site to react site url in production
    current_site = get_current_site(request)
    subject = 'Activate Your MNNIT Mentor Account'
    message = render_to_string('api/emails/account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        #todo:look whehter .decocde() is requiered at end or not
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)
    response['success']="a confirmation link has been sent to your registered mail id."
    return JsonResponse(response)





# api : this api verify email token
# call:http://localhost:8000/api/verify/<uid>/<token>/
# return:{"success":"true","student":student deatials,"token":token} if email_verification_token is valid
#         {"success":"false"} if token is invalid 
def api_verify_token(request, uidb64, token):
    # user_of_email_token is created by me imported from serializers
    user = user_of_email_token(uidb64,token)

    if user is not None and account_activation_token.check_token(user, token):
            student= UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(student,many=False)
            token = Token.objects.get(user=user).key
            return JsonResponse({"success":'true',"student":serializer.data,"token":token})
    return JsonResponse({"success":'false'})


# api 
# call:[post only] http://localhost:8000/api/onboard/
# body of api call:[mob,password,password2,regno,uidb64,email_token]
# return:{"success":"true","username":regno}
#         {errors} if any problem with the form
        #  {"error":"bad request."} if the email token did not matched to the user
#           {"error":"user already onboarded"} if api fired for already onboarded(active) user
# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def api_onboarding(request):
    serializer = UserOnboardingSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        user = serializer.save()
        print(user)
        user.is_active = True
        user.save()
        # token = Token.objects.get(user=user).key
        data['success'] = "true"
        data['username'] = user.username
        # data['token'] = token
    else:
        data = serializer.errors
    return JsonResponse(data)




def is_valid_queryparam(param):
    return param != '' and param is not None


def filter(request):
    name_or_rengo_query = request.GET.get('query')
    branch_query = request.GET.get('branch')
    tag_query = request.GET.get('tag')
    qs = UserProfile.objects.all()
    qs = qs.annotate(
                full_name=Concat(
                    'user__first_name',
                    Value(' '),
                    'user__last_name'
                )
            )
    if is_valid_queryparam(name_or_rengo_query):  
        qs = qs.filter(Q(full_name__icontains=name_or_rengo_query)
                       | Q(user__username__icontains=name_or_rengo_query)
                       ).distinct()
    if is_valid_queryparam(branch_query) and branch_query!="all":
        qs = qs.filter(branch__icontains = branch_query)
    if is_valid_queryparam(tag_query) and tag_query!="all":
        qs = qs.filter(tags__tagname = tag_query)

    print(qs[0].full_name)
    return qs


# api 
# call:[get only] http://localhost:8000/api/filter/?query=love&branch=it&tag=django
# or blank call will return whole databse http://localhost:8000/api/filter/
# return:
# [
#     {
#         "id": id,
#         "branch": "branch",
#         "gender": "m",
#         "mob": mobile no.,
#           "name":"full name",
#         "profile_pic": "http://localhost:8000/media/profiles/default.png",
#         "user": 20198042,
#         "tags": [
#             "django"
#         ]

#     }
# ]
class api_filter_view(generics.ListAPIView):
    APIView=['GET',]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return filter(self.request)

    serializer_class = UserProfileSerializer


    # def list(self, request, *args, **kwargs):
    #     qs = self.get_queryset()
    #     response = super().list(request, args, kwargs)
    #     serializer = self.get_serializer(instance = qs, many=True)

    #     serializer_data = serializer.data # get the default serialized data 
    #     serializer_data.append({"DISCOUNT": 210})
    #     return Response(serializer_data)


# api 
# call:[get only] http://localhost:8000/api/detail/<regno>/
#[auth token required]
# return:
# [
#     {
#         "id": id,
#         "branch": "branch",
#         "gender": "m",
#         "mob": mobile no.,
#           "name":"full name",
#         "profile_pic": "http://localhost:8000/media/profiles/default.png",
#         "user": 20198042,
#         "tags": [
#             "django"
#         ]
#     }
# ]
class api_detail_view(generics.RetrieveAPIView):
    APIView=['GET',]
    permission_classes = [IsAuthenticated]

    def get_object(self, regno):
        try:
            return User.objects.get(username = regno)
        except User.DoesNotExist:
            return None

    def get(self, request, regno, format=None):
        user = self.get_object(regno)
        if not user:
            return JsonResponse({"error":"no record found,please check regno again"})
        snippet = UserProfile.objects.get(user= user)
        serializer = UserProfileSerializer(snippet)
        return Response(serializer.data)

# api 
# call:[post only] http://localhost:8000/api/cookie/
# body of api call: [auth token required]
# return:{"success":"true"}
#         {"detail": "Invalid token."} if any problem with the token
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_cookie_token(request):
    user = request.user
    print(user)
    if user in User.objects.all():
        return JsonResponse({"success":"true","user":user.username})
    # if auth token is wrong django rest automatically 
    # return{"detail": "Invalid token."}


#api
#only to upload a single user
# call:[post] http://localhost:8000/api/new/    [auth token of admin user only]
#body of request:[json type data]
# {
#         "name": "name",
#         "regno": "regno",
#         "branch": "branch",
#         "gender": "m",
#         "email": "mailid",
#         "mob": "mobno"
#     }
#return:{"user":regno} if successful
#{"error":"only admin can create new user"} if token is not of admin user
# errors if any other problem occur
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_new_user(request):
    if not request.user.is_superuser:
        return JsonResponse({"error":"only admin can create new user"})
    
    data = JSONParser().parse(request)
    
    serializer = NewUserSerializer(data=data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        email = serializer.validated_data['email']
        regno = serializer.validated_data['regno']
        gender = serializer.validated_data['gender']
        branch = serializer.validated_data['branch']
        mob = serializer.validated_data['mob']
        name_arr = name.split(" ", 1)
        first = name_arr[0]
        last = name_arr[1] if len(name_arr) > 1 else ""
        user = User.objects.create_user(regno,email,regno,first_name = first,last_name = last)
       
        user.is_active = False
        user.save()

        UserProfile.objects.create(user = user,branch = branch,gender = gender,mob = mob)
        return JsonResponse({"user":regno},safe=False)
    return JsonResponse(serializer.errors)
        



