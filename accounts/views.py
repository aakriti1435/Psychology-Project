import re
import environ
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from frontend.views import *
from .models import *
from django.db.models import Q
from django.db.models import  Count
from .backend import authenticate
env = environ.Env()
environ.Env.read_env()


class AdminLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('accounts:login')

      
class LogOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('accounts:login')


class LoginView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'frontend/login.html' , {'activated' : 'login', "title":"Login"})
    
    def post(self,request,*args,**kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")

        history = LoginHistory.objects.create(
            user_ip = request.META.get("REMOTE_ADDR"),
            user_agent = request.META['HTTP_USER_AGENT'],
            code = "http://" + request.META.get("REMOTE_ADDR") + request.path,
            user = request.POST.get("email")
        )
        if request.POST.get('remember_me')=='on':    
            request.session.set_expiry(7600) 
        user = authenticate(username=email, password=password)
        if not user:
            history.status = LOGIN_FAILURE
            history.save()
            messages.error(request, 'Invalid login credentials')
            return render(request, 'frontend/login.html',{"email":email})
        
        if user.is_superuser and user.role_id == ADMIN:
            login(request, user)
            messages.error(request, 'Login Successfully!')
            return redirect('admin:index')
        else:
            history.status = LOGIN_FAILURE
            history.save()
            messages.error(request, 'Invalid login credentials')
            return render(request, 'frontend/login.html',{"email":email})


@login_required
def EditUser(request,id):
    user=User.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('username'):
            user.username = request.POST.get('username')
        if request.POST.get('firstname'):
            user.first_name = request.POST.get('firstname')
        if request.POST.get('lastname'):
            user.last_name = request.POST.get('lastname')
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')
        user.save()
        if user.first_name:
            user.full_name = user.first_name + " " + user.last_name
        user.save()
        messages.success(request, 'Profile Updated successfully')
        return redirect('accounts:view_user', id=user.id)
    return render(request, 'users/edit-user.html',{"user":user})


@login_required
def Allusers(request):
    users=User.objects.all().order_by("-id").exclude(role_id=ADMIN).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(users, PAGE_SIZE)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'users/users.html', {"users":users,"head_title":"Users"} )


@login_required
def ViewUser(request,id):
    user=User.objects.get(id=id)
    return render(request, 'admin/profile.html', {'user':user, "head_title":"Profile"})


@login_required
def DeleteUser(request):
    user=User.objects.get(id = request.GET.get('id'))
    if user:
        user.state = DELETED
        user.is_active = False
        messages.success(request, 'User Deleted Successfully!')
    user.save()
    return redirect('accounts:allusers')


class PasswordChange(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        return render(request,'admin/change-password.html',{"head_title":"Change Password"})

    def post(self,request,*args,**kwargs):
        id=request.user.id
        user=User.objects.get(id=id)
        pass1 = request.POST.get("password")
        user.set_password(pass1)
        user.save()
        messages.add_message(request, messages.INFO, 'Password changed successfully')
        return redirect('accounts:login')


@login_required
def LoginHistoryView(request):
    loginhistory = LoginHistory.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(loginhistory, PAGE_SIZE)
    try:
        loginhistory = paginator.page(page)
    except PageNotAnInteger:
        loginhistory = paginator.page(1)
    except EmptyPage:
        loginhistory = paginator.page(paginator.num_pages)
    return render(request, 'admin/login-history.html', {"loginhistory":loginhistory, "head_title":"Login History"})


@login_required
def DeleteHistory(request):
    history=LoginHistory.objects.all()
    if history:
        history.delete()
        messages.success(request,"All Login History Cleared Sucessfully!!!")
    else:
        messages.error(request,"Nothing to Delete!!!")
    return redirect('accounts:login_history')


@login_required
def UserGraph(request):
    user = []
    d = datetime.now().month
    months = {'jan':'1','feb':'2','mar':'3','apr':'4','may':'5','jun':'6','jul':'7','aug':'8','sep':'9','oct':'10','nov':'11','dec':'12'}
    for i in months.keys():
        x = User.objects.filter(created_on__year=str(datetime.now().year),created_on__month= months[i],role_id=USER).annotate(count=Count('id')).count()
        user.append(x)

    chart = {
        'chart': {'type': 'column'}, 
        'title': {'text': f'Users in {datetime.now().year}'},
        'xAxis': { 'categories': [i.upper() for i in months.keys()]},
        'series': [
            {
                'name': 'Users',
                'data':user
            }]
            }
    return JsonResponse(chart)


def EmailValidation(request):
    if request.is_ajax():
        data ={"valid":None,"exists":None}
        email = request.GET.get("email")
        email = email.lstrip()
        email = email.rstrip()
        pat = r'^[a-zA-Z0-9_.+-]+[@]\w+[.]\w{2,3}$'
        match = str(re.search(pat,email))
        try:
            user_email = User.objects.filter(Q(state = ACTIVE)|Q(state = INACTIVE),email=email).last()
            if email == user_email.email:
                data['exists'] = '1'
        except:
            user_email = None           
        if user_email == None:
            data['exists'] = '0'    
        
        if match == "None":
            data['valid'] = '0'
        else:
            data['valid'] = '1'
        return JsonResponse(data)
