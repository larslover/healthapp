from django.contrib import admin
from django.urls import path, include
from core.views import service_worker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # dashboard, main pages

    # PWA service worker (must NOT be inside its own include)
    path("service-worker.js", service_worker, name="service-worker"),
]
