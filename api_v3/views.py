from django.shortcuts import render
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from api_v1.serializers import GameSerializer, CategorySerializer, TagSerializer
from pages.models import Games, Categories, TagsGame


class GameViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Games.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['price_old']

    def get_serializer_context(self):
        return {'reqeust': self.request}


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Categories.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']
