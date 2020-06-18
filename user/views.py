from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from .forms import user_onboarding_form
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from .emails.tokens import account_activation_token
from .models import UserProfile,Tags
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value
# Create your views here.


# def home_view(request):
#     return render(request,'mentor/templates/home.html',{})

def signup_view(request):
    if request.method == "POST":
        regno = request.POST['regno']
        
        try:
            user = User.objects.get(username = regno)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if not user:
            return HttpResponse("invalid regno")
        if user.is_active:
            return HttpResponse("a user with this regno already exist")
        #mailing process start here
        current_site = get_current_site(request)
        subject = 'Activate Your MNNIT Mentor Account'
        message = render_to_string('user/emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            #todo:look whehter .decocde() is requiered at end or not
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        messages.success(request, ('a confirmation link has been sent to your registered mail id.'))
        return HttpResponse("a confirmation link has been sent to your registered mail id.")

        # else:
        #     return HttpResponse("signup failed")


    return render(request,'user/templates/signup.html',{})


def onboarding(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        current_user_profile = get_object_or_404(UserProfile,user = user)
        if request.method == "POST":
            submitted_data = user_onboarding_form(request.POST,instance=current_user_profile)
            if submitted_data.is_valid():
                password1 = request.POST['password1'] 
                password2 = request.POST['password2']
                # submitted_data.save()
                if 'profile_pic' in request.FILES:
                    current_user_profile.profile_pic = request.FILES['profile_pic']
                if password1 == password2:
                    user.set_password(password1)
                    user.is_active = True
                    user.save()
                    submitted_data.save()
                    return redirect('user:login')
                else:
                    return HttpResponse("confirm password not matched")
            else:
                return HttpResponse(submitted_data.errors)
        return render(request,'user/templates/onboarding.html',{"form":user_onboarding_form(instance=current_user_profile)})
    else:
        messages.error(request, ("invalid link please request another link"))
        return redirect('user:signup')
    # return redirect('user:signup')


def login_view(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password=password)
        
        if user:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("login failed")
    return render(request,'user/templates/login.html',{})


def is_valid_queryparam(param):
    return param != '' and param is not None



#    this function contain the filtring logic
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

@login_required
def home_view(request):
    # this will return the filtered qs
    qs = filter(request)
    context = {
        'queryset': qs,
        'categories': Tags.objects.all()
    }
    return render(request, "user/templates/home.html", context)
