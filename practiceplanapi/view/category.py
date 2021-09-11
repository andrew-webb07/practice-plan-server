"""View module for handling requests about categorys"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from practiceplanapi.models import Category, Player
from django.db.models import Q

class CategoryView(ViewSet):
    """Practice Plan Categories"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized category instance
        """
        player = Player.objects.get(user=request.auth.user)
        category = Category()
        category.label = request.data["label"]
        category.player = player

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category
        Returns:
            Response -- JSON serialized category instance
        """
        try:

            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        except Category.DoesNotExist as ex:
            return Response({'message':ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a category

        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)
        category = Category.objects.get(pk=pk)
        category.player = player
        category.label = request.data["label"]
        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single category
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to categories resource
        Returns:
            Response -- JSON serialized list of categories
        """
        categories = Category.objects.filter(Q(player__user=request.auth.user) | Q(player__is_public=1))

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)
        

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categorys

    Arguments:
        serializer type
    """
    class Meta:
        model = Category
        fields = ('id', 'label', 'player')
        depth = 1