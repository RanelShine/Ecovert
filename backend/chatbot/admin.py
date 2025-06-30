# chatbot/admin.py
from django.contrib import admin
from .models import Conversation, Message  # Mise à jour de l'importation

# Admin pour Conversation
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'started_at']
    search_fields = ['user__username']

admin.site.register(Conversation, ConversationAdmin)

# Admin pour Message
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'content', 'created_at']
    search_fields = ['content']

admin.site.register(Message, MessageAdmin)
