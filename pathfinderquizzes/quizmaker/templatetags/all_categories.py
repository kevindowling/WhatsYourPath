from django import template

from ..models import QuizCategory

register = template.Library()

@register.simple_tag
def get_all_categories():
  """
  Fetches all quiz categories
  """
  print(QuizCategory.objects.all())
  return QuizCategory.objects.all()