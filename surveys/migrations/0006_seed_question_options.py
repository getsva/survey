from django.db import migrations

QUESTION_OPTIONS = {
    1: [
        ("password_manager", "I rely on a password manager app (1Password, Bitwarden, etc.)"),
        ("browser_storage", "I let my browser or phone remember most passwords"),
        ("memorize_few", "I reuse or memorize a small set of passwords"),
        ("offline_list", "I keep them offline (notebook, spreadsheet, etc.)"),
        ("unsure_other", "Something else / not sure"),
    ],
    2: [
        ("very_anxious", "Very anxious — it keeps me up at night"),
        ("somewhat_concerned", "Somewhat concerned — I try to stay cautious"),
        ("neutral", "Neutral — I assume some risk is inevitable"),
        ("unconcerned", "Mostly unconcerned — I don't think about it much"),
        ("resigned", "Resigned — I feel there's nothing I can do"),
    ],
    3: [
        ("mostly_real", "I assume most profiles are real"),
        ("half_real", "I think about half are real and half are bots/fakes"),
        ("suspicious", "I'm skeptical — I assume many are fake"),
        ("depends_platform", "It depends on the platform or topic"),
        ("never_think", "I rarely think about it"),
    ],
    4: [
        ("constant_issue", "It's a constant issue that hurts metrics or UX"),
        ("occasional", "We see it occasionally but it's manageable"),
        ("rare", "It rarely happens"),
        ("not_launched", "We haven't launched broadly enough to know"),
        ("unsure", "Not sure / no visibility"),
    ],
    5: [
        ("shipped", "Yes, we fully shipped phone/ID verification"),
        ("attempted", "We tried but abandoned it due to friction or cost"),
        ("considered", "We considered it but never prioritized it"),
        ("never_needed", "No — we haven't felt the need yet"),
        ("not_applicable", "Not applicable to what we build"),
    ],
    6: [
        ("launch_community", "I'd launch or grow community features more confidently"),
        ("reduce_moderation", "I'd cut moderation / fraud ops workload"),
        ("unlock_growth", "I'd unlock a new product or revenue stream"),
        ("compliance", "I'd meet compliance / trust requirements faster"),
        ("unsure", "Unsure — I'd need to explore use cases"),
    ],
    7: [
        ("excited", "Excited — I'd want to try it right away"),
        ("curious", "Curious but I'd need proof it works"),
        ("privacy_concern", "Concerned about privacy or data handling"),
        ("friction_worry", "Worried it would add too much user friction"),
        ("not_relevant", "It doesn't feel relevant to me"),
    ],
    8: [
        ("definitely_pay", "Yes — I'd pay for a reliable API like this"),
        ("would_trial", "I'd trial it and pay if pricing fits"),
        ("later_scale", "Maybe later, only if we scale a lot"),
        ("probably_not", "Probably not worth paying for us"),
        ("unsure", "Unsure / need more info"),
    ],
}


def seed_question_options(apps, schema_editor):
    Question = apps.get_model("surveys", "Question")
    QuestionOption = apps.get_model("surveys", "QuestionOption")

    for question_id, options in QUESTION_OPTIONS.items():
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            continue
        for order, (value, label) in enumerate(options, start=1):
            QuestionOption.objects.update_or_create(
                question=question,
                value=value,
                defaults={"label": label, "order": order},
            )


def unseed_question_options(apps, schema_editor):
    QuestionOption = apps.get_model("surveys", "QuestionOption")
    QuestionOption.objects.filter(
        question_id__in=list(QUESTION_OPTIONS.keys())
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0005_questionoption"),
    ]

    operations = [
        migrations.RunPython(seed_question_options, unseed_question_options),
    ]


