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
        self._question_configs: dict[str, dict] = {}
        for question in self.questions:
            field_name = self.answer_field_name(question)
            options = list(question.options.all())
            self._question_configs[field_name] = {
                "question": question,
                "options": options,
            }
            if options:
                self.fields[field_name] = forms.ChoiceField(
                    label=question.prompt,
                    choices=[(option.value, option.label) for option in options],
                    widget=forms.RadioSelect,
                    required=False,  # All questions are optional by default
                    help_text=self._build_help_text(question),
                )
            else:
                # Q4 and Q6 use single-line inputs, Q5 and Q8 use larger textarea
                if question.id == 4 or question.id == 6:
                    widget = forms.TextInput(
                        attrs={
                            "placeholder": "Your answer...",
                            "class": "single-line-input",
                        }
                    )
                elif question.id == 5 or question.id == 8:
                    widget = forms.Textarea(
                        attrs={
                            "rows": 5,
                            "placeholder": "Please share your thoughts..." if question.id == 8 else "Please be honest about your experience...",
                        }
                    )
                else:
                    widget = forms.Textarea(
                        attrs={
                            "rows": 3,
                            "placeholder": "Share as much detail as you can...",
                        }
                    )
                # All questions are optional by default
                # Builder-only questions will be validated in clean() method
                self.fields[field_name] = forms.CharField(
                    label=question.prompt,
                    widget=widget,
                    required=False,  # All questions are optional by default
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
        # Get Q1 answer to determine if user is a builder
        q1_answer = cleaned_data.get("question_1", "")
        is_builder = q1_answer in ["developer", "founder"]
        
        # Also check respondent_role for backward compatibility
        respondent_role = cleaned_data.get("respondent_role")
        is_builder_role = respondent_role == SurveyResponse.RespondentRole.BUILDERS
        
        for question in self.questions:
            field_name = self.answer_field_name(question)
            answer = cleaned_data.get(field_name)
            config = self._question_configs.get(field_name, {})
            options = config.get("options", [])
            if answer and not options and isinstance(answer, str):
                cleaned_data[field_name] = answer.strip()
            # Validate builder-only questions based on Q1 answer or respondent_role
            if (
                question.target_audience == Question.TargetAudience.BUILDERS
                and (is_builder or is_builder_role)
                and not cleaned_data.get(field_name)
            ):
                self.add_error(field_name, "This question is required for builders.")
        return cleaned_data

