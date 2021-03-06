"""View module for handling requests about exercises"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from practiceplanapi.models import Exercise, Player, Category
from django.core.files.base import ContentFile
import base64
import uuid
from django.db.models import Q

class ExerciseView(ViewSet):
    """Practice Plan Exercises"""

    def create(self, request):
        """Handle POST operations for an exercise
        Returns:
            Response -- JSON serialized exercise instance
        """
        player = Player.objects.get(user=request.auth.user)

        exercise = Exercise()
        exercise.title = request.data["title"]
        exercise.description = request.data["description"]
        exercise.player = player
        if request.data["examplePicture"] != "":
            format, imgstr = request.data["examplePicture"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["title"]}-{uuid.uuid4()}.{ext}')
            exercise.example_picture = data

        exercise_category = Category.objects.get(pk=request.data["categoryId"])
        exercise.category = exercise_category

        try:
            exercise.save()
            serializer = ExerciseSerializer(exercise, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single exercise

        Returns:
            Response -- JSON serialized exercise instance
        """
        try:
            exercise = Exercise.objects.get(pk=pk)
            serializer = ExerciseSerializer(exercise, context={'request': request})
            return Response(serializer.data)

        except Exercise.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a exercise

        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)

        exercise = Exercise.objects.get(pk=pk)
        exercise.title = request.data["title"]
        exercise.player = player
        exercise.description = request.data["description"]
        if request.data["examplePicture"] != "":
            format, imgstr = request.data["examplePicture"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["title"]}-{uuid.uuid4()}.{ext}')
            exercise.example_picture = data
        else:
            exercise.example_picture = ""

        exercise_category = Category.objects.get(pk=request.data["categoryId"])
        exercise.category = exercise_category
        exercise.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single exercise
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            exercise = Exercise.objects.get(pk=pk)
            exercise.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exercise.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to exercises resource
        Returns:
            Response -- JSON serialized list of exercises
        """
        exercises = Exercise.objects.filter(Q(player__user=request.auth.user) | Q(player__is_public=1))

        # Show whether user signed in created exercise
        for exercise in exercises:
            if exercise.player.user == request.auth.user:
                exercise.is_creator = True
            else:
                exercise.is_creator = False

        search_text = self.request.query_params.get('q', None)
        category_text = self.request.query_params.get('category', None)
        user_data = self.request.query_params.get('isUser', None)

        # If there is content in the search bar, filter exercises by input text
        if search_text is not None:
            exercises = exercises.filter(Q(title__contains=search_text) | Q(description__contains=search_text))
            for exercise in exercises:
                if exercise.player.user == request.auth.user:
                    exercise.is_creator = True
                else:
                    exercise.is_creator = False

        # If there is content in the category dropdown , filter exercises by category selected
        if category_text is not None:
            exercises = exercises.filter(Q(category__label__contains=category_text))
            for exercise in exercises:
                if exercise.player.user == request.auth.user:
                    exercise.is_creator = True
                else:
                    exercise.is_creator = False

        # If checkbox is clicked, show only the current user's exercises       
        if user_data != "" or None:
            exercises = exercises.filter(Q(player__user=request.auth.user))
            for exercise in exercises:
                if exercise.player.user == request.auth.user:
                    exercise.is_creator = True
                else:
                    exercise.is_creator = False

        serializer = ExerciseSerializer(
            exercises, many=True, context={'request': request})
        return Response(serializer.data)

class ExerciseSerializer(serializers.ModelSerializer):
    """JSON serializer for exercises

    Arguments:
        serializer type
    """
    class Meta:
        model = Exercise
        fields = ('id', 'title', 'description', 'player', 'category', 'example_picture', 'is_creator')
        depth = 2
