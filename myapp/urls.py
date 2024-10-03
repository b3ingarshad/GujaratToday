from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

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
    path('top-stories/', top_stories_page, name='top_stories_page'),
    path('e-papers/', epaper_view, name='epaper_view'),
    path('lokhit-movement/', lokhitmovement_view, name='lokhitmovement_view'),
    path('subscribe/', subscribe, name='subscribe'),
    path('search/', views.search_news, name='search_news'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)