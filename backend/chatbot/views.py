from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ConversationSerializer
from .chatbot_logic import my_chat
from .models import Conversation, Message
from PIL import Image
import io

class ChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get(self, request):
        """Récupérer l'historique des conversations de l'utilisateur."""
        conversations = Conversation.objects.filter(user=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Envoyer un message au chatbot et obtenir une réponse."""
        message_content = request.data.get('message')
        image_file = request.FILES.get('image')

        if not message_content:
            return Response({'error': 'Message is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Créer une nouvelle conversation
        conversation = Conversation.objects.create(user=request.user)

        # Enregistrer le message de l'utilisateur
        message = Message.objects.create(
            conversation=conversation,
            sender='user',
            content=message_content
        )

        # Traiter l'image si elle est présente
        img = None
        if image_file:
            try:
                img = Image.open(io.BytesIO(image_file.read()))
            except Exception as e:
                return Response({'error': f'Invalid image file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtenir la réponse du chatbot
        response_content = my_chat(message_content, img)

        # Enregistrer la réponse du chatbot
        Message.objects.create(
            conversation=conversation,
            sender='bot',
            content=response_content
        )

        # Sérialiser et retourner la réponse de la conversation
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)