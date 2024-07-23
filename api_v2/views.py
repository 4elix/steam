from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from pages.models import Games, Categories, TagsGame, Favorite
from api_v1.serializers import GameSerializer, CategorySerializer, TagSerializer, FavoriteSerializer


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


class CategoryList(APIView):
    def get(self, request):
        queryset = Categories.objects.annotate(number_games_in_category=Count('games')).all()
        serializer = CategorySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetail(APIView):
    def get(self, request, cat_id):
        category = Categories.objects.annotate(number_games_in_category=Count('games')).get(pk=cat_id)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

    def put(self, request, cat_id):
        category = Categories.objects.annotate(number_games_in_category=Count('games')).get(pk=cat_id)
        serializer = CategorySerializer(category, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, cat_id):
        category = Categories.objects.annotate(number_games_in_category=Count('games')).get(pk=cat_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(APIView):
    def get(self, request):
        queryset = TagsGame.objects.all()
        serializer = TagSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagDetail(APIView):
    def get(self, request, pk_path):
        tag = TagsGame.objects.annotate(number_games_in_tag=Count('tag_game')).get(pk=pk_path)
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk_path):
        tag = TagsGame.objects.annotate(number_games_in_tag=Count('tag_game')).get(pk=pk_path)
        serializer = TagSerializer(tag, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk_path):
        tag = TagsGame.objects.annotate(number_games_in_tag=Count('tag_game')).get(pk=pk_path)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteList(APIView):
    def get(self, request):
        queryset = Favorite.objects.all()
        serializer = FavoriteSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

