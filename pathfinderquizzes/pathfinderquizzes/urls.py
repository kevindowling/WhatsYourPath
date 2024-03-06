from django.contrib import admin
from django.urls import path, include  # Import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quizmaker.urls')),  # Include quizmaker URLs
    path('accounts/', include('django.contrib.auth.urls')),
]
