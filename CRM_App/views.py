from django.shortcuts import render, redirect
from .models import *
from django.http.response import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from random import randint
from django.db.models import Q, Count
from datetime import datetime
import datetime
from PIL import ImageColor
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

# Create your views here.

def base(request):
    return render(request,'base.html')
def home(request):
    return render(request,'main/home.html')
def loginForm(request):
    return render(request,'main/login.html')
def otpForm(request):
    return render(request,'main/otp.html')
def about(request):
    return render(request,'main/about.html')
def leadpurpose(request):
    purposes = Purpose.objects.all()
    context={
        "purposes":purposes,
    }
    return render(request,'main/leadpurpose.html',context)
def leadsource(request):
    return render(request,'main/leadsource.html')
def leadstatus(request):
    return render(request,'main/leadstatus.html')
def staffDashboard(request):
    login_id = request.session.get('slid')
    leads = Lead.objects.filter(Staff__Lid_id=login_id)
    purposes = Purpose.objects.all()
    purpose_counts = leads.values('Purpose__LeadPurpose').annotate(count=Count('Purpose'))
    purpose_data = [['Purpose', 'Count']]
    for purpose in purposes:
        purpose_name = purpose.LeadPurpose
        count = next((item['count'] for item in purpose_counts if item['Purpose__LeadPurpose'] == purpose_name), 0)
        purpose_data.append([purpose_name, count])

    sources = Source.objects.all()
    source_counts = leads.values('Source__LeadSource').annotate(count=Count('Source'))
    source_data = [['Source', 'Count']]
    for source in sources:
        source_name = source.LeadSource
        count = next((item['count'] for item in source_counts if item['Source__LeadSource'] == source_name), 0)
        source_data.append([source_name, count])
    today = leads.filter(created_at__date=datetime.date.today()).count()
    week = leads.filter(created_at__date__gte=datetime.date.today() - datetime.timedelta(days=7)).count()
    month = leads.filter(created_at__date__gte=datetime.date.today() - datetime.timedelta(days=30)).count()
    total = leads.all().count()
    statuses = Status.objects.annotate(count=Count('lead', filter=Q(lead__in=leads)))
    lead_counts_query = leads.filter(created_at__date__gte=datetime.date.today() - datetime.timedelta(days=15)).values('created_at__date').annotate(count=Count('id'))
    lead_counts = [item['count'] for item in lead_counts_query]

    context = {
        'lead_counts': lead_counts,
        'today': today,
        'weekly': week,
        'monthly': month,
        'total': total,
        'statuses': statuses,
        'purpose_data': purpose_data,
        'source_data': source_data,
    }

    return render(request,'main/staffdashboard.html',context)
def staffeditlead(request,id):
    source=Source.objects.all()
    purpose=Purpose.objects.all()
    status=Status.objects.all()
    staff=Staff.objects.all()
    lead = Lead.objects.get(id=id)
    request.session['Leadid']=lead.id
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context = {
        'source':source,
        'purpose':purpose,
        'status':status,
        'staff':staff,
        'lead':lead,
        'admin':[admin],
    }

    return render(request,'main/staffeditlead.html',context)

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import AdminRegister,Source,Status
from django.shortcuts import get_object_or_404
from datetime import datetime, time
from .models import Lead, Purpose
from pytz import timezone
from django.contrib.auth.decorators import login_required
import json
from dateutil import parser


