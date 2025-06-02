🔹PROJECT-FACE-EXPRESSION-DETECTION🔹

◽LINKEDIN POST◽

<LINK>

1️⃣ PURPOSE

To detect face expressions on a human face. 

2️⃣ DESCRIPTION

The user uploads a picture with one or more human beings with visible faces. The model detects the face and the expression among the following emotions:

1. Happy
2. Sad
3. Neutral
4. Disgust
5. Surprise
6. Fear
7. Angry

3️⃣ TECH STACK

🔹Frontend: HTML, JS, CSS

🔹Backend: Python, Deep Learning, Computer Vision, Django

🔹Infrastructure: AWS

4️⃣ LIBRARIES OR MODULES USED:

🔹 os

🔹 cv2

🔹 np

🔹 keras

🔹 mtcnn

🔹 numpy

🔹 shutil

🔹 random

🔹 django

🔹 imgaug

🔹 imageio

🔹 tensorflow

🔹 matplotlib

5️⃣ WORKFLOW

🔹INPUT: The user uploads an image consisting of one or more human faces.

🔹PROCESSING: Firstly, the human faces are spotted (MTCNN) followed by their expression detection (ResNet50 + CNN).

🔹RESULT: The final processed image is displayed with red bounding boxes around identified human faces along with the name of the expression they show.

6️⃣ INSTALLATION (with VS Code)

🔹Install:

VS Code (https://code.visualstudio.com/download)

Python (https://www.python.org/downloads/release/python-3100/)

Click on - Windows installer (64-bit)

Make sure to add it in the path

🔹Open VS Code

🔹Click on 'Clone Git Repository' and paste 'https://github.com/simGeek/Project-Face-Expression-Detection.git' in the space prompted for the git url

🔹Hit 'Enter' and select a folder locally where to include the project files; open the folder in VS Code

🔹Open Terminal > New Terminal

🔹Run following commands:

py -3.10 -m venv venv   

venv\Scripts\activate

pip install -r requirements.txt

🔹Run following commands:

django-admin startproject my_project

cd my_project

python manage.py startapp home

🔹Delete 'views.py' from 'home'; cut and paste 'urls.py' and 'views.py' from the cloned files to 'home'

🔹Create new folders inside the outer 'my_project' named 'templates' and 'static'

🔹Create new folder named 'css' inside 'static'

🔹Create new folder 'ds_models' inside outer 'my_project'

🔹Cut and paste the following to the respective folders:

.html files --> templates

.css files --> css inside static

.png files --> images inside static

🔹Add the following in settings.py inside inner 'my_project' (make sure to add after the BASE_DIR variable definition):

import os

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

🔹Inside settings.py --> 'INSTALLED_APPS', include 'home'

🔹Inside settings.py --> 'TEMPLATES', paste 'os.path.join(BASE_DIR, 'templates')' in DIRS = [PASTE HERE]

🔹Add in inner 'my_project' --> 'urls.py' (remove everything there and paste the following),

from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [

path('admin/', admin.site.urls),

path('', include('home.urls')),

]

🔹Drive link to download the model:

https://drive.google.com/file/d/1yNgOGq9GQL60p2byW5Hw-xHvC-y4ApAD/view?usp=drive_link

🔹After downloading the model, save it inside 'ds_models'

🔹Create a file forms.py inside 'home' and add the following:

# home/forms.py

from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

🔹Make sure to save all the changes by saving each modified file side by side (ctrl + s).

🔹Ctrl+Shift+P -> Reload Window (to reflect all the installed modules)

🔹Run 'python manage.py migrate' in the VS Code terminal

🔹Run 'python manage.py runserver' in the VS Code terminal

🔹Copy and paste the given link from the output terminal (http://127.0.0.1:8000/) in the browser

🔹Link to the Kaggle Dataset:

https://www.kaggle.com/datasets/jonathanoheix/face-expression-recognition-dataset

7️⃣ CHALLENGES

🔹Model Training

🔹Data Augmentation

8️⃣ KEY LEARNINGS AND SKILLS

🔹Python

🔹Deep Learning

🔹Data Augmentation

🔹Transfer learning (ResNet50)

🔹Convolutional Neural Networks (CNN)

🔹Multi-task Cascaded Convolutional Neural Networks (MTCNN)

9️⃣ DEPLOYED PROJECT IMAGES

![p3-1](https://github.com/user-attachments/assets/ea85353d-5836-42e5-9560-19dfb911db7f)

![p3-2](https://github.com/user-attachments/assets/c3c8f863-bf4e-4e7e-9e3b-7305dfe9d267)
