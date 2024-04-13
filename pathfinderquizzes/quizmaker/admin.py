from django.contrib import admin
from .models import QuizCategory, Quiz, Question, Answer, AnswerAttribute, UserQuizAttempt, UserAnswer, AttributeThreshold, OutcomeCode

admin.site.register(QuizCategory)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerAttribute)
admin.site.register(UserQuizAttempt)
admin.site.register(UserAnswer)
admin.site.register(AttributeThreshold)
admin.site.register(OutcomeCode)