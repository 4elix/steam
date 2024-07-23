from rest_framework import serializers
from pages.models import Games, Categories, TagsGame, Favorite


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'title', 'link_category', 'quantity_symbol_short', 'quantity_symbol_full',
                  'price_old', 'price_new', 'discount', 'slug']

    quantity_symbol_short = serializers.SerializerMethodField(method_name='len_desc_short')
    quantity_symbol_full = serializers.SerializerMethodField(method_name='len_desc_full')
    link_category = serializers.HyperlinkedRelatedField(queryset=Categories.objects.all(),
                                                        view_name='category-detail', source='category',
                                                        lookup_url_kwarg='cat_id')

    def len_desc_short(self, game: Games):
        return f'Количество символов в кратком описание: {len(game.short_description)}'

    def len_desc_full(self, game: Games):
        return f'Количество символов в полном описание: {len(game.full_description)}'

    def create(self, validated_data):
        game = Games(**validated_data)
        game.other = 1
        game.save()
        return game

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'number_games_in_category']

    number_games_in_category = serializers.IntegerField(read_only=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsGame
        fields = ['id', 'tag_name', 'number_games_in_tag']

    number_games_in_tag = serializers.IntegerField(read_only=True)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['auth', 'game']


