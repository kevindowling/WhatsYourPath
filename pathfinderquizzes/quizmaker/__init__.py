from django.apps import AppConfig

class QuizMaker(AppConfig):
  name = 'quizmaker'  # Replace with your app's name

  def ready(self):
    from . import templatetags  # Import your templatetags module
    templatetags.register  # Call the register function from your module
