from django import forms

class ImageUploadForm(forms.Form):
    image_name = forms.CharField(max_length=255, required=False)
    image = forms.ImageField()