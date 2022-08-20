from django.shortcuts import render ,redirect
from accounts.constants import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def ContactsList(request):
	contacts = ContactUs.objects.all().order_by('-id')
	page = request.GET.get('page', 1)
	paginator = Paginator(contacts, PAGE_SIZE)
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)
	return render(request,'contact/contact-list.html',{"head_title":"Contacts Management","contacts":contacts})


@login_required
def DeleteContact(request,id):
    contact = ContactUs.objects.get(id=id).delete()
    messages.success(request,"Contact Deleted Successfully!")
    return redirect('contact:contacts_list')


@login_required
def ViewContact(request,id):
    contact = ContactUs.objects.get(id=id)
    return render(request,'contact/view-contact.html',{"head_title":"Contacts Management","contact":contact})


def ContactFormView(request):
    if request.method == 'POST':
        ContactUs.objects.create(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            phone_number = request.POST.get('phone_number'),
            message = request.POST.get('message'),
        )
        messages.success(request, 'Thank You for contacting us. We will get back to you soon!')
        return redirect('contact:contact_form')
    return render(request,'frontend/contact-us.html')



