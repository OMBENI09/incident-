from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import test_email

app_name = 'incidents'  # Set the app namespace for URL reversing

urlpatterns = [
    # Incident management
    path('', views.incident_list, name='incident_list'),  # List all incidents
    path('report/', views.report_incident, name='report_incident'),  # Report a new incident
    path('<int:id>/', views.incident_detail, name='incident_detail'),  # View incident details
    path('<int:id>/edit/', views.edit_incident, name='edit_incident'),  # Edit an incident

    # Authentication and user management
    path('signup/', views.signup, name='signup'),  # User signup
    path('login/', views.CustomLoginView.as_view(), name='login'),  # User login
    path('logout/', views.logout_view, name='logout'),  # Custom logout view
    path('profile/', views.profile, name='profile'),  # User profile

    # Static pages
    path('about/', views.about_view, name='about'),  # About page
    path('contacts/', views.contacts, name='contacts'),  # Contact page
    path('contact_submit/', views.contact_submit, name='contact_submit'),  # Contact form submission
    path('services/', views.services, name='services'),  # Services page
    path('blogs/', views.blogs, name='blogs'),  # Blogs page
    path('faq/', views.faq, name='faq'),  # FAQ page

    # Search
    path('search/', views.incident_search, name='incident_search'),  # Search incidents

    #testing an email

    path('test-email/', views.test_email, name='test_email'),
]
