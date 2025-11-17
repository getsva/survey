from typing import Iterable

from django import forms

from .models import Question, SurveyResponse


class SurveyForm(forms.Form):
    respondent_name = forms.CharField(
        label="Your name",
        required=False,
        help_text="Optional. Helps us follow up with clarifying questions.",
    )
    respondent_email = forms.EmailField(
        label="Email",
        required=False,
        help_text="Optional. We will only use it to follow up on your answers.",
    )
    respondent_role = forms.ChoiceField(
        label="Which best describes you?",
        choices=SurveyResponse.RespondentRole.choices,
        initial=SurveyResponse.RespondentRole.GENERAL,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, questions: Iterable[Question] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.questions = list(questions or [])
        for question in self.questions:
            field_name = self.answer_field_name(question)
            self.fields[field_name] = forms.CharField(
                label=question.prompt,
                widget=forms.Textarea(
                    attrs={
                        "rows": 3,
                        "placeholder": "Share as much detail as you can...",
                    }
                ),
                required=question.target_audience == Question.TargetAudience.ALL,
                help_text=self._build_help_text(question),
            )

    @staticmethod
    def answer_field_name(question: Question) -> str:
        return f"question_{question.id}"

    @staticmethod
    def _build_help_text(question: Question) -> str:
        parts = [question.category]
        if question.target_audience == Question.TargetAudience.BUILDERS:
            parts.append("Builders only")
        if question.note:
            parts.append(question.note)
        return " • ".join(parts)

    def clean(self):
        cleaned_data = super().clean()
        respondent_role = cleaned_data.get("respondent_role")
        for question in self.questions:
            field_name = self.answer_field_name(question)
            answer = cleaned_data.get(field_name)
            if answer:
                cleaned_data[field_name] = answer.strip()
            if (
                question.target_audience == Question.TargetAudience.BUILDERS
                and respondent_role == SurveyResponse.RespondentRole.BUILDERS
                and not cleaned_data.get(field_name)
            ):
                self.add_error(field_name, "This question is required for builders.")
        return cleaned_data

