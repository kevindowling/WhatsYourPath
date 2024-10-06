from django.db import models
from django.conf import settings
from pydantic import ValidationError
from .structured_output_schema import StructuredOutputSchema
import logging

logger = logging.getLogger('myapp.custom')

class AgentProfile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    personality_settings = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Conversation between {self.user} and {self.agent} started at {self.start_time}"


class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('agent', 'Agent'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=5, choices=SENDER_CHOICES)
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"


class StructuredOutput(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='structured_output')
    output_data = models.JSONField()  # Stores validated structured output
    logger.debug("You're entering into StructuredOutput model")

    @classmethod
    def create_validated(cls, message, data):
        logger.debug("You're entering into StructuredOutput model create_validated function")
        try:
            # Validate using Pydantic
            validated_data = StructuredOutputSchema.model_validate(data)
            # Create and save the StructuredOutput instance
            instance = cls.objects.create(
                message=message,
                output_data=validated_data.model_dump()
            )
            return instance
        except ValidationError as e:
            # Handle validation errors as needed
            print(f"Validation error: {e}")
            return None

    def __str__(self):
        return f"Structured output for message {self.message.id}"


class AgentResponse(models.Model):
    message = models.OneToOneField(Message, on_delete=models.CASCADE, related_name='response')
    response_data = models.JSONField()

    def __str__(self):
        return f"Response for message {self.message.id}"


class PromptTemplate(models.Model):
    template_name = models.CharField(max_length=255)
    template_text = models.TextField()

    def __str__(self):
        return self.template_name


class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    settings_data = models.JSONField()

    def __str__(self):
        return f"Settings for {self.user}"


class Feedback(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveIntegerField()
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Feedback for message {self.message.id} with rating {self.rating}"
