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
    return render(request, 'page/page.html',{"pages":pages,"head_title":"Pages"})


@login_required
def SearchPages(request):
    if request.method == "GET":
        try:
            d = {
                'id':request.GET.get("id"),
                "title" :request.GET.get("title"),
                "content":request.GET.get("content"),
                "created_on":request.GET.get("created_on"),
                "type_id":request.GET.get("type_id"),
            }
            syn = "SELECT * FROM tbl_page WHERE "
            k =[]
            query = ""
            for i in d.keys():
                if i == 'id' or i == 'type_id':    
                    if d[i]:
                        k.append(d[i])
                        query += i + " = %s and " 
                elif i == 'created_on':    
                    if d[i]:
                        k.append(d[i]+"%")
                        query += "DATE("+i+")" + " = %s and " 
                else:
                    if d[i]:
                        k.append('%'+d[i]+"%")
                        query += i + " LIKE %s and "
            query = query.rstrip(" and ")
            syn += query
            searclist=[]
            for make in Pages.objects.raw(syn,k):
                searclist.append(make.id)
            pages = Pages.objects.filter(id__in = searclist).order_by('-id')
            if not pages:
                messages.add_message(request, messages.INFO, 'No Data Found')
            return render(request, "page/page.html", {"pages":pages,'id':request.GET.get("id"),
                "title" :request.GET.get("title"),
                "content":request.GET.get("content"),
                "created_on":request.GET.get("created_on"),
                "type_id":request.GET.get("type_id"),"head_title":"Pages"})
        except:
            messages.add_message(request, messages.INFO, 'Please Enter Something To Search')
            return redirect('page:page_list')


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
