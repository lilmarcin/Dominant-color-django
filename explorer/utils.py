from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import os
import requests

def is_color_light(rgb):
    r, g, b = rgb
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return brightness > 127



def save_image_from_url(image_url):
    filename = os.path.basename(image_url)
    filepath = os.path.join('media', 'uploaded_images', filename)

    response = requests.get(image_url)
    
    with open(filepath, 'wb') as out_file:
        out_file.write(response.content)

    return filepath

def get_dominant_colors(image_path, num_colors):
    image = Image.open(image_path)
    image = image.convert("RGB")

    image_array = np.array(image)

    flattened_array = image_array.reshape(-1, 3)

    # Wykorzystanie algorytmu k-means do grupowania pikseli
    kmeans = KMeans(n_clusters=num_colors, n_init=10)
    kmeans.fit(flattened_array)

    # Uzyskanie etykiet klastrów
    labels = kmeans.labels_

    # Zliczenie wystąpień etykiet
    label_counts = Counter(labels)

    # Sortowanie etykiet według liczby wystąpień
    sorted_labels = sorted(label_counts, key=lambda x: label_counts[x], reverse=True)

    # Uzyskanie centrum klastrów
    cluster_centers = kmeans.cluster_centers_

    # Obliczenie udziału procentowego dla każdego koloru
    total_pixels = flattened_array.shape[0]
    colors_percentages = [(label_counts[i] / total_pixels) * 100 for i in sorted_labels]

    # Uzyskanie dominujących kolorów
    dominant_colors = [cluster_centers[i] for i in sorted_labels]

    # Konwersja wartości kolorów do typu całkowitoliczbowego
    dominant_colors = [tuple(map(int, color)) for color in dominant_colors]

    # Zwrócenie listy dominujących kolorów wraz z ich udziałem procentowym
    result = [(color, int(percentage)) for color, percentage in zip(dominant_colors, colors_percentages)]
    return result[:5]

