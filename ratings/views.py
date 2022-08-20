from django.shortcuts import render, redirect
from accounts.constants import *
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def RatingReviewsList(request):
	ratings = RatingReviews.objects.all().order_by('-id')
	page = request.GET.get('page', 1)
	paginator = Paginator(ratings, PAGE_SIZE)
	try:
		ratings = paginator.page(page)
	except PageNotAnInteger:
		ratings = paginator.page(1)
	except EmptyPage:
		ratings = paginator.page(paginator.num_pages)
	return render(request,'ratings/ratings-list.html',{"head_title":"Ratings And Reviews","ratings":ratings})


@login_required
def DeleteReview(request,id):
    RatingReviews.objects.get(id=id).delete()
    messages.success(request,'Review Deleted Successfully!')
    return redirect('ratings:ratings_list')


@login_required
def ViewReview(request,id):
    rating = RatingReviews.objects.get(id=id)
    return render(request,'ratings/view-rating.html',{"head_title":"Ratings And Reviews","rating":rating})
