"""View module for handling requests about practicePlans"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from practiceplanapi.models import PracticePlan, Player, Category
from django.db.models import Q

class PracticePlanView(ViewSet):
    """Practice Plan Practice Plans"""

    def create(self, request):
        """Handle POST operations to create a practice plan
        Returns:
            Response -- JSON serialized practice plan instance
        """
        player = Player.objects.get(user=request.auth.user)

        practice_plan = PracticePlan()
        practice_plan.title = request.data["title"]
        practice_plan.description = request.data["description"]
        practice_plan.player = player

        try:
            practice_plan.save()
            practice_plan.exercises.set([exercise["id"] for exercise in request.data["exercises"]])
            serializer = PracticePlanSerializer(practice_plan, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single practice plan

        Returns:
            Response -- JSON serialized practice plan instance
        """
        try:
            practice_plan = PracticePlan.objects.get(pk=pk)

            serializer = PracticePlanSerializer(practice_plan, context={'request': request})
            return Response(serializer.data)

        except PracticePlan.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a practice plan
        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)

        practice_plan = PracticePlan.objects.get(pk=pk)
        practice_plan.title = request.data["title"]
        practice_plan.description = request.data["description"]
        practice_plan.player = player
        practice_plan.save()
        practice_plan.exercises.set([exercise["id"] for exercise in request.data["exercises"]])

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single practice plan
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            practice_plan = PracticePlan.objects.get(pk=pk)
            practice_plan.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PracticePlan.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to practice plans resource
        Returns:
            Response -- JSON serialized list of practice plans
        """
        practice_plans = PracticePlan.objects.filter(Q(player__user=request.auth.user) | Q(player__is_public=1))

        # Show whether user signed in created practice plan
        for practice_plan in practice_plans:
            if practice_plan.player.user == request.auth.user:
                practice_plan.is_creator = True
            else:
                practice_plan.is_creator = False

        search_text = self.request.query_params.get('q', None)
        user_data = self.request.query_params.get('isUser', None)

        # If there is content in the search bar, filter practice plans by input text
        if search_text is not None:
            practice_plans = practice_plans.filter(Q(title__contains=search_text))
            for pratice_plan in practice_plans:
                if pratice_plan.player.user == request.auth.user:
                    pratice_plan.is_creator = True
                else:
                    pratice_plan.is_creator = False
        
        # If checkbox is clicked, show only the current user's practice plans
        if user_data != "" or None:
            practice_plans = practice_plans.filter(Q(player__user=request.auth.user))
            for practice_plan in practice_plans:
                if practice_plan.player.user == request.auth.user:
                    practice_plan.is_creator = True
                else:
                    practice_plan.is_creator = False

        serializer = PracticePlanSerializer(
            practice_plans, many=True, context={'request': request})
        return Response(serializer.data)
        

class PracticePlanSerializer(serializers.ModelSerializer):
    """JSON serializer for practicePlans

    Arguments:
        serializer type
    """
    class Meta:
        model = PracticePlan
        fields = ('id',  'player', 'title', 'description', 'exercises', 'is_creator')
        depth = 3
