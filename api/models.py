from django.db import models

# Create your models here.
from django.urls import reverse


class Resume(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    resume = models.FileField(upload_to='files',blank=True)
    text = models.TextField(null=True)
    name = models.CharField(null=True , max_length = 255)
    phone = models.TextField(null=True)
    email = models.CharField(null=True , max_length = 255)
    skills = models.TextField(null=True)
    designation = models.TextField(null=True)
    degree = models.TextField(null=True)
    college = models.TextField(null=True)
    experience = models.TextField(null=True)
    is_parsed = models.BooleanField(default=False)
    # def get_absolute_url(self):
    #     return reverse('web-detail', kwargs={'pk': self.pk})
    