from django.db import migrations


QUESTIONS = [
    {
        "id": 1,
        "category": "Behavior",
        "prompt": "How do you personally manage all your passwords? What's your system?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 2,
        "category": "Emotion",
        "prompt": (
            "After all the data breaches we hear about and the stories of our data being sold, "
            "how does that make you feel about your personal information being on so many different servers?"
        ),
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 3,
        "category": "Ecosystem Trust",
        "prompt": "When you're on a platform like Twitter or any social media, how much do you trust that the other profiles are actual, real people?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 4,
        "category": "Business Pain",
        "prompt": "When you've built projects, did you have to deal with fake accounts, spam signups, or bots? How big of a problem was it, really?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 5,
        "category": "Past Solutions",
        "prompt": "Did you ever consider adding user verification—like phone or ID—to your apps? What stopped you?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 6,
        "category": "Value Proposition",
        "prompt": "If you had a magic API that guaranteed every single user was a real, unique person, what would that unlock for your business? What could you build that you can't build today?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 7,
        "category": "Gut Reaction",
        "prompt": "What is your immediate, gut reaction to that? What part sounds most interesting, and what is your biggest concern or reason for skepticism?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 8,
        "category": "Willingness to Pay",
        "prompt": "For the developer API, does this solve a big enough problem that you would consider paying a monthly fee for it, assuming it worked perfectly?",
        "target_audience": "builders",
        "note": "For builders only",
    },
]


def seed_questions(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    for data in QUESTIONS:
        Question.objects.update_or_create(id=data["id"], defaults=data)


def unseed_questions(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    Question.objects.filter(id__in=[q["id"] for q in QUESTIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_questions, unseed_questions),
    ]

