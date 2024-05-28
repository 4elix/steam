from django.contrib import admin

from .models import Categories, Products, TagsGame, ProductImage

# простое подключения, минус его нельзя настроить, но плюс его лего подключить
admin.site.register(Categories)
admin.site.register(TagsGame)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# подключения через декоратор, плюс и минус в том что его нужно настраивать от а до я
@admin.register(Products)
class CategoriesAdmin(admin.ModelAdmin):
    # тут мы указываем какие поля показывать не переходя на сам продукт
    list_display = ['pk', 'title', 'price_old', 'price_new', 'discount', 'category']
    # тут мы указываем какие поля позволят переходить на сам продукт
    list_display_links = ['pk', 'title']
    # нужно для поиска
    search_fields = ['title']
    # данный поля само будет заполнять с помощью заголовка
    prepopulated_fields = {'slug': ['title']}
    # сортирует от меньшего к большому
    ordering = ['pk']
    # нужен для изменения
    list_editable = ['category']
    # нужен для указания количества отображаемых элементов, то есть пагинация
    list_per_page = 3
    # нужен для фильтрации
    list_filter = ['category__name', 'tags__tag_name']
    # нужен для удобного изменения, применяется к ForeignKey и к choices
    radio_fields = {"category": admin.VERTICAL}
    inlines = [ProductImageInline]

    # работа с внутренними полями

    # нужен для отображения полей
    fields = ['title', 'short_description', 'full_description', 'price_old', 'price_new',
              'discount', 'limitation_age', 'date_time', 'file_came', 'category', 'slug', 'tags']

    # нужен для того что бы указанные поля не отображали
    # exclude = [""]
    # нужен для того что бы указанные поля отображали, но изменять их будет нельзя
    # readonly_fields = ['full_description']
    # нужны для комфортного отображения множества
    filter_horizontal = ['tags']

    # filter_vertical = ['tags']

    # данный метод будет сам меня заполнять поля discount
    def save_model(self, request, obj, form, change):
        # Вычислить скидку, если старая и новая цена были введены
        if obj.price_old and obj.price_new:
            obj.discount = round((obj.price_old - obj.price_new) / obj.price_old * 100)
        super().save_model(request, obj, form, change)
