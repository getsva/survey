from django.db import migrations


NEW_QUESTIONS = [
    {
        "id": 9,
        "category": "Journey Friction",
        "prompt": "Which part of your customer journey suffers most from trust or authenticity gaps right now?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 10,
        "category": "Adoption Blockers",
        "prompt": "What is the biggest blocker keeping you from strengthening identity verification today?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 11,
        "category": "Compliance Clock",
        "prompt": "How urgent are regulatory or audit requirements tied to user identity for your team?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 12,
        "category": "Pilot Timing",
        "prompt": "When would you realistically pilot a higher-assurance verification partner?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 13,
        "category": "Decision Owner",
        "prompt": "Who ultimately signs off on identity, trust, and verification tooling in your org?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 14,
        "category": "Pricing Fit",
        "prompt": "Which pricing structure best matches how you budget for trust or identity tooling?",
        "target_audience": "builders",
        "note": "",
    },
]


def add_questions(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    for data in NEW_QUESTIONS:
        Question.objects.update_or_create(id=data["id"], defaults=data)


def remove_questions(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    Question.objects.filter(id__in=[data["id"] for data in NEW_QUESTIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0006_seed_question_options"),
    ]

    operations = [
        migrations.RunPython(add_questions, remove_questions),
    ]


