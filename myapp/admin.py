from django.contrib import admin
from .models import NavbarLink, SiteLogo, Category, New, EpaperDaily, Lokhitmovement, TopNew, Feedback, Contact,Subscription
from django.core.exceptions import ValidationError
from django.contrib import messages

# Register your models here.
admin.site.register(NavbarLink)
admin.site.register(Category)
admin.site.register(New)
admin.site.register(SiteLogo)
# admin.site.register(Contact)
admin.site.register(Subscription)



@admin.register(EpaperDaily,Lokhitmovement)

class EpaperDailyAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

class LokhitmovementAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

class TopNewAdmin(admin.ModelAdmin):
    # Override get_form to filter news choices
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filter out news articles that are already selected as top news
        form.base_fields['news'].queryset = New.objects.exclude(id__in=TopNew.objects.values_list('news_id', flat=True))
        return form

    # Override save_model to enforce 10 top news limit
    def save_model(self, request, obj, form, change):
        if TopNew.objects.count() >= 10 and not change:
            # Show an error message and return without saving
            self.message_user(request, "You can only select up to 10 top news articles.", level=messages.ERROR)
        else:
            # Proceed with saving if the limit is not exceeded
            super().save_model(request, obj, form, change)

admin.site.register(TopNew, TopNewAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    # Specify the fields to display in the admin list view
    list_display = ('name', 'email', 'mobile_number','formatted_created_at')
    
    # Add filtering by creation date
    list_filter = ('created_at',)

    # Add a method to format the date and time
    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    formatted_created_at.short_description = 'Created At'  # Renames column in admin

# Register the Feedback model with custom admin options
admin.site.register(Feedback, FeedbackAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'email')

admin.site.register(Contact, ContactAdmin)