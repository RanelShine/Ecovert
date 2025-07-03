#chatot/models.py
from django.conf import settings # Add this import
from django.db import models


# Conversation
class Conversation(models.Model):
    # Change this line:
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation {self.id} by {self.user.username}'


# Message
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=10)  # 'user' ou 'bot'
    content = models.TextField()
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.content[:50]}'