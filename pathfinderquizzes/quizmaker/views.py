from django.shortcuts import render, redirect
from .models import Quiz
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def create_quiz(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        quiz_category_id = request.POST.get('quiz_category_id')  # Assume you have a dropdown in your form
        # You need to validate and convert quiz_category_id to an integer or get the actual object before saving
        
        quiz = Quiz.objects.create(
            Title=title,
            Description=description,
            QuizCategory_id=quiz_category_id,  # This assumes you're passing the ID directly; adjust as needed
            CreatedBy=request.user,
            IsPublished=False  # or True, based on your form input
        )
        return redirect('some-view-name')  # Redirect to a new URL:
    return render(request, 'quizmaker/create_quiz.html', {})
