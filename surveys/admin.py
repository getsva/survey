from django.contrib import admin

from .models import Question, QuestionOption, SurveyAnswer, SurveyResponse


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 0
    fields = ("label", "value", "order")
    ordering = ("order", "id")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "target_audience", "is_active")
    list_filter = ("target_audience", "is_active")
    search_fields = ("prompt", "category")
    ordering = ("id",)
    inlines = [QuestionOptionInline]


class SurveyAnswerInline(admin.TabularInline):
    model = SurveyAnswer
    extra = 0
    readonly_fields = ("question", "answer_text")


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ("respondent_name", "respondent_role", "created_at")
    list_filter = ("respondent_role", "created_at")
    search_fields = ("respondent_name", "respondent_email")
    inlines = [SurveyAnswerInline]
    readonly_fields = ("created_at", "updated_at")
