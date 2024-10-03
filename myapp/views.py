from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import *
from .serializers import *
import json
# Create your views here.

def index(request):
    logo = SiteLogo.objects.all()
    epaper = EpaperDaily.objects.all()
    categories = Category.objects.all()
    news_queryset = New.objects.all()  # Assuming you have a News model
    paginator = Paginator(news_queryset, 10)  # Show 10 news items per page
    page_number = request.GET.get('page', 1)  # Default to page 1
    news_list = paginator.get_page(page_number)

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        news_data = [
            {
                "id": news.id,
                "category": news.category.name,
                "date": news.date.strftime("%Y-%m-%d"),
                "title": news.title,
                "author": news.author,
                "description": news.description,
                "image": news.image.url,
                "is_trending": news.is_trending,
            }
            for news in news_list
        ]
        return JsonResponse({
            "news": news_data,
            "has_next": news_list.has_next(),
        })

    return render(request, 'index.html', {'logo': logo, 'news_list': news_list, 'categories': categories,'epaper': epaper})


def news_list(request):
    news_queryset = New.objects.all()  # Assuming you have a News model
    paginator = Paginator(news_queryset, 10)  # Show 10 news items per page
    page_number = request.GET.get('page')
    news_list = paginator.get_page(page_number)
    
    return render(request, 'index.html', {'news_list': news_list})

class NavbarAPIView(APIView):
    def get(self, request):
        links = NavbarLink.objects.all()
        serializer = NavbarLinkSerializer(links, many=True)
        return Response(serializer.data)

