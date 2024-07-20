from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pages.models import Games, Categories, TagsGame
from api_v1.serializers import GameSerializer


class GameList(APIView):
    def get(self, request):
        queryset = Games.objects.all()
        serializer = GameSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = GameSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameDetail(APIView):
    def get(self, request, slug_path):
        game = get_object_or_404(Games, slug=slug_path)
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)

    def put(self, request, slug_path):
        game = get_object_or_404(Games, slug=slug_path)
        serializer = GameSerializer(game, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, slug_path):
        game = get_object_or_404(Games, slug=slug_path)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
