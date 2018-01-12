from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import User as _User
from .models import Affiliate
from accounts.models import SubmittedHistory
from django.views.decorators.http import require_POST
from .form import RegisterForm

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required(login_url="/accounts/login/")
def profile(request):
    topUsers = _User.objects.filter(is_superuser__exact=False).order_by("-score", "lastSubmitDatetime")
    idx = 1
    for user in topUsers:
        if user.username == request.user.username:
            break
        idx += 1
    maxSize = _User.objects.filter(is_superuser__exact=False).count()
    fromIdx = 0 if idx-3 < 0 else idx-3
    toIdx   =  maxSize if idx+3 > maxSize else idx+3
    aroundUsers = topUsers[fromIdx:toIdx]
    history = SubmittedHistory.objects.filter(user__exact=request.user).order_by("-submitDatetime")[:5]
    return render(request,"accounts/profile.html", 
                  {'user' : request.user,
                   'baseIdx': fromIdx, 
                   'idx': idx,
                   'aroundUsers': aroundUsers,
                   'history': history
               }
              )

@login_required(login_url="/accounts/login/")
def update(request):
    #newUserID = request.POST['userID']
    newUsername = request.POST['userName']
    #newAffiliate = request.POST['affiliate']
    newEmail = request.POST['email']
    newPW = request.POST['newPW']
    confirmPW = request.POST['confirmPW']
    currentPW = request.POST['currentPW']
    #return render(request, 'accounts/error.html')

    changePWFlag = True
    if newPW == "" or (newPW != confirmPW):
        changePWFlag = False
    if request.user.check_password(currentPW) and changePWFlag:
        request.user.username = newUsername
        if newPW != "":
            request.user.set_password(newPW)
        request.user.save()
        return HttpResponseRedirect(reverse('accounts:index'))
    else:
        return render(request,"accounts/profile.html", 
                      {'user' : request.user, 
                       "errorStr": "Update Failed. Please try again.",
                   }
                  )

def register(request):
    registerForm = RegisterForm(request.POST or None)
    return render(request, 'accounts/register.html', {'form': registerForm, "affiliates": Affiliate.objects.all()})

@require_POST
def register_redirect(request):
    registerForm = RegisterForm(request.POST)

    if request.POST['password'] != request.POST['confirm'] or len(_User.objects.filter(username__exact=request.POST['username'])) != 0:
        return HttpResponseRedirect(reverse('accounts:register'))        

    username = request.POST['username']
    password = request.POST['password']
    affiliate = Affiliate.objects.filter(name__exact=request.POST['affiliate'])
    if len(affiliate) == 0:
        return HttpResponseRedirect(reverse('accounts:register'))        
    user = User.objects.create_user(username, '', password)
    user.affiliate = affiliate[0]
    user.save()
    return HttpResponseRedirect(reverse('accounts:login'))
