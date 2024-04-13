from django.shortcuts import get_object_or_404, render, redirect
from .models import Quiz, QuizCategory, AnswerAttribute, AttributeThreshold, Question, Answer
from django.contrib.auth.decorators import login_required
import logging
from django.http import HttpResponse
from django.contrib import messages

logger = logging.getLogger('myapp.custom')

@login_required
def create_quiz(request):
    categories = QuizCategory.objects.all()
    context = {'categories': categories}
    if request.method == 'POST':
        logger.debug("Create Quiz: POST")
        title = request.POST.get('title')
        description = request.POST.get('description')
        quiz_category_id = request.POST.get('quiz_category_id')
        is_published = request.POST.get('is_published') == 'true'
        quiz = Quiz.objects.create(
            Title=title,
            Description=description,
            QuizCategory_id=quiz_category_id,  
            CreatedBy=request.user,
            IsPublished=is_published
        )        
        categories = QuizCategory.objects.all()
        context['quiz_id']= quiz.pk
        logger.debug('Quiz ID passed from create quiz: %s', quiz.pk)
        return render(request, 'quizmaker/add_attribute_threshold.html', context)
    else:
        return render(request, 'quizmaker/create_quiz.html')

@login_required
def submit_attribute_thresholds(request):
    if request.method == 'POST':
        quiz_id = request.POST.get('quiz_id')
        logger.debug('Quiz ID recieved from create quiz: %s', quiz_id)
        quiz = Quiz.objects.get(pk=quiz_id)
        attribute_names_codes = []
        for key in request.POST:
            if key.startswith('attribute_name'):
                index = key[len('attribute_name'):]  # Extract the counter value from the key
                attribute_name = request.POST.get(key)
                threshold_value = request.POST.get(f'attribute_threshold{index}')
                left_code_string = request.POST.get(f'left_code_string{index}')
                right_code_string = request.POST.get(f'right_code_string{index}')   
                description = request.POST.get(f'threshold_description{index}')
                if attribute_name and threshold_value:
                    AttributeThreshold.objects.create(
                        Quiz=quiz,
                        AttributeName=attribute_name,
                        ThresholdValue=threshold_value,
                        Description=description,
                        GradingInstruction='',  # [FUTURE]
                        LeftCodeString=left_code_string,
                        RightCodeString=right_code_string,
                    )
                    attribute_names_codes.append([attribute_name, left_code_string, right_code_string])
                    

        context = {
            'quiz_id': quiz.pk,
            'attribute_names_codes': attribute_names_codes}
        return render(request, 'quizmaker/add_outcome_codes.html', context)
    else:
        return redirect('create_quiz')

@login_required 
def submit_outcome_codes(request):
    if request.method == 'POST':
        quiz_id = request.POST.get('quiz_id')
        #quiz = Quiz.objects.get(pk=quiz_id)

        #Create OutcomeCode Objects.
    return redirect('quizmaker/add_questions.html', { 'quiz_id': quiz_id }) 

@login_required
def submit_questions(request):

 
    if request.method == 'POST':

        quiz_id = request.POST.get('quiz_id')
        # Ensure quiz exists, otherwise redirect with an error message
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        attribute_thresholds = AttributeThreshold.objects.filter(Quiz=quiz)
        attribute_names = [at.AttributeName for at in attribute_thresholds]
        context = {
            'quiz_id': quiz.pk,
            # Include other context variables as necessary
        }
        question_fields = [key for key in request.POST if key.startswith('question_text')]
        for q_index, q_field in enumerate(question_fields, start=1):  # Enumerate for Sequence
            question_text = request.POST.get(q_field)
            if question_text:  
                question_type = "default_type"  # Adjust as necessary, maybe based on another form field
                sequence = q_index  # Use enumeration index as sequence
                
                question = Question.objects.create(
                    Quiz=quiz, 
                    Text=question_text, 
                    QuestionType=question_type, 
                    Sequence=sequence
                )
                
                # Loop through answers for this question
                for a_index in range(1, 7):  # Assuming up to 6 answers per question
                    answer_text = request.POST.get(f'answer_text{q_index}_{a_index}', None)
                    answer_attribute_name = request.POST.get(f'answer_attribute{q_index}_{a_index}', None)
                    answer_weight = request.POST.get(f'answer_weight{q_index}_{a_index}', None)
                    if answer_text:
                        answer = Answer.objects.create(Question=question, Text=answer_text)
                        if answer_attribute_name and answer_weight:
                            attribute_threshold = AttributeThreshold.objects.filter(AttributeName=answer_attribute_name, Quiz=quiz).first()
                            if attribute_threshold:
                                AnswerAttribute.objects.create(
                                    Answer=answer,
                                    AttributeName=answer_attribute_name,
                                    Weight=answer_weight  # Use the retrieved weight value
                                )
        messages.success(request, 'Questions and answers submitted successfully!')
        return redirect('create_quiz')  # Adjust the redirect as necessary

    else:
        return redirect('create_quiz')