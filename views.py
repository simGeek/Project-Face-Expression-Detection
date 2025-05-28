import os
import cv2
import numpy as np
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageUploadForm  # make sure this exists
from keras.models import load_model
from mtcnn.mtcnn import MTCNN


def project3(request):
    return render(request, "project3.html")


def p3_clear_uploaded_images():
    # Define the directory where uploaded images are stored
    uploaded_images_directory = os.path.join(settings.MEDIA_ROOT, 'images')
    # Iterate through all files in the specified directory
    for filename in os.listdir(uploaded_images_directory):
        # Construct the full file path for each file
        file_path = os.path.join(uploaded_images_directory, filename)
        try:
            # Check if the path is a file (not a directory)
            if os.path.isfile(file_path):
                # Remove the file from the filesystem
                os.remove(file_path)
        except Exception as e:
            # Print an error message if file deletion fails
            print(f"Failed to delete {file_path}. Reason: {str(e)}")


def p3_clear_processed_images():
    # Define the directory where processed images are stored
    processed_images_directory = os.path.join(settings.MEDIA_ROOT, 'processed_images')
    # Iterate through all files in the specified directory
    for filename in os.listdir(processed_images_directory):
        # Construct the full file path for each file
        file_path = os.path.join(processed_images_directory, filename)
        try:
            # Check if the path is a file (not a directory)
            if os.path.isfile(file_path):
                # Remove the file from the filesystem
                os.remove(file_path)
        except Exception as e:
            # Print an error message if file deletion fails
            print(f"Failed to delete {file_path}. Reason: {str(e)}")


def p3_success(request):
    if request.method == 'GET':
        try:
            # Clear previously processed images
            p3_clear_processed_images()

            # Define the directory where uploaded images are stored
            images_directory = os.path.join(settings.MEDIA_ROOT, 'images')
            # List all files in the directory
            uploaded_images = os.listdir(images_directory)

            if uploaded_images:
                # Assuming processing the latest uploaded image
                latest_image_filename = uploaded_images[0]
                # Construct the full path to the latest uploaded image
                uploaded_image_path = os.path.join(images_directory, latest_image_filename)
                # Load the pre-trained model for face expression recognition
                model = load_model('ds_models/face_model.h5')
                class_names = ['ANGRY', 'DISGUST', 'FEAR', 'HAPPY', 'NEUTRAL', 'SAD', 'SURPRISE']

                # Initialize the MTCNN face detector
                mtcnn = MTCNN()
                # Read the image from the file path
                image = cv2.imread(uploaded_image_path)
                if image is None:
                    return JsonResponse({'error': 'Could not open or find the image'})

                # Prepare for face detection and recognition
                output_image = image.copy()
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                boxes, _ = mtcnn.detect(rgb_image)

                if boxes is not None:
                    labels = []
                    boxes = boxes.astype(int)
                    for (x, y, w, h) in boxes:
                        # Draw bounding boxes around detected faces
                        cv2.rectangle(output_image, (x, y), (w, h), (0, 255, 0), 2)
                        # Extract face from the image
                        face = image[y:h, x:w]
                        # Resize face to match model input size
                        resized_face = cv2.resize(face, (96, 96))
                        reshaped_face = np.expand_dims(resized_face, axis=0)
                        # Predict face expression
                        prediction = model.predict(reshaped_face)
                        expression = np.argmax(prediction)
                        label = f"{class_names[expression]}"
                        labels.append(label)
                        # Draw the predicted label on the image
                        cv2.putText(output_image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                    # Save the processed image to the 'processed_images' folder
                    processed_image_path = os.path.join(settings.MEDIA_ROOT, 'processed_images', latest_image_filename)
                    processed_image_url = os.path.join(settings.MEDIA_URL, 'processed_images', latest_image_filename)
                    # Write the output image to file
                    cv2.imwrite(processed_image_path, output_image)
                    # Remove the original uploaded image
                    os.remove(uploaded_image_path)

                    # Render the response with the processed image URL and labels
                    context = {'processed_image_url': processed_image_url, 'labels': labels}
                    response = render(request, 'p3face.html', context)
                    return response
                else:
                    # If no faces are detected, remove the uploaded image
                    os.remove(uploaded_image_path)
                    return JsonResponse({'error': 'No faces detected'}, status=404)
            else:
                # If no uploaded images are found, return a 404 error
                return JsonResponse({'error': 'No uploaded images found'}, status=404)

        except Exception as e:
            # In case of an exception, remove the uploaded image (if it exists)
            if 'uploaded_image_path' in locals():
                os.remove(uploaded_image_path)
            print("Error:", str(e))
            return JsonResponse({'error': 'An error occurred while processing the image'}, status=500)
    else:
        # If the request method is not GET, return a 405 error
        if 'uploaded_image_path' in locals():
            os.remove(uploaded_image_path)
        return JsonResponse({'error': 'Invalid method'}, status=405)


def p3_imageUpload(request):
    # Clear previously uploaded images
    p3_clear_uploaded_images()

    # Check if the request method is POST
    if request.method == 'POST':
        # Create a form instance with POST data and uploaded files
        form = ImageUploadForm(request.POST, request.FILES)

        # Validate the form
        if form.is_valid():
            # Save the form data (i.e., the uploaded image)
            form.save()

            # Redirect to the 'p3_success' view upon successful upload
            return redirect('p3_success')
        else:
            # Print form validation errors to the console
            print("Form is not valid")
            print(form.errors)
    else:
        # For GET requests or other methods, instantiate a new empty form
        form = ImageUploadForm()

    # Render the 'project3.html' template with the form instance
    return render(request, 'project3.html', {'form': form})