@csrf_exempt
def pabbly_lead_webhook(request):
    if request.method == 'POST':
        try:
            # Load the incoming JSON data
            data = json.loads(request.body)
            # Extract the necessary lead information
            customer_name = data.get('Res2 Full Name', '')
            company_name = data.get('Res2 Company Name', '')
            email_id = data.get('Res2 Email', '')
            phone_number = data.get('Res2 Phone Number', '')
            source = data.get('Res2 Platform', '')
            source_instance, _ = Source.objects.get_or_create(LeadSource=source)
            lead_type = data.get('Res1 Ad Name', '')
            address = data.get('Res2 Address', '')
            created_time = data.get('Res1 Created Time', '')
             # Handle created time parsing and conversion to IST
            if created_time:
                utc_created_time = parser.parse(created_time)
                ist_created_time = utc_created_time.astimezone(timezone('Asia/Kolkata'))
            else:
                ist_created_time = None

            # Create a new Lead record and assign it to the admin

            # Get the staff member and status
            staff_to_assign = Staff.objects.first()  # Assign the first staff member
            status = Status.objects.first()  # Assign the first status
            purpose = Purpose.objects.first()

            admin_instance = AdminRegister.objects.first()





            # Create a new Lead record and assign it to the admin
            new_lead = Lead(
                admin=admin_instance,
                CustomerName=customer_name,
                CompanyName=company_name,
                EmailId=email_id,
                PhoneNumber=phone_number,
                Source=source_instance,
                Type=lead_type,
                created_at=ist_created_time,
                address=address,
                Purpose=purpose,
                Staff=staff_to_assign,
                Status=status,
                Followup_date=datetime.now().date(),
                Followup_time=time(12, 0),
            )
            new_lead.save()

            # Send an email notification to multiple recipients
            subject = 'New Lead Received'
            message = f'A new lead has been received.\n\nCustomer Name: {customer_name}\nEmail: {email_id}\nPhone Number: {phone_number}\nCompany Name: {company_name}\nAddress: {address}\nSource: {source}\nType: {lead_type}'
            from_email = 'quickfixsorter123@gmail.com'
            to_emails = ['althaf162017@gmail.com', 'delemonjobs@gmail.com', ]  # Add multiple email addresses here
            send_mail(subject, message, from_email, to_emails)

            return JsonResponse({"status": "success"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


# views.py
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from .models import Lead, AdminRegister, Source, Purpose, Status, Staff
# import json
# from datetime import datetime

# @csrf_exempt
# def pabbly_lead_webhook(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

            # admin_name = data.get('admin_name')
            # if admin_name:
            #     # Assuming "althaf" is the name of the admin
            #     if admin_name == "althaf":
            #         admin_instance = AdminRegister.objects.get(Name="althaf")
            #     else:
            #         return JsonResponse({'status': 'error', 'message': f'Admin "{admin_name}" not found'}, status=400)
            # else:
            #     return JsonResponse({'status': 'error', 'message': 'Admin name not provided'}, status=400)

#             required_keys = [
#                 'source_id', 'purpose_id', 'status_id', 'staff_id',
#                 'Res2 Full Name', 'Res2 Email', 'Res2 Phone Number', 'Res2 Address',
#                 'Type', 'Followup_title', 'Followup_date', 'Followup_time'
#             ]

#             missing_keys = [key for key in required_keys if key not in data]
#             if missing_keys:
#                 return JsonResponse({'status': 'error', 'message': f'Missing keys: {", ".join(missing_keys)}'}, status=400)

#             # Fetch related objects from the database
#             source = Source.objects.get(id=data['source_id'])
#             purpose = Purpose.objects.get(id=data['purpose_id'])
#             status = Status.objects.get(id=data['status_id'])
#             staff = Staff.objects.get(id=data['staff_id'])

#             # Create and save the Lead instance
#             lead = Lead(
#                 admin=admin_instance,
#                 CustomerName=data['Res2 Full Name'],
#                 CompanyName=data.get('Res2 Company Name'),
#                 EmailId=data['Res2 Email'],
#                 PhoneNumber=data['Res2 Phone Number'],
#                 AlternativeNumber=data.get('Res1 Ad Name'),
#                 address=data['Res2 Address'],
#                 Source=source,
#                 Purpose=purpose,
#                 Type=data['Type'],
#                 Status=status,
#                 Staff=staff,
#                 Note=data.get('Res2 Platform'),
#                 Followup_title=data['Followup_title'],
#                 Followup_date=followup_date,
#                 Followup_time=followup_time,
#                 created_at=datetime.now()
#             )
#             lead.save()

#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
#     else:
#         return JsonResponse({'status': 'invalid request'}, status=400)









def login(request):
    # Clear session data
    request.session.flush()

    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    try:
        ob = Login.objects.get(username=username, password=password)
        if ob.type == "admin":
            request.session['alid'] = ob.id
            return HttpResponse("<script>window.location='/adminDashboard'</script>")
        elif ob.type == "staff":
            request.session['slid'] = ob.id
            return HttpResponse("<script>window.location='/staffDashboard'</script>")
        else:
            return HttpResponse("<script>alert('Invalid username or password');window.location='/loginForm'</script>")
    except Login.DoesNotExist:
        return HttpResponse("<script>alert('Invalid username or password');window.location='/loginForm'</script>")

def forgetpwd(request):
   return render(request, "main/forgetpwd.html")

def getpwd(request):
    email_id=request.POST['emailid']
    try:
        pwd = Login.objects.get(username=email_id)
    except Login.DoesNotExist:
        return HttpResponse("<script>alert('Invalid email address.');window.location='/forgetpwd'</script>")

    if pwd is not None:
        send_mail('CREDITCARD FRAUD DETECTION', "YOUR NEW PASSWORD IS  -" + pwd.password, 'email@gmail.com', [email_id],
                  fail_silently=False)
        return HttpResponse("<script>alert('Email sent successfully.');window.location='/loginForm'</script>")
    else:
        return HttpResponse("<script>alert('Please enter valid email address.');window.location='/forgetpwd'</script>")
def changepwdform(request):
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context={
        'admin':[admin]
    }
    return render(request,"main/changepwd.html",context)
def changepwd(request):
    cpwd=request.POST['currentpwd']
    npwd=request.POST['newpwd']
    cnpwd=request.POST['confirmnewpwd']
    try:
        ob=Login.objects.get(password=cpwd,id=request.session['alid'])
        if ob is not None:
            if npwd == cnpwd:
                ob.password=npwd
                # ob.npwd=cnpwd
                ob.save()
                return HttpResponse("<script> alert('password changed  successfully');window.location='/adminDashboard'</script>")
            else:
                return HttpResponse("<script> alert(' password mismatch');window.location='/changepwdform'</script>")
    except:
        return HttpResponse("<script> alert('incorrect password');window.location='/changepwdform'</script>")


def editStaffForm(request,id):
    staff = Staff.objects.get(id=id)
    request.session['staffid']=staff.id
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context = {
        'staff':staff,
        'admin':[admin],
    }
    return render(request,'main/editstaff.html',context)
def staffForm(request):
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context = {
        'admin':[admin],
    }
    return render(request,'main/addstaff.html',context)
def addStaff(request):
     Name=request.POST['name']
     EmailId=request.POST['emailid']
     PhoneNumber=request.POST['phonenumber']
    #  Place=request.POST['place']
    #  City=request.POST['city']
    #  State=request.POST['state']
    #  Country=request.POST['country']
     Role=request.POST['designation']
     Admin=request.POST['admin']
     login_id = request.session.get('alid')
     admin = AdminRegister.objects.filter(Lid_id=login_id).first()
     ob=Login()
     ob.username=Name+'CRM'
     ob.password=Name+'@'+PhoneNumber[-5:]
     ob.type='staff'
     ob.save()
     ob1=Staff()
     ob1.Name=Name
     ob1.Lid=ob
     ob1.EmailId=EmailId
     ob1.Admin=Admin
    #  ob1.Place=Place
     ob1.PhoneNumber=PhoneNumber
    #  ob1.City=City
    #  ob1.State=State
    #  ob1.Country=Country
     ob1.admin=admin
     ob1.Role=Role
     ob1.save()
     return HttpResponse("<script>alert('Inserted successfully');window.location='/staff'</script>")

def staff(request):
    login_id = request.session.get('alid')
    staffs=Staff.objects.filter(admin__Lid_id=login_id)
    # staffs=Staff.objects.all()
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context = {
        'staffs':staffs,
        'admin':[admin],
    }
    return render(request,'main/staff.html',context)
def deleteStaff(request,id):
    ob = Staff.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('deleted successfully');window.location='/staff'</script>")
def editStaff(request):
     Name=request.POST['name']
     EmailId=request.POST['emailid']
     PhoneNumber=request.POST['phonenumber']
    #  Place=request.POST['place']
    #  City=request.POST['city']
    #  State=request.POST['state']
    #  Country=request.POST['country']
     Role=request.POST['role']
     Admin=request.POST['admin']
     ob1 = Staff.objects.get(id=request.session['staffid'])
     ob1.Name=Name
     ob1.EmailId=EmailId
     ob1.Admin=Admin
     ob1.PhoneNumber=PhoneNumber
     ob1.Role=Role
     ob1.save()
     return HttpResponse("<script>alert('edited successfully');window.location='/staff'</script>")

from datetime import date, timedelta


def adminDashboard(request):
    login_id = request.session.get('alid')
    leads = Lead.objects.filter(admin__Lid_id=login_id)
    status = Status.objects.all()
    purposes = Purpose.objects.all()
    purpose_counts = leads.values('Purpose__LeadPurpose').annotate(count=Count('Purpose'))
    purpose_data = [['Purpose', 'Count']]
    for purpose in purposes:
        purpose_name = purpose.LeadPurpose
        count = next((item['count'] for item in purpose_counts if item['Purpose__LeadPurpose'] == purpose_name), 0)
        purpose_data.append([purpose_name, count])

    sources = Source.objects.all()
    source_counts = leads.values('Source__LeadSource').annotate(count=Count('Source'))
    source_data = [['Source', 'Count']]
    for source in sources:
        source_name = source.LeadSource
        count = next((item['count'] for item in source_counts if item['Source__LeadSource'] == source_name), 0)
        source_data.append([source_name, count])
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()

    today = leads.filter(created_at__date=date.today()).count()
    week = leads.filter(created_at__date__gte=date.today() - timedelta(days=7)).count()
    month = leads.filter(created_at__date__gte=date.today() - timedelta(days=30)).count()
    total = leads.all().count()
    statuses = status.annotate(count=Count('lead', filter=Q(lead__in=leads)))
    lead_counts_query = leads.filter(created_at__date__gte=date.today() - timedelta(days=15)).values('created_at__date').annotate(count=Count('id'))
    lead_counts = [item['count'] for item in lead_counts_query]

    context = {
        'lead_counts': lead_counts,
        'admin': [admin],  # Pass admin as a queryset
        'today': today,
        'weekly': week,
        'monthly': month,
        'total': total,
        'statuses': statuses,
        'purpose_data': purpose_data,
        'source_data': source_data,
    }
    return render(request, "main/admindashboard.html", context)

from .utils import generate_barrier_token

def addAdmin(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        EmailId = request.POST.get('emailid')
        PhoneNumber = request.POST.get('phonenumber')
        Password = request.POST.get('password')
        PabblyApiToken = request.POST.get('pabbly_api_token')  # Get the token from the form
        CreatedTime = datetime.now()  # Assuming creation time is current time

        # Generate barrier token
        barrier_token = generate_barrier_token(EmailId, PhoneNumber, CreatedTime)


        request.session['name'] = Name
        request.session['email'] = EmailId

        otp = randint(100000, 999999)
        request.session['otp'] = otp

        subject = 'Email Verification'
        message = f"Hey {Name},\n\nYour OTP is: {otp}\n\nThank you for being a part of LeadLoom. If you have any questions regarding the onboarding process, please feel free to contact us at customercare.gmail.com"
        from_email = 'quickfixsorter123@gmail.com'
        recipient_list = [EmailId]

        send_mail(subject, message, from_email, recipient_list)

        ob = Login()
        ob.username = EmailId
        ob.password = Password

        ob.type = 'admin'
        ob.save()

        ob1 = AdminRegister()
        ob1.Lid = ob
        ob1.Name = Name
        ob1.EmailId = EmailId
        ob1.PhoneNumber = PhoneNumber
        ob1.PabblyApiToken = PabblyApiToken  # Save the token
        ob1.BarrierToken = barrier_token
        ob1.save()
        return HttpResponse("<script>alert('Inserted successfully');window.location='/otpForm'</script>")
    else:
        return HttpResponse("Method Not Allowed")
def expire_otp(request):
   print("/////////")
   if request.method == 'POST':
       print("*************MMMMMMMM")
       request.session.pop('otp', None)
       request.session.pop('rotp', None)
   return HttpResponse("<script>alert('OTP expired');window.location='/otpForm'</script>")
def resendOTP(request):
     print("@@@@@@@@@2")
     Name = request.session.get('name')
     EmailId = request.session.get('email')
     otp = randint(100000, 999999)
     request.session.pop('otp', None)
     request.session['rotp'] = otp
     subject = 'Email Verification'
     message = f"Hey {Name},\n\nYour OTP is: {otp}\n\nThank you for being a part of LeadLoom. If you have any questions regarding the onboarding process, please feel free to contact us at customercare.gmail.com"
     from_email = 'quickfixsorter123@gmail.com'
     recipient_list = [EmailId]

     send_mail(subject, message, from_email, recipient_list)
     return HttpResponse("<script>alert('OTP resent successfully');window.location='/otpForm'</script>")
def verifyOTP(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        resend_otp = request.session.get('rotp')
        print(entered_otp, stored_otp,"+++++++++++++++++++++____")
        print(type(entered_otp),type(stored_otp))
        if int(entered_otp) == stored_otp or  int(entered_otp) == resend_otp :
            print("****")
            return HttpResponse("<script>alert('OTP verification successful');window.location='/loginForm'</script>")
        else:
            return HttpResponse("<script>alert('Incorrect OTP. Please try again.');window.location='/otpForm'</script>")
    else:
        return HttpResponse("Invalid request method")
def editAdmin(request):
     Name=request.POST['name']
     EmailId=request.POST['emailid']
     PhoneNumber=request.POST['phonenumber']
     Place=request.POST['place']
     City=request.POST['city']
     State=request.POST['state']
     Country=request.POST['country']
     ob1= AdminRegister.objects.get(id=request.session['alid'])
     ob1.Name=Name
     ob1.EmailId=EmailId
     ob1.Place=Place
     ob1.PhoneNumber=PhoneNumber
     ob1.City=City
     ob1.State=State
     ob1.Country=Country
     ob1.save()
     return HttpResponse("<script>alert('Inserted successfully');window.location='/profile'</script>")
from django.core.paginator import Paginator

def lead(request):
    # leads = Lead.objects.all()
    login_id = request.session.get('alid')
    leads = Lead.objects.filter(admin__Lid_id=login_id)
    sort_by = request.GET.get('sort_by', 'asc')
    if sort_by == 'desc':
        leads = leads.order_by('-created_at')  # Descending order
    else:
        leads = leads.order_by('created_at')

    # Pagination
    per_page = int(request.GET.get('per_page', 10))  # Default per page is 10
    paginator = Paginator(leads, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sources = Source.objects.all()
    purposes = Purpose.objects.all()
    statuses = Status.objects.all()
    staffs = Staff.objects.all()
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context = {
        'page_obj': page_obj,
        'sources': sources,
        'purposes': purposes,
        'statuses': statuses,
        'staffs': staffs,
        'admin': [admin],
    }
    return render(request, 'main/lead.html', context)
def staffleads(request):
    login_id = request.session.get('slid')
    leads = Lead.objects.filter(Staff__Lid_id=login_id)
    sort_by = request.GET.get('sort_by', 'asc')
    if sort_by == 'desc':
        leads = leads.order_by('-created_at')  # Descending order
    else:
        leads = leads.order_by('created_at')
    per_page = int(request.GET.get('per_page', 10))  # Default per page is 10
    paginator = Paginator(leads, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    sources = Source.objects.all()
    purposes = Purpose.objects.all()
    statuses = Status.objects.all()
    staffs = Staff.objects.all()
    context = {
        'page_obj': page_obj,
        'sources': sources,
        'purposes': purposes,
        'statuses': statuses,
        'staffs': staffs,
    }
    return render(request,'main/staffleads.html',context)
def addLeadForm(request):
    source=Source.objects.all()
    purpose=Purpose.objects.all()
    status=Status.objects.all()
    staff=Staff.objects.all()
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context = {
        'source':source,
        'purpose':purpose,
        'status':status,
        'staff':staff,
        'admin':[admin],

    }
    return render(request,'main/addlead.html',context)
def editLeadForm(request,id):
    source=Source.objects.all()
    purpose=Purpose.objects.all()
    status=Status.objects.all()
    staff=Staff.objects.all()
    lead = Lead.objects.get(id=id)
    request.session['Leadid']=lead.id
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context = {
        'source':source,
        'purpose':purpose,
        'status':status,
        'staff':staff,
        'lead':lead,
        'admin':[admin],
    }

    return render(request,'main/editLead.html',context)
def addLead(request):
     CustomerName=request.POST['customername']
     CompanyName=request.POST['companyname']
     EmailId=request.POST['emailid']
     PhoneNumber=request.POST['phonenumber']
     AlternativeNumber=request.POST['alternativenumber']
     address=request.POST['address']
     Sources=request.POST['source']
     Purposes=request.POST['purpose']
     Type=request.POST['type']
     Statuss=request.POST['status']
     Staffs=request.POST['staff']
     Note=request.POST['note']
     Followup_title=request.POST['Followup_title']
     Followup_date=request.POST['Followup_date']
     Followup_time=request.POST['Followup_time']
     login_id = request.session.get('alid')
     admin = AdminRegister.objects.filter(Lid_id=login_id).first()
     ob1=Lead()
     obsourse=Source.objects.get(id=Sources)
     obpurpose=Purpose.objects.get(id=Purposes)
     obstatus=Status.objects.get(id=Statuss)
     obstaff=Staff.objects.get(id=Staffs)
     ob1.CustomerName=CustomerName
     ob1.CompanyName=CompanyName
     ob1.EmailId=EmailId
     ob1.PhoneNumber=PhoneNumber
     ob1.AlternativeNumber=AlternativeNumber
     ob1.address=address
     ob1.Source=obsourse
     ob1.Purpose=obpurpose
     ob1.Type=Type
     ob1.Status=obstatus
     ob1.Staff=obstaff
     ob1.Note=Note
     ob1.Followup_title=Followup_title
     ob1.Followup_date=Followup_date
     ob1.Followup_time=Followup_time
     ob1.admin=admin
     ob1.save()
     return HttpResponse("<script>alert('Inserted successfully');window.location='/lead'</script>")
def deleteLead(request,id):
    ob = Lead.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('deleted successfully');window.location='/lead'</script>")
def editLead(request):
     origin = request.POST.get('origin')
     CustomerName=request.POST['customernames']
     CompanyName=request.POST['companynames']
     EmailId=request.POST['emailids']
     PhoneNumber=request.POST['phonenumbers']
     AlternativeNumber=request.POST['alternativenumbers']
     address=request.POST['address']
     Sources=request.POST['source']
     Purposes=request.POST['purpose']
     Type=request.POST['type']
     Statuss=request.POST['status']
     Staffs=request.POST['staff']
     Note=request.POST['notes']
     ob1= Lead.objects.get(id=request.session['Leadid'])
     obsourse=Source.objects.get(id=Sources)
     obpurpose=Purpose.objects.get(id=Purposes)
     obstatus=Status.objects.get(id=Statuss)
     obstaff=Staff.objects.get(id=Staffs)
     ob1.CustomerName=CustomerName
     ob1.CompanyName=CompanyName
     ob1.EmailId=EmailId
     ob1.PhoneNumber=PhoneNumber
     ob1.AlternativeNumber=AlternativeNumber
     ob1.address=address
     ob1.Source=obsourse
     ob1.Purpose=obpurpose
     ob1.Type=Type
     ob1.Status=obstatus
     ob1.Staff=obstaff
     ob1.Note=Note
     ob1.save()
     if origin == 'adminedit':
        return HttpResponse("<script>alert('Inserted successfully');window.location='/lead'</script>")
     elif origin == 'staffedit':
        return HttpResponse("<script>alert('Inserted successfully');window.location='/staffleads'</script>")

def addcompany(request):
     CompanyName=request.POST['companyname']
     EmailId=request.POST['emailid']
     PhoneNumber=request.POST['phonenumber']
     Country=request.POST['alternativenumber']
     Website=request.POST['place']
     Location=request.POST['place']
     admin_id = request.session.get('alid')
     ob=Company()
     ob.CompanyName=CompanyName
     ob.Location=Location
     ob.Country=Country
     ob.PhoneNumber=PhoneNumber
     ob.EmailId=EmailId
     ob.Website=Website
     ob.Admin=admin_id
     ob.save()
     return HttpResponse("<script>alert('Inserted successfully');window.location='/'</script>")
def deletecompany(request,id):
    ob = Company.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('deleted successfully');window.location='/'</script>")

def editcompany(request,id):
     CompanyName=request.POST['companyname']
     EmailId=request.POST['emailid']
     PhoneNumber=request.POST['phonenumber']
     Country=request.POST['alternativenumber']
     Website=request.POST['place']
     Location=request.POST['place']
     admin_id = request.session.get('alid')
     ob=Company()
     ob.CompanyName=CompanyName
     ob.Location=Location
     ob.Country=Country
     ob.PhoneNumber=PhoneNumber
     ob.EmailId=EmailId
     ob.Website=Website
     ob.Admin=admin_id
     ob.save()
     return HttpResponse("<script>alert('Inserted successfully');window.location='/'</script>")
def  source(request):
    leadsource=request.POST['leadsource']
    ob=Source()
    ob.LeadSource=leadsource
    ob.save()
    return HttpResponse("<script>alert('Inserted successfully');window.location='/addLeadForm'</script>")
def purpose(request):
    leadPurpose=request.POST['leadPurpose']
    origin=request.POST['origin']
    if origin == 'lead':
        ob1 = Purpose()
        ob1.LeadPurpose = leadPurpose
        ob1.save()
        return HttpResponse("<script>alert('Inserted successfully');window.location='/addLeadForm'</script>")
    elif origin == 'purpose':
        ob1 = Purpose()
        ob1.LeadPurpose = leadPurpose
        ob1.save()
        return HttpResponse("<script>alert('Inserted successfully');window.location='/leadpurpose'</script>")
    else:
        print("+++")
def searchpurpose(request):
    search_term = request.POST.get('searchitem', '')
    results = Purpose.objects.filter(
             Q(LeadPurpose__icontains=search_term)
    )
    context={
        'purposes':results
    }
    return render (request,'main/leadpurpose.html',context)
def deletepurpose(request,id):
    ob = Purpose.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('deleted successfully');window.location='/leadpurpose'</script>")
def status(request):
    leadstatus=request.POST['leadstatus']
    color=request.POST['color']
    rgb_color = ImageColor.getrgb(color)
    ob2=Status()
    ob2.LeadStatus=leadstatus
    ob2.color="rgb"+str(rgb_color)
    ob2.save()
    return HttpResponse("<script>alert('Inserted successfully');window.location='/addLeadForm'</script>")
def settings(request):
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    context = {
        'admin': [admin],
    }
    return render(request,'main/settings.html',context)


def filterSearch(request):
    sources = Source.objects.all()
    purposes = Purpose.objects.all()
    statuses = Status.objects.all()
    staffs = Staff.objects.all()

    source_id = request.GET.get('source', '')
    purpose_id = request.GET.get('purpose', '')
    status_id = request.GET.get('status', '')
    staff_id = request.GET.get('staff', '')
    date_filter = request.GET.get('date_filter')

    login_id = request.session.get('alid')
    leads = Lead.objects.filter(admin__Lid_id=login_id)
    sort_by = request.GET.get('sort_by', 'asc')
    if sort_by == 'desc':
        leads = leads.order_by('-created_at')  # Descending order
    else:
        leads = leads.order_by('created_at')

    if source_id:
        leads = leads.filter(Source__id=source_id)
    if purpose_id:
        leads = leads.filter(Purpose__id=purpose_id)
    if status_id:
        leads = leads.filter(Status__id=status_id)
    if staff_id:
        leads = leads.filter(Staff__id=staff_id)

    if date_filter:
        today = datetime.date.today()
        if date_filter == 'today':
            leads = leads.filter(created_at__date=today - datetime.timedelta(days=0))
        elif date_filter == 'yesterday':
            leads = leads.filter(created_at__date=today - datetime.timedelta(days=1))
        elif date_filter == 'last_7_days':
            leads = leads.filter(created_at__date__gte=today - datetime.timedelta(days=7))
        elif date_filter == 'last_30_days':
            leads = leads.filter(created_at__date__gte=today - datetime.timedelta(days=30))
        elif date_filter == 'this_month':
            leads = leads.filter(created_at__month=today.month, created_at__year=today.year)
        elif date_filter == 'last_month':
            last_month = today.replace(day=1) - datetime.timedelta(days=1)
            leads = leads.filter(created_at__month=last_month.month, created_at__year=last_month.year)
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()

    context = {
        'admin':[admin],
        'page_obj': leads,
        'sources': sources,
        'purposes': purposes,
        'statuses': statuses,
        'staffs': staffs,
        'selected_source': int(source_id) if source_id else None,
        'selected_purpose': int(purpose_id) if purpose_id else None,
        'selected_status': int(status_id) if status_id else None,
        'selected_staff': int(staff_id) if staff_id else None,
    }
    return render(request, 'main/lead.html', context)

def filterSearchstaff(request):
    sources = Source.objects.all()
    purposes = Purpose.objects.all()
    statuses = Status.objects.all()
    staffs = Staff.objects.all()

    source_id = request.GET.get('source', '')
    purpose_id = request.GET.get('purpose', '')
    status_id = request.GET.get('status', '')
    staff_id = request.GET.get('staff', '')
    date_filter = request.GET.get('date_filter')

    login_id = request.session.get('slid')
    leads = Lead.objects.filter(Staff__Lid_id=login_id)
    sort_by = request.GET.get('sort_by', 'asc')
    if sort_by == 'desc':
        leads = leads.order_by('-created_at')  # Descending order
    else:
        leads = leads.order_by('created_at')

    if source_id:
        leads = leads.filter(Source__id=source_id)
    if purpose_id:
        leads = leads.filter(Purpose__id=purpose_id)
    if status_id:
        leads = leads.filter(Status__id=status_id)
    if staff_id:
        leads = leads.filter(Staff__id=staff_id)

    if date_filter:
        today = datetime.date.today()
        if date_filter == 'today':
            leads = leads.filter(created_at__date=today - datetime.timedelta(days=0))
        elif date_filter == 'yesterday':
            leads = leads.filter(created_at__date=today - datetime.timedelta(days=1))
        elif date_filter == 'last_7_days':
            leads = leads.filter(created_at__date__gte=today - datetime.timedelta(days=7))
        elif date_filter == 'last_30_days':
            leads = leads.filter(created_at__date__gte=today - datetime.timedelta(days=30))
        elif date_filter == 'this_month':
            leads = leads.filter(created_at__month=today.month, created_at__year=today.year)
        elif date_filter == 'last_month':
            last_month = today.replace(day=1) - datetime.timedelta(days=1)
            leads = leads.filter(created_at__month=last_month.month, created_at__year=last_month.year)

    context = {
        'page_obj': leads,
        'sources': sources,
        'purposes': purposes,
        'statuses': statuses,
        'staffs': staffs,
        'selected_source': int(source_id) if source_id else None,
        'selected_purpose': int(purpose_id) if purpose_id else None,
        'selected_status': int(status_id) if status_id else None,
        'selected_staff': int(staff_id) if staff_id else None,
    }
    return render(request, 'main/staffleads.html', context)

def profile(request):
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id)
    return render(request, 'main/profile.html', {'admin': admin})
@csrf_exempt
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('image'):
        admin = AdminRegister.objects.get(pk=request.user.id)
        admin.Image = request.FILES['image']
        admin.save()
        return JsonResponse({'message': 'Profile picture updated successfully'})
    else:
        return JsonResponse({'error': 'No image file received'}, status=400)


def search(request):
        sources = Source.objects.all()
        purposes = Purpose.objects.all()
        statuses = Status.objects.all()
        staffs = Staff.objects.all()
        search_term = request.POST.get('searchitem', '')
        login_id = request.session.get('alid')
        admin = AdminRegister.objects.filter(Lid_id=login_id).first()
        leads = Lead.objects.filter(admin__Lid_id=login_id)
        sort_by = request.GET.get('sort_by', 'asc')
        if sort_by == 'desc':
             leads = leads.order_by('-created_at')
        else:
             leads = leads.order_by('created_at')
        results = leads.filter(
            Q(CustomerName__icontains=search_term) |
            Q(PhoneNumber__icontains=search_term) |
            Q(Source__LeadSource__icontains=search_term) |  # Adjusted to use the actual field name of Source model
            Q(EmailId__icontains=search_term) |
            Q(AlternativeNumber__icontains=search_term) |
            Q(Purpose__LeadPurpose__icontains=search_term) |
            Q(Status__LeadStatus__icontains=search_term) |
            Q(Staff__Name__icontains=search_term) |
            Q(CompanyName__icontains=search_term) |
            Q(Note__icontains=search_term) |
            Q(address__icontains=search_term)|
            Q(Followup_title__icontains=search_term) |
            Q(Followup_date__icontains=search_term) |
            Q(Followup_time__icontains=search_term) |
            Q(admin__Name__icontains=search_term)


        )
        context={
            'admin':[admin],
            'page_obj':results,
            'sources': sources,
            'purposes': purposes,
            'statuses': statuses,
            'staffs':staffs
        }
        return render(request, 'main/lead.html',context)

def searchstaff(request):
        sources = Source.objects.all()
        purposes = Purpose.objects.all()
        statuses = Status.objects.all()
        staffs = Staff.objects.all()
        search_term = request.POST.get('searchitem', '')
        login_id = request.session.get('slid')
        admin = AdminRegister.objects.filter(Lid_id=login_id).first()
        leads = Lead.objects.filter(Staff__Lid_id=login_id)
        sort_by = request.GET.get('sort_by', 'asc')
        if sort_by == 'desc':
             leads = leads.order_by('-created_at')
        else:
             leads = leads.order_by('created_at')
        results = leads.filter(
            Q(CustomerName__icontains=search_term) |
            Q(PhoneNumber__icontains=search_term) |
            Q(Source__LeadSource__icontains=search_term) |  # Adjusted to use the actual field name of Source model
            Q(EmailId__icontains=search_term) |
            Q(AlternativeNumber__icontains=search_term) |
            Q(Purpose__LeadPurpose__icontains=search_term) |
            Q(Status__LeadStatus__icontains=search_term) |
            Q(Staff__Name__icontains=search_term) |
            Q(CompanyName__icontains=search_term) |
            Q(Note__icontains=search_term) |
            Q(address__icontains=search_term)|
            Q(Followup_title__icontains=search_term) |
            Q(Followup_date__icontains=search_term) |
            Q(Followup_time__icontains=search_term) |
            Q(admin__Name__icontains=search_term)


        )
        context={
            'admin':[admin],
            'page_obj':results,
            'sources': sources,
            'purposes': purposes,
            'statuses': statuses,
            'staffs':staffs
        }
        return render(request, 'main/staffleads.html',context)
def editTaskForm(request, id):
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    leads = Lead.objects.filter(admin__Lid_id=login_id)
    staffs = Staff.objects.filter(admin__Lid_id=login_id)
    task = Task.objects.get(id=id)
    request.session['taskid'] = task.id
    taskcategory = Taskcategory.objects.all()
    callstatus = Callstatus.objects.all()
    context = {
        'admin': [admin],
        'leads': leads,
        'staffs': staffs,
        'task': task,
        'taskcategory': taskcategory,
        'callstatus': callstatus,
        'date':str(task.Date),
        'time':str(task.Time)
    }
    return render(request, 'main/edittask.html', context)
def task(request):
    login_id = request.session.get('alid')
    admin = AdminRegister.objects.filter(Lid_id=login_id).first()
    leads = Lead.objects.filter(admin__Lid_id=login_id)
    staffs = Staff.objects.filter(admin__Lid_id=login_id)
    tasks = Task.objects.all()  # Query tasks
    taskcategory = Taskcategory.objects.all()
    callstatus=Callstatus.objects.all()
    context = {
        'admin': [admin],
        'leads': leads,
        'staffs': staffs,
        'tasks': tasks,  # Add tasks to context
        'taskcategory': taskcategory,
        'callstatus':callstatus
    }
    return render(request, 'main/task.html', context)

from django.http import HttpResponse
from .models import Task, Lead, Staff, Taskcategory, AdminRegister, Callstatus

def addTask(request):
    if request.method == 'POST':
        TaskName = request.POST.get('taskname')
        lead_id = request.POST.get('leads')
        lead_instance = Lead.objects.get(pk=lead_id)
        assigned_to_id = request.POST.get('staff')
        staff_instance = Staff.objects.get(pk=assigned_to_id)
        task_category_id = request.POST.get('taskcategory')
        task_category_instance = Taskcategory.objects.get(pk=task_category_id)
        Date = request.POST.get('date')
        Time = request.POST.get('time')
        Description = request.POST.get('description')
        call_status = "Pending"

        # Try to get the "Pending" status, create it if it doesn't exist
        try:
            pending_status = Callstatus.objects.get(CallStatus=call_status)
        except Callstatus.DoesNotExist:
            # Create the "Pending" status if it doesn't exist
            pending_status = Callstatus.objects.create(CallStatus=call_status)

        login_id = request.session.get('alid')
        admin = AdminRegister.objects.filter(Lid_id=login_id).first()

        ob1 = Task.objects.create(
            TaskName=TaskName,
            Lead=lead_instance,
            AssignedBy=admin,
            AssignedTo=staff_instance,
            TaskCategory=task_category_instance,
            Date=Date,
            Time=Time,
            Description=Description,
            CallStatus=pending_status
        )

        return HttpResponse("<script>alert('Inserted successfully');window.location='/task'</script>")

    # If the request method is not POST, handle it accordingly
    else:
        return HttpResponse("Invalid request method")


def editTask(request):
    TaskName = request.POST['taskname']
    lead_id = request.POST.get('leads')
    lead_instance = Lead.objects.get(pk=lead_id)
    assigned_to_id = request.POST.get('staff')
    staff_instance = Staff.objects.get(pk=assigned_to_id)
    comment = request.POST['comment']
    task_category_id = request.POST.get('taskcategory')
    task_category_instance = Taskcategory.objects.get(pk=task_category_id)
    Date = request.POST['date']
    Time = request.POST['time']
    Description = request.POST['description']
    call_status_id = request.POST.get('callstatus')
    call_status_instance = Callstatus.objects.get(pk=call_status_id)
    ob1 = Task.objects.get(id=request.session['taskid'])
    ob1.TaskName = TaskName
    ob1.Lead = lead_instance
    ob1.AssignedTo = staff_instance
    ob1.Comment = comment
    ob1.TaskCategory = task_category_instance
    ob1.Date = Date
    ob1.Time = Time
    ob1.Description = Description
    ob1.CallStatus = call_status_instance
    ob1.save()
    return HttpResponse("<script>alert('Updated successfully');window.location='/task'</script>")
def deleteTask(request,id):
    ob = Task.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert('deleted successfully');window.location='/task'</script>")


# views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Properties

# @csrf_exempt
# def add_property(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         price = request.POST.get('price')

#         # Save property in the CRM
#         property_obj = Properties.objects.create(
#             title=title,
#             description=description,
#             price=price,
#         )
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
# views.py (in your CRM application)

# from django.http import JsonResponse
# from rest_framework import status
# import requests
# from rest_framework import generics
# from .models import Properties
# from .serializers import PropertiesSerializer

# class PropertiesListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Properties.objects.all()
#     serializer_class = PropertiesSerializer
# def add_property(request):
#     if request.method == 'POST':
#         # Extract data from the POST request
#         serializer = PropertiesSerializer(data=request.data)

#         # Check if the data is valid
#         if serializer.is_valid():
#             # Save the property to the CRM database
#             property_obj = serializer.save()

#             try:
#                 # Send the property data to the real estate website's API
#                 response = requests.post('https://www.kifrealty.com/api/add_property/', json=serializer.data)
#                 response.raise_for_status()  # Raise an error for non-2xx response

#                 # Check response from the real estate website
#                 if response.status_code == status.HTTP_200_OK:
#                     return JsonResponse({'status': 'success'})
#                 else:
#                     # If the real estate website API returns an error response
#                     property_obj.delete()
#                     return JsonResponse({'status': 'error', 'message': 'Failed to add property to Real Estate website'},
#                                         status=status.HTTP_503_SERVICE_UNAVAILABLE)

#             except requests.exceptions.RequestException as e:
#                 # If the request to the real estate website's API fails,
#                 # delete the property from the CRM database to maintain consistency
#                 property_obj.delete()
#                 return JsonResponse({'status': 'error', 'message': f'Failed to add property to Real Estate website: {str(e)}'},
#                                     status=status.HTTP_503_SERVICE_UNAVAILABLE)
#         else:
#             # If the data provided in the request is invalid,
#             # return an error response with details about the validation errors
#             return JsonResponse({'status': 'error', 'message': 'Invalid data', 'errors': serializer.errors},
#                                 status=status.HTTP_400_BAD_REQUEST)
#     else:
#         # If the request method is not POST,
#         # return an error response
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method. Only POST requests are allowed.'},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)


# views.py

from rest_framework import generics
from .models import Properties
from .serializers import PropertiesSerializer

class PropertiesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSerializer


from rest_framework import viewsets
from .models import Property, PropertyImage, PropertyCategory, Location, Developer
from .serializers import PropertySerializer, PropertyImageSerializer, PropertyCategorySerializer, LocationSerializer, DeveloperSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyCategoryViewSet(viewsets.ModelViewSet):
    queryset = PropertyCategory.objects.all()
    serializer_class = PropertyCategorySerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Property
from .serializers import PropertySerializer


class PropertiesAPI(APIView):
    def get(self, request):
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)


#privyr integration

@csrf_exempt
def handle_privyr_webhook(request):
    if request.method == 'POST':
        try:
            # Extract lead data from the request payload
            payload = json.loads(request.body)

            # Extract and process lead data
            lead_name = payload.get('name')
            lead_email = payload.get('email')
            lead_phone = payload.get('phone')
            lead_company_name = payload.get('company_name', None)
            lead_alternative_number = payload.get('alternative_number', None)
            lead_address = payload.get('address', '')
            lead_type = payload.get('type', '')
            lead_note = payload.get('note', None)
            followup_title = payload.get('followup_title', '')
            followup_date = payload.get('followup_date', '2023-01-01')  # Adjust default date
            followup_time = payload.get('followup_time', '00:00:00')  # Adjust default time

            # Assume foreign key fields come as IDs and are included in the payload
            admin_id = payload.get('admin_id')
            source_id = payload.get('source_id')
            purpose_id = payload.get('purpose_id')
            status_id = payload.get('status_id')
            staff_id = payload.get('staff_id')

            # Fetch related objects
            admin = AdminRegister.objects.get(id=admin_id)
            source = Source.objects.get(id=source_id)
            purpose = Purpose.objects.get(id=purpose_id)
            status = Status.objects.get(id=status_id)
            staff = Staff.objects.get(id=staff_id)

            # Save lead data to your database
            lead = Lead.objects.create(
                admin=admin,
                CustomerName=lead_name,
                CompanyName=lead_company_name,
                EmailId=lead_email,
                PhoneNumber=lead_phone,
                AlternativeNumber=lead_alternative_number,
                address=lead_address,
                Source=source,
                Purpose=purpose,
                Type=lead_type,
                Status=status,
                Staff=staff,
                Note=lead_note,
                Followup_title=followup_title,
                Followup_date=followup_date,
                Followup_time=followup_time,
            )

            # Respond with a success message
            return JsonResponse({'message': 'Lead received and saved successfully'}, status=200)

        except Exception as e:
            # Respond with an error if there's any issue processing the lead
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Respond with an error if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=405)
