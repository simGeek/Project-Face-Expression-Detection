from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.project_landing_page, name='project_landing_page'),
    path("imageUpload", views.imageUpload, name='imageUpload'),
    path("success", views.success, name='success')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
