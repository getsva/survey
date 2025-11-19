from django.db import migrations

UPDATED_QUESTIONS = [
    {
        "id": 1,
        "category": "Identity Hygiene",
        "prompt": "How do you currently manage your passwords across work and personal tools?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 2,
        "category": "Risk Posture",
        "prompt": "How concerned are you about your personal data being exposed in a breach or leak?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 3,
        "category": "Network Trust",
        "prompt": "How confident are you that people on major platforms are who they claim to be?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 4,
        "category": "Abuse Impact",
        "prompt": "How often do fake accounts or spam registrations distort your product metrics?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 5,
        "category": "Verification Status",
        "prompt": "Where are you today with adding phone, document, or ID verification to your product?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 6,
        "category": "Value Unlock",
        "prompt": "If you could trust every user was unique and human, what would you prioritize shipping first?",
        "target_audience": "builders",
        "note": "",
    },
    {
        "id": 7,
        "category": "Market Reaction",
        "prompt": "What is your immediate reaction to a platform that guarantees verified human users?",
        "target_audience": "all",
        "note": "",
    },
    {
        "id": 8,
        "category": "Budget Intent",
        "prompt": "Would you allocate budget for a verification API if it consistently proved reliability?",
        "target_audience": "builders",
        "note": "For builders only",
    },
]

ORIGINAL_QUESTIONS = [
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
        "prompt": "After all the data breaches we hear about and the stories of our data being sold, how does that make you feel about your personal information being on so many different servers?",
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


def apply_question_copy(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    for data in UPDATED_QUESTIONS:
        Question.objects.update_or_create(id=data["id"], defaults=data)


def revert_question_copy(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    for data in ORIGINAL_QUESTIONS:
        Question.objects.update_or_create(id=data["id"], defaults=data)


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0008_seed_additional_question_options"),
    ]

    operations = [
        migrations.RunPython(apply_question_copy, revert_question_copy),
    ]


