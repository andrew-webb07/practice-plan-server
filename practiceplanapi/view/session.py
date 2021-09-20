"""View module for handling requests about sessions"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from practiceplanapi.models import Session, Player, PracticePlan
from django.db.models import Q

class SessionView(ViewSet):
    """Practice Plan Sessions"""

    def create(self, request):
        """Handle POST operations for creating a session
        Returns:
            Response -- JSON serialized session instance
        """
        player = Player.objects.get(user=request.auth.user)

        session = Session()
        session.length_of_session = request.data["lengthOfSession"]
        session.date = request.data["date"]
        session.player = player
        session.notes = request.data["notes"]

        practice_plan = PracticePlan.objects.get(pk=request.data["practicePlanId"])
        session.practice_plan = practice_plan

        try:
            session.save()
            serializer = SessionSerializer(session, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single session

        Returns:
            Response -- JSON serialized session instance
        """
        try:

            session = Session.objects.get(pk=pk)

            serializer = SessionSerializer(session, context={'request': request})
            return Response(serializer.data)

        except Session.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a session
        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)

        session = Session.objects.get(pk=pk)
        session.length_of_session = request.data["lengthOfSession"]
        session.date = request.data["date"]
        session.player = player
        session.notes = request.data["notes"]

        practice_plan = PracticePlan.objects.get(pk=request.data["practicePlanId"])
        session.practice_plan = practice_plan
        session.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single session
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            session = Session.objects.get(pk=pk)
            session.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Session.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to sessions resource
        Returns:
            Response -- JSON serialized list of sessions
        """
        sessions = Session.objects.filter(player__user=request.auth.user)

        serializer = SessionSerializer(
            sessions, many=True, context={'request': request})
        return Response(serializer.data)
        

class SessionSerializer(serializers.ModelSerializer):
    """JSON serializer for sessions

    Arguments:
        serializer type
    """
    class Meta:
        model = Session
        fields = ('id', 'player', 'practice_plan', 'length_of_session', 'date', 'notes', 'length_of_each_exercise')
        depth = 2
