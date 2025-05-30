import os
import cv2
import numpy as np
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageUploadForm
from tensorflow import keras 
from mtcnn.mtcnn import MTCNN


def project_landing_page(request):
    return render(request, "project_landing_page.html")


def clear_uploaded_images():
    uploaded_images_directory = os.path.join(settings.MEDIA_ROOT, 'images')
    for filename in os.listdir(uploaded_images_directory):
        file_path = os.path.join(uploaded_images_directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {str(e)}")


def clear_processed_images():
    processed_images_directory = os.path.join(settings.MEDIA_ROOT, 'processed_images')
    for filename in os.listdir(processed_images_directory):
        file_path = os.path.join(processed_images_directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {str(e)}")


def success(request):
    if request.method == 'GET':
        try:
            clear_processed_images()
            images_directory = os.path.join(settings.MEDIA_ROOT, 'images')
            uploaded_images = os.listdir(images_directory)

            if uploaded_images:
                latest_image_filename = uploaded_images[0]
                uploaded_image_path = os.path.join(images_directory, latest_image_filename)
                model = keras.models.load_model('ds_models/face_model.h5')
                class_names = ['ANGRY', 'DISGUST', 'FEAR', 'HAPPY', 'NEUTRAL', 'SAD', 'SURPRISE']
                mtcnn = MTCNN()
                image = cv2.imread(uploaded_image_path)
                if image is None:
                    return JsonResponse({'error': 'Could not open or find the image'})

                output_image = image.copy()
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                detections = mtcnn.detect_faces(rgb_image)

                if detections:
                    labels = []
                    for detection in detections:
                        x, y, w, h = detection['box']
                        x, y = max(0, x), max(0, y)
                        face = image[y:y+h, x:x+w]
                        if face.size == 0:
                            continue
                        resized_face = cv2.resize(face, (96, 96))
                        reshaped_face = np.expand_dims(resized_face, axis=0)
                        prediction = model.predict(reshaped_face)
                        expression = np.argmax(prediction) 
                        label = f"{class_names[expression]}"
                        labels.append(label)
                        cv2.rectangle(output_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(output_image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    processed_image_path = os.path.join(settings.MEDIA_ROOT, 'processed_images', latest_image_filename)
                    processed_image_url = os.path.join(settings.MEDIA_URL, 'processed_images', latest_image_filename)
                    cv2.imwrite(processed_image_path, output_image)
                    os.remove(uploaded_image_path)
                    context = {'processed_image_url': processed_image_url, 'labels': labels}
                    response = render(request, 'output.html', context)
                    return response
                else:
                    os.remove(uploaded_image_path)
                    return JsonResponse({'error': 'No faces detected'}, status=404)
            else:
                return JsonResponse({'error': 'No uploaded images found'}, status=404)

        except Exception as e:
            if 'uploaded_image_path' in locals():
                os.remove(uploaded_image_path)
            print("Error:", str(e))
            return JsonResponse({'error': 'An error occurred while processing the image'}, status=500)
    else:
        if 'uploaded_image_path' in locals():
            os.remove(uploaded_image_path)
        return JsonResponse({'error': 'Invalid method'}, status=405)


def imageUpload(request):
    clear_uploaded_images()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = ImageUploadForm()

    return render(request, 'project_landing_page.html', {'form': form})
