from django.db import migrations

NEW_QUESTIONS = [
    {
        "id": 1,
        "category": "About You",
        "prompt": "Which of these best describes you?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 2,
        "category": "About You",
        "prompt": "On average, how do you usually sign up for a new website or app?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 3,
        "category": "About You",
        "prompt": "How do you feel when you hear about a major data breach at a company where you have an account?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 4,
        "category": "The Core Problem",
        "prompt": "If you could wave a magic wand and permanently fix one thing about logging in, signing up, or managing your online accounts, what would it be?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 5,
        "category": "The Core Problem",
        "prompt": "For founders/developers: how big of a problem are bots, spam, and fake accounts for your projects? Please be honest.",
        "target_audience": "builders",
        "note": "For builders only",
    },
    {
        "id": 6,
        "category": "The Solution & The Test",
        "prompt": "What is your immediate, gut reaction to the Sva concept?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 7,
        "category": "The Solution & The Test",
        "prompt": "For the developer API that eliminates bots, would you consider paying a monthly fee if it worked perfectly?",
        "target_audience": "builders",
        "note": "For builders only",
    },
]

NEW_OPTIONS = {
    1: [
        ("student", "Student"),
        ("developer", "Software Developer / Engineer"),
        ("founder", "Founder / Entrepreneur"),
        ("product_manager", "Product Manager"),
        ("other", "Other"),
    ],
    2: [
        ("new_password", "I create a new, unique password for it."),
        ("social_login", "I use \"Continue with Google\" or another social login."),
        ("reuse_password", "I reuse a password I've used on other sites."),
        ("password_manager", "I use a password manager to generate a new password."),
    ],
    3: [
        ("anxious", "Anxious: I immediately go and change my password."),
        ("resigned", "Resigned: I'm not surprised, I just assume it will happen."),
        ("apathetic", "Apathetic: I don't really think about it much."),
    ],
    7: [
        ("no_free_only", "No, I would only use a free solution."),
        ("yes_small_fee", "Yes, this solves a minor problem, I'd pay a small fee (e.g., ~$10/mo)."),
        ("yes_significant_fee", "Yes, this solves a major problem, I'd pay a significant fee (e.g., $50/mo or more)."),
        ("not_sure", "I'm not sure."),
    ],
}


def apply_new_structure(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    QuestionOption = apps.get_model("surveys", "QuestionOption")
    
    # Update questions
    for data in NEW_QUESTIONS:
        Question.objects.update_or_create(id=data["id"], defaults=data)
    
    # Clear old options and add new ones
    for question_id, options in NEW_OPTIONS.items():
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            continue
        # Delete old options
        QuestionOption.objects.filter(question=question).delete()
        # Add new options
        for order, (value, label) in enumerate(options, start=1):
            QuestionOption.objects.create(
                question=question,
                value=value,
                label=label,
                order=order,
            )


def revert_new_structure(apps, schema_editor):
    # This would revert to previous state, but we'll keep it simple
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0010_refresh_question_options"),
    ]

    operations = [
        migrations.RunPython(apply_new_structure, revert_new_structure),
    ]

