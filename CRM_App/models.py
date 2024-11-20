from django.db import models
from datetime import date, time
from .utils import generate_barrier_token

# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    type=models.CharField(max_length=50)


    def __str__(self):
        return self.username

class Source(models.Model):
    LeadSource=models.CharField(max_length=100)

    def __str__(self):
        return self.LeadSource
class Purpose(models.Model):
    LeadPurpose=models.CharField(max_length=100)

    def __str__(self):
        return self.LeadPurpose

class Status(models.Model):
    LeadStatus=models.CharField(max_length=100)
    color=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.LeadStatus




class AdminRegister(models.Model):
    Lid=models.ForeignKey(Login,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    Image=models.ImageField(upload_to="images/",null=True)
    EmailId=models.CharField(max_length=50)
    PhoneNumber=models.CharField(max_length=50)
    PabblyApiToken = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    Place=models.CharField(max_length=100,null=True)
    City=models.CharField(max_length=100,null=True)
    State=models.CharField(max_length=100,null=True)
    Country=models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    BarrierToken = models.CharField(max_length=64, blank=True)
    # otp=models.CharField(max_length=6,null=True)
    def save(self, *args, **kwargs):
        # Generate barrier token if it doesn't exist yet
        if not self.BarrierToken:
            self.BarrierToken = generate_barrier_token(self.EmailId, self.PhoneNumber, self.created_at)  # Assuming 'created_at' field exists
        super().save(*args, **kwargs)



    def __str__(self):
        return self.Name
class Company(models.Model):
    CompanyName=models.CharField(max_length=100)
    Location=models.CharField(max_length=100)
    Country=models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=12)
    EmailId = models.EmailField(max_length=200, blank=True)
    Website = models.CharField(max_length=200, blank=True)
    Admin=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)

    def __str__(self):
        return self.CompanyName
class Staff(models.Model):
    admin=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)
    Lid=models.ForeignKey(Login,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    Image=models.ImageField(upload_to="images/",null=True)
    EmailId=models.CharField(max_length=50)
    PhoneNumber=models.CharField(max_length=50)
    Role=models.CharField(max_length=100)
    Place=models.CharField(max_length=100,null=True)
    City=models.CharField(max_length=100,null=True)
    State=models.CharField(max_length=100, null=True)
    Country=models.CharField(max_length=100, null=True)
    Co_Admin=(
        ('YES','yes'),
        ('NO','no'),
    )
    Admin=models.CharField(max_length=20,choices=Co_Admin,default='NO')

    def __str__(self):
        return self.Name


class Lead(models.Model):
    admin=models.ForeignKey(AdminRegister,on_delete=models.CASCADE)
    CustomerName=models.CharField(max_length=100)
    CompanyName=models.CharField(max_length=100,null=True)
    EmailId=models.CharField(max_length=50)
    PhoneNumber=models.CharField(max_length=50)
    AlternativeNumber=models.CharField(max_length=50,null=True)
    address=models.CharField(max_length=400)
    Source=models.ForeignKey(Source,on_delete=models.CASCADE)
    Purpose=models.ForeignKey(Purpose,on_delete=models.CASCADE)
    Type=models.CharField(max_length=100)
    Status=models.ForeignKey(Status,on_delete=models.CASCADE)
    Staff=models.ForeignKey(Staff,on_delete=models.CASCADE)
    Note=models.TextField(null=True)
    Followup_title = models.CharField(max_length=100)
    Followup_date = models.DateField()
    Followup_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.CustomerName
class Callstatus(models.Model):
    CallStatus=models.CharField(max_length=100)

    def __str__(self):
        return self.CallStatus

class Callreasons(models.Model):
    CallReasons=models.CharField(max_length=100)

    def __str__(self):
        return self.CallReasons

class Meetingoutcome(models.Model):
    MeetingOutcome=models.CharField(max_length=100)

    def _str_(self):
        return self.MeetingOutcome

class Taskcategory(models.Model):
    TaskCategory=models.CharField(max_length=100)

    def __str__(self):
        return self.TaskCategory

class Task(models.Model):
    TaskName = models.CharField(max_length=100)
    Lead = models.ForeignKey('Lead', on_delete=models.CASCADE)
    AssignedBy = models.ForeignKey('AdminRegister', on_delete=models.CASCADE,null=True)
    AssignedTo = models.ForeignKey('Staff', on_delete=models.CASCADE)
    CallStatus = models.ForeignKey('Callstatus', on_delete=models.CASCADE,null=True)
    TaskCategory = models.ForeignKey('Taskcategory', on_delete=models.CASCADE)
    MeetingOutcome = models.ForeignKey('Meetingoutcome', on_delete=models.CASCADE,null=True)
    CallReason = models.ForeignKey('Callreasons', on_delete=models.CASCADE,null=True)
    Comment = models.TextField(null=True)
    Date = models.DateField()
    Time = models.TimeField()
    Description = models.TextField(null=True)
    Status=models.CharField(max_length=50,null=True)





# models.py
from django.db import models

class Properties(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class PropertyCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.CharField(max_length=100)
    # latitude = models.FloatField()
    # longitude = models.FloatField()

    def __str__(self):
        return self.city

class Developer(models.Model):
    name = models.CharField(max_length=100)
    # website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    STATUS_CHOICES = (
        ('FOR SALE', 'For Sale'),
        ('OFF PLAN', 'Off Plan'),
    )

    PROPERTY_TYPE_CHOICES = (
        ('RENTAL', 'Rental'),
        ('SALE', 'Sale'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FOR SALE')
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='SALE')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.CharField(max_length=20)
    bedrooms = models.CharField(max_length=20)
    bathrooms = models.CharField(max_length=20)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # New field for property brochure PDF
    brochure = models.FileField(upload_to='media/property_brochures/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("singlepage", kwargs={'pk': self.pk})

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='media/property_images/')

    def __str__(self):
        return f"Image for {self.property.property_type} - {self.property.title}"

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="100px" height="100px" />' % (self.image.url))
        else:
            return "No Image"

    image_tag.short_description = 'Image'
