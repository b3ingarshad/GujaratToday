from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

class NavbarLink(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', default='category_images/default_image.jpg')
    color = models.CharField(max_length=20, default='#000000', blank=True)
    category_url = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class New(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = RichTextField(config_name='default')
    image = models.ImageField(upload_to='news_images/')
    is_trending = models.BooleanField(default=False)
    class Meta:
        ordering = ['-date'] 
    def __str__(self):
        return self.title

class TopNew(models.Model):
    news = models.ForeignKey(New, on_delete=models.CASCADE)

    def __str__(self):
        return self.news.title
    
class SiteLogo(models.Model):
    logo = models.ImageField(upload_to='logos/')  # Directory where logos will be uploaded
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "Site Logo"

class EpaperDaily(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-uploaded_at']
    def __str__(self):
        return self.title

class Lokhitmovement(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-uploaded_at']
    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    comment_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name

class Subscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email