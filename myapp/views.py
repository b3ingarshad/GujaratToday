from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q
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
                "category_url": news.category.category_url,
                "category_color": news.category.color,
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
    related_news = New.objects.filter(category=news.category).exclude(id=news.id)[:4]  # Limiting to 4 related posts
    return render(request, 'news-details.html', {'news': news, 'logo': logo, 'categories': categories,'related_news':related_news})
    
def topnews_detail_view(request, id):
    logo = SiteLogo.objects.all()  # Fetch the first logo (assuming only one logo)
    categories = Category.objects.all()
    topnews = get_object_or_404(TopNew, id=id)  # Fetch the top news item by ID
    
    # Fetch related news based on the category of the news object in TopNew
    related_news = New.objects.filter(category=topnews.news.category).exclude(id=topnews.news.id)[:4]
    
    return render(request, 'news-details.html', {
        'news': topnews.news,  # Pass the related `New` object
        'logo': logo,
        'categories': categories,
        'related_news': related_news  # Related news articles
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
            "category_color": news.category.color,
            "category_url": news.category.category_url,
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


# def top_stories_page(request):
#     logo = SiteLogo.objects.all()
#     epaper = EpaperDaily.objects.all()
#     categories = Category.objects.all()

#     # Get the current date and calculate the date 7 days ago
#     today = timezone.now()
#     last_week = today - timezone.timedelta(days=7)

#     # Filter news items from the last 7 days
#     news_queryset = New.objects.filter(date__gte=last_week).order_by('-date')
#     paginator = Paginator(news_queryset, 10)  # Show 10 news items per page
#     page_number = request.GET.get('page', 1)
#     news_list = paginator.get_page(page_number)

#     # Serialize news_list to JSON
#     news_list_json = json.dumps([
#         {
#             "id": news.id,
#             "category": news.category.name,
#             "date": news.date.strftime("%Y-%m-%d"),
#             "title": news.title,
#             "author": news.author,
#             "description": news.description,
#             "image": news.image.url if news.image else None,  # Ensure safe access to image
#             "is_trending": news.is_trending,
#         }
#         for news in news_list
#     ])

#     return render(request, 'top-stories.html', {
#         'logo': logo,
#         'news_list_json': news_list_json,  # Pass serialized JSON to the template
#         'categories': categories,
#         'epaper': epaper
#     })

def search_news(request):
    logo = SiteLogo.objects.all()
    query = request.GET.get('q')

    # Get all news objects
    news_queryset = New.objects.all()
    
    if query:
        # Search in the New model (title, description, author, etc.)
        news_queryset = news_queryset.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(author__icontains=query) |  # Example: filtering by author
            Q(category__name__icontains=query)  # Example: filtering by category if it is a ForeignKey
            # Add more fields as needed
        )

    news_list = [
        {
            "id": news.pk,
            "category": news.category.name if news.category else "Uncategorized",
            "category_color": news.category.color,  # Handle category safely
            "date": news.date.strftime("%Y-%m-%d"),
            "title": news.title,
            "author": news.author,
            "description": news.description,
            "image": news.image.url if news.image else None,  # Ensure safe access to image
            "is_trending": news.is_trending,
        }
        for news in news_queryset
    ]

   
    # Serialize to JSON
    news_list_json = json.dumps(news_list)
    no_results = len(news_list) == 0

    # Pass the serialized JSON data to the template
    return render(request, 'search.html', {
        'news_json': news_list_json,  # Serialized news queryset
        'query': query,
        'no_results': no_results,
        'logo': logo
    })

def about(request):
    logo = SiteLogo.objects.all()
    categories = Category.objects.all()
    return render(request, 'about-us.html', {'logo': logo,'categories': categories})

def dynamic_page_view(request, template_name):
    logo = SiteLogo.objects.all()
    categories = Category.objects.all()

    # Fetch all news items ordered by date
    news_queryset = New.objects.all().order_by('-date')

    # Serialize news_queryset to JSON (without pagination)
    news_list_json = json.dumps([
        {
            "id": news.id,
            "category": news.category.name,
            "category_url": news.category.category_url,
            "category_color": news.category.color,
            "date": news.date.strftime("%Y-%m-%d"),
            "title": news.title,
            "author": news.author,
            "description": news.description,
            "image": news.image.url if news.image else None,  # Ensure safe access to image
            "is_trending": news.is_trending,
        }
        for news in news_queryset
    ])

    return render(request, template_name, {
        'logo': logo,
        'news_list_json': news_list_json,  # Pass serialized JSON to the template
        'categories': categories,
    })

# def custom_404_view(request, resource):
#     logo = SiteLogo.objects.all()
#     news_queryset = New.objects.all()
#     # You can add custom logic here if needed
#     return render(request, 'error-404.html',{'logo': logo,'news_queryset':news_queryset, 'resource': resource}, status=404)