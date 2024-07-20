from django.contrib import admin

from .models import Categories, Games, TagsGame, GameImage

# простое подключения, минус его нельзя настроить, но плюс его лего подключить
admin.site.register(Categories)
admin.site.register(TagsGame)


class GamesImageInline(admin.TabularInline):
    model = GameImage
    extra = 1


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'price_old', 'price_new', 'discount', 'category']
    list_display_links = ['pk', 'title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ['title']}
    ordering = ['pk']
    list_editable = ['category']
    list_per_page = 3
    list_filter = ['category__name', 'tags__tag_name']
    radio_fields = {"category": admin.VERTICAL}
    inlines = [GamesImageInline]

    field = ['__all__']

    filter_horizontal = ['tags']

    def save_model(self, request, obj, form, change):
        # Вычислить скидку, если старая и новая цена были введены
        if obj.price_old and obj.price_new:
            res = round((obj.price_old - obj.price_new) / obj.price_old * 100)
            if res < 0:
                obj.discount = 0
            else:
                obj.discount = res
        super().save_model(request, obj, form, change)
