from django.shortcuts import render, redirect
from accounts.constants import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def RatingReviewsList(request):
	ratings = RatingReviews.objects.all().order_by('-id')
	if request.GET.get('id'):
		ratings = ratings.filter(id = request.GET.get('id'))
	if request.GET.get('rating'):
		ratings = ratings.filter(rating__icontains = request.GET.get('rating'))
	if request.GET.get('review'):
		ratings = ratings.filter(review__icontains = request.GET.get('review'))
	if request.GET.get('name'):
		ratings = ratings.filter(name__icontains = request.GET.get('name'))
	if request.GET.get('created_on'):
		ratings = ratings.filter(created_on__date = request.GET.get('created_on'))
	page = request.GET.get('page', 1)
	paginator = Paginator(ratings, PAGE_SIZE)
	try:
		ratings = paginator.page(page)
	except PageNotAnInteger:
		ratings = paginator.page(1)
	except EmptyPage:
		ratings = paginator.page(paginator.num_pages)
	return render(request,'ratings/ratings-list.html',{"head_title":"Ratings And Reviews","ratings":ratings,"id":request.GET.get('id'),"rating":request.GET.get('rating'),"review":request.GET.get('review'),"name":request.GET.get('name'),"created_on":request.GET.get('created_on')})


@login_required
def DeleteReview(request,id):
    RatingReviews.objects.get(id=id).delete()
    messages.success(request,'Review Deleted Successfully!')
    return redirect('ratings:ratings_list')


@login_required
def ViewReview(request,id):
    rating = RatingReviews.objects.get(id=id)
    return render(request,'ratings/view-rating.html',{"head_title":"Ratings And Reviews","rating":rating})
