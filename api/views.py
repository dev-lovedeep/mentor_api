from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view,APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import send_mail_serializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from api.emails.tokens import account_activation_token
from django.utils.encoding import force_bytes,force_text
from django.shortcuts import HttpResponse
from .models import UserProfile
from .serializers import UserProfileSerializer,UserOnboardingSerializer
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


# api 
# call:http://localhost:8000/api/verify/<uid>/<token>/
# return:{"success":"true","student":student deatials} if email_verification_token is valid
#         {"success":"false"} if token is invalid 
def api_verify_token(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
            student= UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(student,many=False)
            return JsonResponse({"success":'true',"student":serializer.data})
    return JsonResponse({"success":'false'})


# api 
# call:[post only] http://localhost:8000/api/onboard/
# body of api call:[mob,password,password2,regno]
# return:{"success":"true","username":regno,"token":token}
#         {errors} if any problem with the form
@api_view(['POST'])
def api_onboarding(request):
    serializer = UserOnboardingSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = True
        user.save()
        token = Token.objects.get(user=user).key
        data['success'] = "true"
        data['username'] = user.username
        data['token'] = token
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

    return qs


# api 
# call:[get only] http://localhost:8000/api/filter/?query=love&branch=it&tag=django
# or blank call will return whole databse http://localhost:8000/api/filter/
# return:
# [
#     {
#         "id": 2,
#         "branch": "branch",
#         "gender": "m",
#         "mob": mobile no.,
#         "profile_pic": "http://localhost:8000/media/profiles/default.png",
#         "user": 5,
#         "tags": [
#             1
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
    #     response = super().list(request, args, kwargs)
    #     # Add data to response.data Example for your object:
    #     response.data['name'] =  # Or wherever you get this values from
    #     return response



