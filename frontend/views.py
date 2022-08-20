from django.shortcuts import render,redirect
from accounts.constants import *
from page.models import *
import logging
db_logger = logging.getLogger('db')


## Index Page
def index(request):
    if request.user.is_authenticated == True and request.user.is_superuser and request.user.role_id == ADMIN:
        return redirect('admin:index')
    else:
        return render(request, "frontend/index.html")


## About Us Page 
def TermsAndConditions(request):
    try:
        content = Pages.objects.get(type_id=TERMS_AND_CONDITION)
    except:
        content = None
    return render(request, "frontend/staticpage.html",{"content":content, "title":"TERMS & CONDITIONS"})


## About Us Page 
def AboutUs(request):
    try:
        content = Pages.objects.get(type_id=ABOUT_US)
    except:
        content = None
    return render(request, "frontend/staticpage.html",{"content":content, "title":"ABOUT US"})


## Privacy Page 
def PrivacyPolicy(request):
    try:
        content = Pages.objects.get(type_id=PRIVACY_POLITY)
    except:
        content = None
    return render(request, "frontend/staticpage.html",{"content":content, "title":"PRIVACY POLICY"})


def handler404(request, exception, template_name="frontend/404.html"):
    db_logger.exception(Exception)
    return render(request, template_name, status=404)
    

def handler500(request, *args, **argv):
    db_logger.exception(Exception)
    return render(request, 'frontend/404.html', status=500)
    

def handler403(request, exception, template_name="frontend/404.html"):
    db_logger.exception(exception)
    return render(request, template_name, status=403)
    

def handler400(request, exception, template_name="frontend/404.html"):
    db_logger.exception(exception)
    return render(request, template_name, status=400)
    