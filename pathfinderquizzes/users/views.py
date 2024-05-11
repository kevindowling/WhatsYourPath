# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Or another appropriate redirect
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    token, _ = Token.objects.get_or_create(user=request.user)  # Create if not exist

    return render(request, 'users/profile.html', {'token': token.key})

def regenerate_token(request):
    Token.objects.filter(user=request.user).delete()  # Delete the old token
    Token.objects.create(user=request.user)  # Create a new token
    return redirect('profile')  # Redirect back to the profile page

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('login')