from django.contrib import admin
from .models import AgentProfile, Conversation, Message, StructuredOutput, AgentResponse, PromptTemplate, UserSettings, Feedback

@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'agent', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')
    search_fields = ('user__username', 'agent__name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'timestamp')
    list_filter = ('sender',)
    search_fields = ('conversation__user__username',)

@admin.register(StructuredOutput)
class StructuredOutputAdmin(admin.ModelAdmin):
    list_display = ('message',)
    search_fields = ('message__conversation__user__username',)

@admin.register(AgentResponse)
class AgentResponseAdmin(admin.ModelAdmin):
    list_display = ('message',)
    search_fields = ('message__conversation__user__username',)

@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_name',)
    search_fields = ('template_name',)

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('message', 'rating')
    list_filter = ('rating',)
    search_fields = ('message__conversation__user__username',)
