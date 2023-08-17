from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScoupeInlineFormset(BaseInlineFormSet):
    def save(self):
        count_is_main = 0
        for form in self.forms:
            if form.cleaned_data['is_main']:
                count_is_main += 1

        if count_is_main != 1:
            raise ValidationError('Один из тегов должен быть основным')
        return super().save()  # вызываем базовый код переопределяемого метода


class ScoupeInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = ScoupeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ScoupeInline,
    ]
    list_display = ['title', 'text', 'published_at', 'image']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
