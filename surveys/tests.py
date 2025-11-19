from django.test import TestCase
from django.urls import reverse

from .models import Question, QuestionOption, SurveyAnswer, SurveyResponse


class SurveyViewTests(TestCase):
    def setUp(self):
        Question.objects.all().delete()
        q1 = Question.objects.create(
            id=1,
            category="Behavior",
            prompt="How do you manage passwords?",
            target_audience=Question.TargetAudience.ALL,
        )
        q2 = Question.objects.create(
            id=2,
            category="Builders",
            prompt="Builders only question",
            target_audience=Question.TargetAudience.BUILDERS,
        )
        QuestionOption.objects.create(
            question=q1,
            value="password_manager",
            label="Password manager",
            order=1,
        )
        QuestionOption.objects.create(
            question=q2,
            value="required_option",
            label="Required option",
            order=1,
        )

    def test_get_form_renders_questions(self):
        response = self.client.get(reverse("surveys:form"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How do you manage passwords?")

    def test_post_creates_response_and_answers(self):
        payload = {
            "respondent_name": "Alex",
            "respondent_email": "alex@example.com",
            "respondent_role": SurveyResponse.RespondentRole.GENERAL,
            "question_1": "password_manager",
            "question_2": "",
        }
        response = self.client.post(reverse("surveys:form"), data=payload)
        self.assertRedirects(response, reverse("surveys:thank_you"))
        self.assertEqual(SurveyResponse.objects.count(), 1)
        self.assertEqual(SurveyAnswer.objects.count(), 1)

    def test_builder_question_required_for_builders(self):
        payload = {
            "respondent_name": "",
            "respondent_email": "",
            "respondent_role": SurveyResponse.RespondentRole.BUILDERS,
            "question_1": "password_manager",
            "question_2": "",
        }
        response = self.client.post(reverse("surveys:form"), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This question is required for builders.")
