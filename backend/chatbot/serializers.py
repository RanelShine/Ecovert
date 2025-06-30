from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'image', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  # Inclure les messages associés

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'started_at', 'messages']
        read_only_fields = ['started_at']
