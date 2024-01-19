# Importing necessary modules from Django
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

# Function to define the upload path for server icons
def server_icon_upload_path(instance, filename):
    return f"server/{instance.id}/server_icons/{filename}"

# Function to define the upload path for server banners
def server_banner_upload_path(instance, filename):
    return f"server/{instance.id}/server_banner/{filename}"

# Function to define the upload path for category icons
def category_icon_upload_path(instance, filename):
    return f"category/{instance.id}/category_icon/{filename}"

# Model representing a Category
class Category(models.Model):
    # Fields for the Category model
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=category_icon_upload_path,
        null=True,
        blank=True,
    )
    
    # Custom save method to delete old icon file when updating
    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
                super(Category, self).save(*args, **kwargs)

    # Signal to delete associated files when a Category instance is deleted
    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)
                
    # String representation of the Category instance
    def __str__(self):
        return self.name

# Model representing a Server
class Server(models.Model):
    # Fields for the Server model
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="server_category")
    description = models.CharField(max_length=250, blank=True, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)
    
    # String representation of the Server instance
    def __str__(self):
        return f"{self.name}-{self.id}"

# Model representing a Channel
class Channel(models.Model):
    # Fields for the Channel model
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner")
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channel_server")
    banner = models.ImageField(upload_to=server_banner_upload_path, null=True, blank=True)
    icon = models.ImageField(upload_to=server_icon_upload_path, null=True, blank=True)
    
    # Custom save method to delete old icon and banner files when updating
    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    # Signal to delete associated files when a Channel instance is deleted
    @receiver(models.signals.pre_delete, sender="server.Channel")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)
    
    # String representation of the Channel instance
    def __str__(self):
        return self.name
