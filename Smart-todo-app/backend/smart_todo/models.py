from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    tags = models.TextField(help_text="Comma-separated tags", blank=True)
    usage_frequency = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Very High'),
        (5, 'Critical'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    priority_score = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_completed = models.BooleanField(default=False)  # Optional, if you want a quick toggle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContextEntry(models.Model):
    SOURCE_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('notes', 'Notes'),
        ('other', 'Other'),
    ]

    content = models.TextField()
    processed_insights = models.TextField(blank=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
