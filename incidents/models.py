from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    severity = models.IntegerField()  # Consider using an Enum or more descriptive choices if needed
    date_reported = models.DateTimeField(auto_now_add=True)
    assigned_team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='incident_images/', null=True, blank=True)  # Add image field
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Add reporter field

    def __str__(self):
        return self.title

class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Comment(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='comments')  # Related name for comments
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow anonymous users
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'Comment by {self.user} on {self.incident}'
        return f'Anonymous comment on {self.incident}'
