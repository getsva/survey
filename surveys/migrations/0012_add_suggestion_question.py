from django.db import migrations

NEW_QUESTION = {
    "id": 8,
    "category": "Feedback & Suggestions",
    "prompt": "Is there a specific pain point or problem you face that Sva could help solve? Any suggestions on how we can make it better?",
    "target_audience": "all",
    "note": "Optional - Share your thoughts",
}


def add_suggestion_question(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    QuestionOption = apps.get_model("surveys", "QuestionOption")
    
    # Create or update the question
    question, created = Question.objects.update_or_create(
        id=NEW_QUESTION["id"], 
        defaults=NEW_QUESTION
    )
    
    # Ensure Q8 has no options (it should be a text input, not multiple choice)
    QuestionOption.objects.filter(question=question).delete()


def remove_suggestion_question(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    Question.objects.filter(id=NEW_QUESTION["id"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0011_new_survey_structure"),
    ]

    operations = [
        migrations.RunPython(add_suggestion_question, remove_suggestion_question),
    ]

