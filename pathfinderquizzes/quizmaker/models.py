from django.db import models
from users.models import CustomUser as User


class QuizCategory(models.Model):
    QuizCategoryID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField(null=True, blank=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.Name

class Quiz(models.Model):
    QuizID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    QuizCategory = models.ForeignKey(QuizCategory, on_delete=models.CASCADE)
    CreatedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)
    IsPublished = models.BooleanField(default=False)
    def __str__(self):
        return self.Title

class Question(models.Model):
    QuestionID = models.AutoField(primary_key=True)
    Quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    Text = models.CharField(max_length=255)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    QuestionType = models.CharField(max_length=50)
    Sequence = models.IntegerField()
    def __str__(self) -> str:
        return self.Text

class Answer(models.Model):
    AnswerID = models.AutoField(primary_key=True)
    Question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    Text = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.Text

class AnswerAttribute(models.Model):
    AttributeID = models.AutoField(primary_key=True)
    Answer = models.ForeignKey(Answer, related_name='attributes', on_delete=models.CASCADE)
    AttributeName = models.CharField(max_length=255)
    Weight = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self) -> str:
        return f'Attribute: {self.AttributeName} weighted: {self.Weight} for Answer: {self.Answer}'

class UserQuizAttempt(models.Model):
    AttemptID = models.AutoField(primary_key=True)
    Quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    StartedAt = models.DateTimeField()
    CompletedAt = models.DateTimeField(null=True, blank=True)
    def __str__(self) -> str:
        return f'User: {self.User} attempt at {self.CompletedAt}'

class UserAnswer(models.Model):
    UserAnswerID = models.AutoField(primary_key=True)
    Attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE)
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)
    Answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    AnsweredAt = models.DateTimeField()
    def __str__(self) -> str:
        return f'Question {self.Question} answered with {self.Answer} at {self.AnsweredAt}'

class AttributeThreshold(models.Model):
    AttributeThresholdID = models.AutoField(primary_key=True)
    Quiz = models.ForeignKey(Quiz, related_name='attributethresholds', on_delete=models.CASCADE)
    AttributeName = models.CharField(max_length=255)
    ThresholdValue = models.DecimalField(max_digits=5, decimal_places=2)
    Description = models.TextField(null=True, blank=True)
    GradingInstruction = models.TextField()
    LeftCodeString = models.CharField(max_length=255, default='', help_text="Code for the left side of the threshold")
    RightCodeString = models.CharField(max_length=255, default='', help_text="Code for the right side of the threshold")

    def __str__(self) -> str:
        return f'{self.AttributeName} threshold: {self.ThresholdValue}'

class OutcomeCode(models.Model):
    OutcomeCodeID = models.AutoField(primary_key=True)
    Quiz = models.ForeignKey(Quiz, related_name='outcomecodes', on_delete=models.CASCADE)
    CombinationCode = models.CharField(max_length=255, default='', help_text="A code representing the combination of attribute thresholds")
    Description = models.TextField(help_text="A detailed description of what this combination means")
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.CombinationCode}: {self.Description}'
