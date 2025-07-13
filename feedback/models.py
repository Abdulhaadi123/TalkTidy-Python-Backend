from django.db import models

# Create your models here.

class PresentationFeedback(models.Model):
    content = models.TextField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(max_length=10, choices=[
        ('text', 'Text'),
        ('file', 'File')
    ])
    file_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Feedback {self.id} - {self.created_at}"
