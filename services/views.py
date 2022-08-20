from django.shortcuts import render, redirect
from accounts.constants import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def ServicesList(request):
	services = Services.objects.all().order_by('-id')
	page = request.GET.get('page', 1)
	paginator = Paginator(services, PAGE_SIZE)
	try:
		services = paginator.page(page)
	except PageNotAnInteger:
		services = paginator.page(1)
	except EmptyPage:
		services = paginator.page(paginator.num_pages)
	return render(request,'services/service-list.html',{"head_title":"Services Management","services":services})


@login_required
def AddService(request):
    if request.method == 'POST':
        if Services.objects.filter(title=request.POST.get('title')):
            messages.error(request, "Service Title Already Exist!")
            return render(request, 'services/add-service.html',{"head_title":"Services Management"})
        else:
            service = Services.objects.create(
                title = request.POST.get('title'),
                description = request.POST.get('description'),
                image = request.FILES.get('image'),
                price = request.POST.get('price'),
                created_by = request.user,
            )
            messages.success(request,'Service Added Successfully!')
            return redirect('services:view_service',id=service.id)
    return render(request, 'services/add-service.html',{"head_title":"Services Management"})


@login_required
def DeleteService(request,id):
    service = Services.objects.get(id=id).delete()
    messages.success(request,'Service Deleted Successfully!')
    return redirect('services:services_list')


@login_required
def ViewService(request,id):
    service = Services.objects.get(id=id)
    return render(request, 'services/view-service.html',{"head_title":"Services Management","service":service})


@login_required
def EditService(request, id):
    service = Services.objects.get(id=id)
    if request.method == 'POST':
        service_exist = Services.objects.filter(title=request.POST.get('title')).exclude(id=id)
        if service_exist:
            messages.error(request, "Service Title Already Exist!")
            return render(request, 'services/edit-service.html',{"head_title":"Services Management","service":service})
        else:
            service.title = request.POST.get('title')
            service.description = request.POST.get('description')
            if request.FILES.get('image'):
                service.image = request.FILES.get('image')
            service.price = request.POST.get('price')
            service.save()
            messages.success(request,'Service Updated Successfully!')
            return redirect('services:view_service',id=service.id)
    return render(request, 'services/edit-service.html',{"head_title":"Services Management","service":service})






