from django.db import models


class Question(models.Model):
    class TargetAudience(models.TextChoices):
        ALL = "all", "Everyone"
        BUILDERS = "builders", "Builders"

    id = models.PositiveSmallIntegerField(primary_key=True)
    category = models.CharField(max_length=100)
    prompt = models.TextField()
    target_audience = models.CharField(
        max_length=20,
        choices=TargetAudience.choices,
        default=TargetAudience.ALL,
    )
    note = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.id}. {self.prompt[:50]}"


class SurveyResponse(models.Model):
    class RespondentRole(models.TextChoices):
        GENERAL = "all", "General respondent"
        BUILDERS = "builders", "Builder / technical"

    respondent_name = models.CharField(max_length=120, blank=True)
    respondent_email = models.EmailField(blank=True)
    respondent_role = models.CharField(
        max_length=20,
        choices=RespondentRole.choices,
        default=RespondentRole.GENERAL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        identity = self.respondent_name or "Anonymous responder"
        return f"{identity} ({self.get_respondent_role_display()})"


class SurveyAnswer(models.Model):
    response = models.ForeignKey(
        SurveyResponse,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name="answers",
    )
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["question_id"]
        unique_together = ("response", "question")

    def __str__(self) -> str:
        return f"Response {self.response_id} → Question {self.question_id}"
