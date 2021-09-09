"""View module for handling requests about players"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from practiceplanapi.models import Player

class PlayerView(ViewSet):
    """Practice Plan Players"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single player
        Returns:
            Response -- JSON serialized player instance
        """
        try:

            player = Player.objects.get(pk=pk)
            serializer = PlayerSerializer(player, context={'request': request})
            return Response(serializer.data)

        except Player.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to categories resource
        Returns:
            Response -- JSON serialized list of categories
        """
        players = Player.objects.all()

        serializer = PlayerSerializer(
            players, many=True, context={'request': request})
        return Response(serializer.data)
        

class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for players

    Arguments:
        serializer type
    """
    class Meta:
        model = Player
        fields = ('id', 'user', 'practice_focus', 'bio', 'is_public')
        depth = 1