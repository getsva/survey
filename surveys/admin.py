from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export.formats import base_formats

from .models import Question, QuestionOption, SurveyAnswer, SurveyResponse
from .resources import (
    QuestionResource,
    SurveyResponseResource,
    SurveyAnswerResource,
    SurveyResponseDetailedResource,
)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 0
    fields = ("label", "value", "order")
    ordering = ("order", "id")


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ("id", "category", "target_audience", "is_active")
    list_filter = ("target_audience", "is_active")
    search_fields = ("prompt", "category")
    ordering = ("id",)
    inlines = [QuestionOptionInline]
    formats = (base_formats.CSV, base_formats.XLSX, base_formats.JSON)


class SurveyAnswerInline(admin.TabularInline):
    model = SurveyAnswer
    extra = 0
    readonly_fields = ("question", "answer_text")


@admin.register(SurveyResponse)
class SurveyResponseAdmin(ImportExportActionModelAdmin):
    """
    Admin for Survey Responses with export functionality.
    Provides two export options:
    1. Basic export: Response details only
    2. Detailed export: Responses with all questions as columns (via action)
    """
    resource_class = SurveyResponseDetailedResource
    list_display = ("respondent_name", "respondent_email", "respondent_role", "created_at")
    list_filter = ("respondent_role", "created_at")
    search_fields = ("respondent_name", "respondent_email")
    inlines = [SurveyAnswerInline]
    readonly_fields = ("created_at", "updated_at")
    formats = (base_formats.CSV, base_formats.XLSX, base_formats.JSON)
    
    def get_resource_class(self):
        """Use detailed resource for export"""
        return SurveyResponseDetailedResource
    
    def get_export_resource_class(self):
        """Use detailed resource for export"""
        return SurveyResponseDetailedResource


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(ImportExportModelAdmin):
    """Admin for individual Survey Answers - useful for detailed analysis"""
    resource_class = SurveyAnswerResource
    list_display = ("response", "question", "answer_text", "created_at")
    list_filter = ("question__category", "created_at")
    search_fields = ("answer_text", "response__respondent_name", "question__prompt")
    readonly_fields = ("created_at",)
    formats = (base_formats.CSV, base_formats.XLSX, base_formats.JSON)
