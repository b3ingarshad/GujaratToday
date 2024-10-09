from rest_framework import serializers
from .models import NavbarLink, Category, New, TopNew

class NavbarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarLink
        fields = ['id', 'name', 'url']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'color','category_url']

class NewsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    category_url = serializers.CharField(source='category.category_url')
    category_color = serializers.CharField(source='category.color')
    class Meta:
        model = New
        fields = '__all__'

class TopNewSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='news.category.name')
    category_url = serializers.CharField(source='news.category.category_url')
    category_color = serializers.CharField(source='news.category.color')  
    title = serializers.CharField(source='news.title')
    author = serializers.CharField(source='news.author')
    date = serializers.DateField(source='news.date')
    image = serializers.ImageField(source='news.image')

    class Meta:
        model = TopNew
        fields = ['id', 'title', 'author', 'category','category_url', 'category_color', 'date', 'image']