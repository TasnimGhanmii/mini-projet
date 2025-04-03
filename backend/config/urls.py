from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('surveillance_api.urls')),

    # Include the app's URLs
]
