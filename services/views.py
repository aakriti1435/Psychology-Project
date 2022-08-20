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
