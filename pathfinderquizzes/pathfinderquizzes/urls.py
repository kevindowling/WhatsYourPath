from django.contrib import admin
from django.urls import path, include
from users.views import signup, profile, logout_view, regenerate_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quizmaker.urls')),  # Include quizmaker URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/profile/', profile, name='profile'),
    path('regenerate_token', regenerate_token, name='regenerate_token'),
    path('logout/', logout_view, name='logout'),
    path('quizzes/', include('quizzes.urls')),
]

