from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.index, name="index"),
    path('api/navbar/', NavbarAPIView.as_view(), name='navbar-api'),
    path('api/category/', CategoryAPIView.as_view(), name='category-api'),
    path('api/news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('api/topnews/', TopNewsList.as_view(), name='top-news-list'),
    path('news/<int:id>/', views.news_detail_view, name='news_detail'),
    path('topnews/<int:id>/', topnews_detail_view, name='topnews-detail-view'),
    path('submit-feedback/', feedback_view, name='feedback'),
    path("contact/", views.contact, name="contact"),
    path('trending-news/', trending_news_page, name='trending_news_page'),
    path('top-stories/', lambda request: dynamic_page_view(request, 'top-stories.html')),
    path('epaper-daily/', epaper_view, name='epaper_view'),
    path('lokhit-movement/', lokhitmovement_view, name='lokhitmovement_view'),
    path('subscribe/', subscribe, name='subscribe'),
    path('search/', views.search_news, name='search_news'),
    path('about-us/', views.about, name='about'),
    path('hate-crime/', lambda request: dynamic_page_view(request, 'hate-crime.html')),
    path('injustice/', lambda request: dynamic_page_view(request, 'injustice.html')),
    path('religion/', lambda request: dynamic_page_view(request, 'religion.html')),
    path('downtrodden/', lambda request: dynamic_page_view(request, 'downtrodden.html')),
    path('sports/', lambda request: dynamic_page_view(request, 'sports.html')),
    path('politics/', lambda request: dynamic_page_view(request, 'politics.html')),
    path('education/', lambda request: dynamic_page_view(request, 'education.html')),
    path('enviroment/', lambda request: dynamic_page_view(request, 'enviroment.html')),
    path('economy/', lambda request: dynamic_page_view(request, 'economy.html')),
    path('national/', lambda request: dynamic_page_view(request, 'national.html')),
    path('international/', lambda request: dynamic_page_view(request, 'international.html')),
    path('motivation/', lambda request: dynamic_page_view(request, 'motivation.html')),
    path('muslim-freedom-fighters/', lambda request: dynamic_page_view(request, 'muslim-freedom-fighters.html')),
    path('harmony/', lambda request: dynamic_page_view(request, 'harmony.html')),
    path('hatred/', lambda request: dynamic_page_view(request, 'hatred.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# urlpatterns += [
#     # Catch-all path for 404 page
#     path('<path:resource>', views.custom_404_view, name='404'),
# ]