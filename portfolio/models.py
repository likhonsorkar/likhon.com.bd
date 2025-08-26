from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/')
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    client_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.IntegerField(default=5) # e.g., 1-5 stars
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.client_name}"