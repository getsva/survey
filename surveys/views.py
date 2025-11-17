from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import SurveyForm
from .models import Question, SurveyAnswer, SurveyResponse


def survey_form(request):
    questions = list(Question.objects.filter(is_active=True).order_by("id"))
    has_questions = len(questions) > 0

    if request.method == "POST":
        form = SurveyForm(request.POST, questions=questions)
        if form.is_valid():
            response = SurveyResponse.objects.create(
                respondent_name=form.cleaned_data.get("respondent_name", "").strip(),
                respondent_email=form.cleaned_data.get("respondent_email", "").strip(),
                respondent_role=form.cleaned_data["respondent_role"],
            )
            answers = []
            for question in questions:
                field_name = SurveyForm.answer_field_name(question)
                answer_text = form.cleaned_data.get(field_name, "")
                if answer_text:
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
    else:
        form = SurveyForm(questions=questions) if has_questions else None

    question_field_pairs = []
    if has_questions and form is not None:
        for question in questions:
            field_name = SurveyForm.answer_field_name(question)
            question_field_pairs.append(
                {"question": question, "field": form[field_name]}
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
