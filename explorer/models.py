from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    is_folder = models.BooleanField(default=False)
    parent_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class UploadedImage(models.Model):
    image_url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_url