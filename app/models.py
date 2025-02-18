from django.db import models
from django.contrib.auth.models import AbstractUser

class DroneUser(AbstractUser):
    

    # Basic Information
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    address = models.CharField(max_length=255, verbose_name="Address")
    contact_no = models.CharField(max_length=15, verbose_name="Contact No")
    email = models.EmailField(verbose_name="Email")
    drone_experience = models.TextField(verbose_name="Your Drone Related Experience")

    # Citizenship Upload
    citizenship_upload = models.FileField(upload_to='citizenship/', blank=True, null=True, verbose_name="Upload Citizenship")

    # Involvement Type
    INVOLVEMENT_CHOICES = [
        ('individual', 'Individual / Freelancer'),
        ('organizational', 'Organizational'),
    ]
    involvement_type = models.CharField(max_length=20, blank=True,null=True, choices=INVOLVEMENT_CHOICES, verbose_name="Involved as Organizational or Individual")

    # Organizational Details (conditional fields)
    organization_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Involved Organization Name")
    organization_weblink = models.URLField(blank=True, null=True, verbose_name="Organization Weblink")
    organization_social_media_link = models.URLField(blank=True, null=True, verbose_name="Organization Social Media Link")
    regd_document_upload = models.FileField(upload_to='organization_docs/', blank=True, null=True, verbose_name="Regd Document Upload")

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Drone Enthusiast"
        
class ImageWithDetails(models.Model):
    # Title of the image
    title = models.CharField(max_length=255, verbose_name="Title")

    # Description of the image
    description = models.TextField(verbose_name="Description")

    # Image field to upload the image
    image = models.ImageField(upload_to='images/',blank=True, null=True, verbose_name="Image")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Image with Details"
        verbose_name_plural = "Images with Details"

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/', verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

    def __str__(self):
        return f"Gallery Image {self.id}"