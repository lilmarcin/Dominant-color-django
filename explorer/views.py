from django.shortcuts import render
from .models import File, UploadedImage
from .utils import get_dominant_colors, is_color_light, save_image_from_url
from .forms import ImageUploadForm
import os

def index(request, folder_id=None):
    if folder_id:
        folder = File.objects.get(pk=folder_id)
        files = File.objects.filter(parent_folder=folder)
    else:
        folder = None
        files = File.objects.filter(parent_folder__isnull=True)

    return render(request, 'explorer/index.html', {'folder': folder, 'files': files})



def display_image(request):
    dominant_colors_with_lightness = []
    uploaded_image = None
    image_filepath = None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']

            image_filepath = os.path.join('uploads', 'temporary.png')
            with open(image_filepath, 'wb') as destination:
                for chunk in uploaded_image.chunks():
                    destination.write(chunk)

            num_colors = 5
            dominant_colors = get_dominant_colors(uploaded_image, num_colors)
            dominant_colors_with_lightness = [(color, int(percentage), is_color_light(color)) for color, percentage in dominant_colors]
            #print("Image URL:", uploaded_image)
            #print("Image filepath:", image_filepath)
    else:
        form = ImageUploadForm()

    return render(request, 'index.html', {'image_filepath': image_filepath, 'dominant_colors': dominant_colors_with_lightness, 'form': form})
