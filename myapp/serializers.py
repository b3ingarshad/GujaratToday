from rest_framework import serializers
from .models import NavbarLink, Category, New, TopNew

class NavbarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarLink
        fields = ['id', 'name', 'url']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

class NewsSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    class Meta:
        model = New
        fields = '__all__'

class TopNewSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='news.category.name')  # assuming Category model has a 'name' field
    title = serializers.CharField(source='news.title')
    author = serializers.CharField(source='news.author')
    date = serializers.DateField(source='news.date')
    image = serializers.ImageField(source='news.image')

    class Meta:
        model = TopNew
        fields = ['id', 'title', 'author', 'category', 'date', 'image']