class CategoryAPIView(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

class NewsListCreateView(generics.ListCreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewsSerializer

class TrendingNewsAPIView(APIView):
    def get(self, request):
        trending_news = New.objects.filter(is_trending=True).order_by('-date')[:10]  # Limit to 10 latest trending news
        serializer = NewsSerializer(trending_news, many=True)
        return Response(serializer.data)

class TopNewsList(generics.ListCreateAPIView):
    queryset = TopNew.objects.all()
    serializer_class = TopNewSerializer

def news_view(request):
    news_list = New.objects.all()  # Fetch all news
    return render(request, 'index.html', {'news_list': news_list})

def news_detail_view(request, id):
    logo = SiteLogo.objects.all()
    categories = Category.objects.all()
    print(categories)
    news = get_object_or_404(New, id=id)
    return render(request, 'news-details.html', {'news': news, 'logo': logo, 'categories': categories})
    
def topnews_detail_view(request, id):
    logo = SiteLogo.objects.all()
    categories = Category.objects.all()
    topnews = get_object_or_404(TopNew, id=id)  # Fetch the top news item by ID

    # Use the `news` attribute from `TopNew` to get related news details
    return render(request, 'news-details.html', {
        'news': topnews.news,  # Related news object
        'logo': logo,
        'categories': categories
    })


def epaper_view(request):
    logo = SiteLogo.objects.all()
    epaper = EpaperDaily.objects.all()
    print("All paper", epaper)
    return render(request, 'e-papers.html', {'logo': logo, 'epaper': epaper})

def lokhitmovement_view(request):
    logo = SiteLogo.objects.all()
    lokhitmovement = Lokhitmovement.objects.all()
    print("All lokhitmovement", lokhitmovement)
    return render(request, 'lokhit-movement.html', {'logo': logo, 'lokhitmovement': lokhitmovement})

def feedback_view(request):
    if request.method == 'POST':
        # Print the POST data for debugging
        print("POST data:", request.POST)
        
        # Capture form data
        obj = Feedback()
        obj.name = request.POST.get('name')
        obj.email = request.POST.get('email')
        obj.mobile_number = request.POST.get('mobile_number')
        obj.comment_message = request.POST.get('comment_message')
        
        # Check if the data is being correctly fetched
        print("Name:", obj.name)
        print("Email:", obj.email)
        print("Mobile Number:", obj.mobile_number)
        print("Comment:", obj.comment_message)

        # Save to database
        obj.save()
        messages.success(request, 'Your Feedback is Submitted Successfully')
        return HttpResponse("Feedback submitted successfully")
    
    return render(request, 'news-details.html')

def contact(request):
    logo = SiteLogo.objects.all()
    if request.method == 'POST':
        # Print the POST data for debugging
        print("POST data:", request.POST)
        
        # Capture form data
        obj = Contact()
        obj.name = request.POST.get('contact-name')
        obj.email = request.POST.get('contact-email')
        obj.phone = request.POST.get('contact-phone')
        obj.message = request.POST.get('contact-message')
        
        # Check if the data is being correctly fetched
        print("Name:", obj.name)
        print("Email:", obj.email)
        print("Mobile Number:", obj.phone)
        print("Comment:", obj.message)

        # Save to database
        obj.save()
        messages.success(request, 'Your Feedback is Submitted Successfully')
        return HttpResponse("Feedback submitted successfully")
    return render(request, 'contact.html', {'logo': logo})

def subscribe(request):
    if request.method == 'POST':
        obj = Subscription()
        obj.email = request.POST.get('subscription-email')
        print("Subscription Name :", obj.email)

        obj.save()
        messages.success(request, 'Your Subscription is Submitted Successfully')
        return HttpResponse("Feedback submitted successfully")
    return render(request, 'index.html')


def trending_news_page(request):
    logo = SiteLogo.objects.all()
    epaper = EpaperDaily.objects.all()
    categories = Category.objects.all()
    news_queryset = New.objects.filter(is_trending=True)  # Only get trending news
    paginator = Paginator(news_queryset, 10)  # Show 10 news items per page
    page_number = request.GET.get('page', 1)
    news_list = paginator.get_page(page_number)

    # Serialize news_list to JSON
    news_list_json = json.dumps([
        {
            "id": news.id,
            "category": news.category.name,
            "date": news.date.strftime("%Y-%m-%d"),
            "title": news.title,
            "author": news.author,
            "description": news.description,
            "image": news.image.url,
            "is_trending": news.is_trending,
        }
        for news in news_list
    ])

    return render(request, 'trending-stories.html', {
        'logo': logo,
        'news_list_json': news_list_json,  # Pass serialized JSON to the template
        'categories': categories,
        'epaper': epaper
    })
    # return render(request, 'trending-stories.html')


def top_stories_page(request):
    logo = SiteLogo.objects.all()
    epaper = EpaperDaily.objects.all()
    categories = Category.objects.all()

    # Get the current date and calculate the date 7 days ago
    today = timezone.now()
    last_week = today - timezone.timedelta(days=7)

    # Filter news items from the last 7 days
    news_queryset = New.objects.filter(date__gte=last_week).order_by('-date')
    paginator = Paginator(news_queryset, 10)  # Show 10 news items per page
    page_number = request.GET.get('page', 1)
    news_list = paginator.get_page(page_number)

    # Serialize news_list to JSON
    news_list_json = json.dumps([
        {
            "id": news.id,
            "category": news.category.name,
            "date": news.date.strftime("%Y-%m-%d"),
            "title": news.title,
            "author": news.author,
            "description": news.description,
            "image": news.image.url if news.image else None,  # Ensure safe access to image
            "is_trending": news.is_trending,
        }
        for news in news_list
    ])

    return render(request, 'top-stories.html', {
        'logo': logo,
        'news_list_json': news_list_json,  # Pass serialized JSON to the template
        'categories': categories,
        'epaper': epaper
    })

from django.db.models import Q

def search_news(request):
    query = request.GET.get('q')
    news_queryset = New.objects.all()

    if query:
        # Search by title or description or any other field you want to include
        news_queryset = news_queryset.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Pagination if needed
    paginator = Paginator(news_queryset, 10)  # Show 10 news items per page
    page_number = request.GET.get('page', 1)
    news_list = paginator.get_page(page_number)

    return render(request, 'search.html', {'news_list': news_list, 'query': query})
