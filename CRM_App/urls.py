from django.urls import path,include
from . import views
from django.conf import settings
from .views import PropertiesListCreateAPIView
from django.conf.urls.static import static
urlpatterns = [
    path('base',views.base,name='base'),
    path('',views.home,name='home'),
    path('loginForm',views.loginForm,name='loginForm'),
    path('login',views.login,name='login'),
    path('addAdmin',views.addAdmin,name='addAdmin'),
    path('editAdmin',views.editAdmin,name='editAdmin'),
    path('staff',views.staff,name='staff'),
    path('addStaff',views.addStaff,name='addStaff'),
    path('deleteStaff/<int:id>',views.deleteStaff,name='deleteStaff'),
    path('editStaff',views.editStaff,name='editStaff'),
    path('addLead',views.addLead,name='addLead'),
    path('deleteLead/<int:id>',views.deleteLead,name='deleteLead'),
    path('editLead',views.editLead,name='editLead'),
    path('addcompany',views.addcompany,name='addcompany'),
    path('deletecompany',views.deletecompany,name='deletecompany'),
    path('editcompany',views.editcompany,name='editcompany'),
    path('source',views.source,name='source'),
    path('purpose',views.purpose,name='purpose'),
    path('status',views.status,name='status'),
    path('changepwd',views.changepwd,name="changepwd"),
    path('changepwdform',views.changepwdform,name="changepwdform"),
    path('otpForm',views.otpForm,name="otpForm"),
    path('verifyOTP',views.verifyOTP,name="verifyOTP"),
    path('resendOTP',views.resendOTP,name="resendOTP"),
    path('about',views.about,name="about"),
    path('expire_otp',views.expire_otp,name="expire_otp"),
    path('forgetpwd',views.forgetpwd,name="forgetpwd"),
    path('getpwd',views.getpwd,name="getpwd"),
    path('addLeadForm',views.addLeadForm,name="addLeadForm"),
    path('adminDashboard',views.adminDashboard,name="adminDashboard"),
    path('lead',views.lead,name="lead"),
    path('staff',views.staff,name='staff'),
    path('staffForm',views.staffForm,name='staffForm'),
    path('editLeadForm/<int:id>',views.editLeadForm,name="editLeadForm"),
    path('editStaffForm/<int:id>',views.editStaffForm,name="editStaffForm"),
    path('settings',views.settings,name="settings"),
    path('filterSearch',views.filterSearch,name="filterSearch"),
    path('profile',views.profile,name="profile"),
    path('update_profile_picture',views.update_profile_picture,name="update_profile_picture"),
    path('search',views.search,name="search"),
    path('staffDashboard',views.staffDashboard,name="staffDashboard"),
    path('staffleads',views.staffleads,name="staffleads"),
    path('staffeditlead/<int:id>',views.staffeditlead,name="staffeditlead"),
    path('filterSearchstaff',views.filterSearchstaff,name="filterSearchstaff"),
    path('task', views.task, name="task"),
    path('addTask', views.addTask, name="addTask"),
    path('editTaskForm/<int:id>', views.editTaskForm, name="editTaskForm"),
    path('editTask', views.editTask, name="editTask"),
    path('searchstaff',views.searchstaff,name="searchstaff"),
    path('deleteTask/<int:id>',views.deleteTask,name="deleteTask"),
    path('leadpurpose',views.leadpurpose,name='leadpurpose'),
    path('leadsource',views.leadsource,name='leadsource'),
    path('leadstatus',views.leadstatus,name='leadstatus'),
    path('deletepurpose/<int:id>',views.deletepurpose,name="deletepurpose"),
    path('searchpurpose',views.searchpurpose,name="searchpurpose"),
    path('pabbly_lead_webhook/', views.pabbly_lead_webhook, name='pabbly_lead_webhook'),
    #privyr
    path('privyr-webhook/',views.handle_privyr_webhook, name='privyr_webhook'),

    # path('api/add_property/', views.add_property, name='api_add_property'),
    # path('add_property/',views.add_property, name='add_property'),
    # path('properties/', PropertiesListCreateAPIView.as_view(), name='properties-list-create'),
    path('properties/', PropertiesListCreateAPIView.as_view(), name='properties-list-create'),
    path('propertiesapi/',views.PropertiesAPI.as_view(), name='properties_api'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)