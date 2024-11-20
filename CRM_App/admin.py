from django.contrib import admin
from .models import *

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ['username', 'type','password']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['Name', 'EmailId', 'PhoneNumber', 'Role', 'Place', 'City', 'State', 'Country', 'Admin']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['LeadSource']

@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ['LeadPurpose']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['LeadStatus', 'color']



@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['CustomerName','Staff', 'CompanyName', 'EmailId', 'PhoneNumber', 'AlternativeNumber', 'address', 'Type', 'Note','created_at', 'Followup_title', 'Followup_date', 'Followup_time','Source','Purpose','Status']

@admin.register(AdminRegister)
class AdminRegisterAdmin(admin.ModelAdmin):
    list_display = ['Name', 'EmailId', 'PhoneNumber', 'Place', 'City', 'State', 'Country', 'Image']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['CompanyName', 'Location', 'Country', 'PhoneNumber', 'EmailId', 'Website', 'Admin']
@admin.register(Callstatus)
class CallstatusAdmin(admin.ModelAdmin):
    list_display = ('CallStatus',)

@admin.register(Callreasons)
class CallreasonsAdmin(admin.ModelAdmin):
    list_display = ('CallReasons',)

@admin.register(Meetingoutcome)
class MeetingoutcomeAdmin(admin.ModelAdmin):
    list_display = ('MeetingOutcome',)

@admin.register(Taskcategory)
class TaskcategoryAdmin(admin.ModelAdmin):
    list_display = ('TaskCategory',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('TaskName', 'Lead', 'AssignedBy', 'AssignedTo', 'CallStatus', 'TaskCategory', 'MeetingOutcome', 'CallReason', 'Comment', 'Date', 'Time', 'Description')




@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price']


from django.utils.safestring import mark_safe
from .models import PropertyCategory, Location, Developer, Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]

    list_display = ('title', 'download_brochure_link', 'status', 'category', 'property_type', 'price', 'bedrooms', 'bathrooms', 'area', 'location', 'developer', 'created_at')
    search_fields = ('title', 'status', 'price', 'bedrooms', 'bathrooms', 'area', 'created_at')

    def download_brochure_link(self, obj):
        if obj.brochure:
            return mark_safe(f'<a href="{obj.brochure.url}" download="{obj.brochure.name}">Download Brochure</a>')
        return "No Brochure"

    download_brochure_link.short_description = "Brochure"

admin.site.register(PropertyCategory)
admin.site.register(Location)
admin.site.register(Developer)  # Add Developer to the admin site
admin.site.register(Property, PropertyAdmin)


class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image_tag','images_link',)
    # search_fields =('property')
    readonly_fields = ('image_tag',)
    search_fields = ('property__title',)

    def images_link(self, obj):
        if obj.image:  # Assuming 'images' is the field name in your model
            return mark_safe(f'<a href="{obj.image.url}" download>Download Image</a>')
        return "No Image"
    images_link.short_description = "Images"
admin.site.register(PropertyImage,PropertyImageAdmin)
# admin.site.register(PropertyImage)



