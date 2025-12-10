from django.contrib import admin
from .models import Category, Question, Choice, Result

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'category')

admin.site.register(Category)
admin.site.register(Result)
