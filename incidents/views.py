from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q  # For complex lookups in search functionality
from .models import Incident, Comment
from .forms import IncidentForm, CommentForm
from datetime import datetime
from django.http import HttpResponse  # For test email view

# Custom LoginView
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('incidents:profile'))

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('incidents:incident_list')

# View to list all incidents
def incident_list(request):
    incidents = Incident.objects.all().order_by('-date_reported')
    current_year = datetime.now().year
    return render(request, 'incidents/incident_list.html', {
        'incidents': incidents,
        'current_year': current_year
    })

# View for detailed incident with comments
def incident_detail(request, id):
    incident = get_object_or_404(Incident, id=id)
    comments = incident.comments.select_related('user')
    current_year = datetime.now().year

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.incident = incident
            comment.user = request.user if request.user.is_authenticated else None
            comment.save()
            messages.success(request, "Comment successfully added.")
            return redirect('incidents:incident_detail', id=incident.id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'incidents/incident_detail.html', {
        'incident': incident,
        'comments': comments,
        'comment_form': comment_form,
        'current_year': current_year
    })

# Report a new incident
@login_required
def report_incident(request):
    current_year = datetime.now().year
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reporter = request.user
            incident.save()
            messages.success(request, "Incident reported successfully.")
            return redirect('incidents:incident_list')
    else:
        form = IncidentForm()
    
    return render(request, 'incidents/report_incident.html', {
        'form': form,
        'current_year': current_year
    })

# Edit an existing incident
@login_required
def edit_incident(request, id):
    incident = get_object_or_404(Incident, id=id)
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES, instance=incident)
        if form.is_valid():
            form.save()
            messages.info(request, "Incident updated successfully.")
            return redirect('incidents:incident_detail', id=incident.id)
    else:
        form = IncidentForm(instance=incident)
    
    return render(request, 'incidents/edit_incident.html', {
        'form': form,
        'incident': incident
    })

# Search incidents
def incident_search(request):
    query = request.GET.get('q')
    incidents = Incident.objects.all()

    if query:
        incidents = incidents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(reporter__username__icontains=query)
        ).order_by('-date_reported')
    
    current_year = datetime.now().year
    return render(request, 'incidents/search_results.html', {
        'incidents': incidents,
        'query': query,
        'current_year': current_year
    })

# Static pages
def about_view(request):
    return render(request, 'incidents/about.html', {'current_year': datetime.now().year})

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Message from {name} ({email}, {phone}):\n\n{message}"

        send_mail(
            subject,
            full_message,
            'jacqueombeni@gmail.com',
            ['jacquesombeni558@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "Your message has been sent successfully.")
        return redirect('incidents:contacts')
    
    return redirect('incidents:contacts')

def contacts(request):
    return render(request, 'incidents/contacts.html', {'current_year': datetime.now().year})

def services(request):
    return render(request, 'incidents/services.html', {'current_year': datetime.now().year})

def blogs(request):
    return render(request, 'incidents/blogs.html', {'current_year': datetime.now().year})

def faq(request):
    return render(request, 'incidents/faq.html', {'current_year': datetime.now().year})

# User signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

# User profile
@login_required
def profile(request):
    return render(request, 'registration/profile.html', {
        'current_year': datetime.now().year,
        'user': request.user
    })

# Test email functionality
def test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email from the Incident Management System.',
            'jacqueombeni@gmail.com',
            ['jacquesombeni558@gmail.com'],  # Replace with your email for testing
            fail_silently=False,
        )
        return HttpResponse("Test email sent successfully.")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
