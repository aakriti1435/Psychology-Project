from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.shortcuts import redirect, render


@login_required
def ChangeState(request,id):
    page = Pages.objects.get(id=id)
    if page.is_active:
        page.is_active = False
        page.save()
        messages.error(request, 'Page Deactivated Successfully')
        return redirect('page:view_page',page.id)
    else:
        page.is_active = True
        page.save()
        messages.error(request, 'Page Activated Successfully')
        return redirect('page:view_page',page.id)


@login_required
def PagesView(request):
    pages = Pages.objects.all().order_by('-updated_on')
    if request.GET.get('id'):
        pages = pages.filter(id=request.GET.get('id'))
    if request.GET.get('title'):
        pages = pages.filter(title__icontains=request.GET.get('title'))
    if request.GET.get('content'):
        pages = pages.filter(content__icontains=request.GET.get('content'))
    if request.GET.get('created_on'):
        pages = pages.filter(created_on__date=request.GET.get('created_on'))
    if request.GET.get('type_id'):
        pages = pages.filter(type_id=request.GET.get('type_id'))
    return render(request, 'page/page.html',{"pages":pages,"head_title":"Pages","id":request.GET.get('id'),"title":request.GET.get('title'),"content":request.GET.get('content'),"created_on":request.GET.get('created_on'),"type_id":request.GET.get('type_id')})


@login_required
def AddPage(request):
    if request.method == 'POST':
        if Pages.objects.filter(type_id = request.POST.get("type")):
            messages.error(request, 'Page Already Exists')
            return render(request, 'page/add-page.html',{"title":request.POST.get("title"),"content":request.POST.get("content")})
        page = Pages.objects.create(
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            type_id=request.POST.get("type"),
            is_active=True
        )
        page.save()
        messages.error(request, 'Page Add Successfully')
        return redirect('page:page_list')
    return render(request, 'page/add-page.html',{"head_title":"Pages"})


@login_required
def DeletePage(request):
    page = Pages.objects.get(id=request.GET.get("id"))
    if page:
        page.delete()
        return redirect('page:page_list')


@login_required
def ViewPage(request,id):
    page = Pages.objects.get(id=id)
    return render(request, 'page/view-page.html',{"page":page,"head_title":"Pages"})


@login_required
def PageEdit(request,id):
    page =  Pages.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get("title",None):
            page.title = request.POST.get("title")
        if request.POST.get("content"):
            page.content = request.POST.get("content")
        else:
            page.content = ""
        page.save()
        messages.error(request, 'Page Update Successfully.')
        return render(request, "page/view-page.html",{"page":page,"head_title":"Pages"})
    return render(request, "page/edit-page.html",{"page":page,"head_title":"Pages"})
