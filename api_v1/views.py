from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pages.models import Games, Categories, TagsGame
from .serializers import GameSerializer, CategorySerializer, TagSerializer


@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        queryset = Games.objects.all()
        serializer = GameSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request, slug_path):
    game = get_object_or_404(Games, slug=slug_path)
    if request.method == 'GET':
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GameSerializer(game, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        queryset = Categories.objects.annotate(number_games_in_category=Count('games')).all()
        serializer = CategorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, cat_id):
    category = Categories.objects.annotate(number_games_in_category=Count('games')).get(pk=cat_id)
    if request.method == 'GET':
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def tags_game_list(request):
    if request.method == 'GET':
        queryset = TagsGame.objects.annotate(number_games_in_tag=Count('tag_game')).all()
        serializer = TagSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def tags_detail(request, pk_path):
    tag = TagsGame.objects.annotate(number_games_in_tag=Count('tag_game')).get(pk=pk_path)
    if request.method == 'GET':
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TagSerializer(tag, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
