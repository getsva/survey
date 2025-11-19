from django import forms
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import SurveyForm
from .models import Question, SurveyAnswer, SurveyResponse


def survey_form(request):
    questions = list(
        Question.objects.filter(is_active=True)
        .order_by("id")
        .prefetch_related("options")
    )
    has_questions = len(questions) > 0

    if request.method == "POST":
        form = SurveyForm(request.POST, questions=questions)
        if form.is_valid():
            try:
                # Determine respondent_role based on Q1 answer
                q1_answer = form.cleaned_data.get("question_1", "")
                if q1_answer in ["developer", "founder"]:
                    respondent_role = SurveyResponse.RespondentRole.BUILDERS
                else:
                    respondent_role = form.cleaned_data.get("respondent_role", SurveyResponse.RespondentRole.GENERAL)
                
                response = SurveyResponse.objects.create(
                    respondent_name=form.cleaned_data.get("respondent_name", "").strip(),
                    respondent_email=form.cleaned_data.get("respondent_email", "").strip(),
                    respondent_role=respondent_role,
                )
                answers = []
                for question in questions:
                    field_name = SurveyForm.answer_field_name(question)
                    answer_value = form.cleaned_data.get(field_name, "")
                    if not answer_value:
                        continue
                    options = list(question.options.all())
                    if options:
                        option_lookup = {opt.value: opt for opt in options}
                        selected_option = option_lookup.get(answer_value)
                        answer_text = (
                            selected_option.label if selected_option else answer_value
                        )
                    else:
                        answer_text = answer_value
                    answers.append(
                        SurveyAnswer(
                            response=response,
                            question=question,
                            answer_text=answer_text,
                        )
                    )
                if answers:
                    SurveyAnswer.objects.bulk_create(answers)
                messages.success(
                    request,
                    "Thanks for sharing! Your responses were saved successfully.",
                )
                return redirect(reverse("surveys:thank_you"))
            except Exception as e:
                messages.error(
                    request,
                    f"An error occurred while saving your response: {str(e)}",
                )
        else:
            # Form is invalid - errors will be displayed in template
            messages.error(
                request,
                "Please correct the errors below and try again.",
            )
    else:
        form = SurveyForm(questions=questions) if has_questions else None

    question_field_pairs = []
    if has_questions and form is not None:
        for question in questions:
            field_name = SurveyForm.answer_field_name(question)
            bound_field = form[field_name]
            question_field_pairs.append(
                {
                    "question": question,
                    "field": bound_field,
                    "is_radio": isinstance(bound_field.field.widget, forms.RadioSelect),
                }
            )

    return render(
        request,
        "surveys/survey_form.html",
        {
            "form": form,
            "questions": questions,
            "question_field_pairs": question_field_pairs,
            "no_questions": not has_questions,
        },
    )


def thank_you(request):
    return render(request, "surveys/thank_you.html")
