from django.db import migrations

NEW_OPTIONS = {
    1: [
        ("password_manager", "Dedicated password manager (1Password, Bitwarden, etc.)"),
        ("browser_wallet", "Browser or mobile auto-fill handles most logins"),
        ("limited_set", "I reuse a small set of memorable passwords"),
        ("shared_sheet", "I track them manually in a sheet or notebook"),
        ("ad_hoc", "It's ad hoc — I reset passwords when I forget them"),
    ],
    2: [
        ("extremely_concerned", "Extremely concerned — it is a top personal risk"),
        ("heightened_awareness", "Concerned — I stay cautious and monitor accounts"),
        ("managed_risk", "Aware but calm — I take basic precautions"),
        ("minimally_concerned", "Minimally concerned — I rarely think about it"),
        ("not_focused", "Not focused on it at all"),
    ],
    3: [
        ("high_trust", "I generally trust that most profiles are authentic"),
        ("situational_trust", "Trust varies by community or topic"),
        ("skeptical", "I'm skeptical — I assume many profiles are fake"),
        ("depends_channel", "Confidence depends entirely on the platform"),
        ("no_attention", "I don't pay attention to authenticity signals"),
    ],
    4: [
        ("constant_headache", "It is a constant headache that warps reporting"),
        ("regular_surge", "We see meaningful spikes every month or quarter"),
        ("rare_noise", "It happens but is mostly background noise"),
        ("prelaunch", "We are pre-launch / don’t have volume yet"),
        ("no_visibility", "Unsure — we lack visibility into the problem"),
    ],
    5: [
        ("fully_live", "We already run phone, document, or ID verification live"),
        ("pilot_phase", "We have a pilot with a subset of traffic"),
        ("planned_quarter", "It is committed on the roadmap this quarter"),
        ("researching_only", "We are researching solutions but not scheduled"),
        ("not_prioritized", "It hasn't been prioritized yet"),
    ],
    6: [
        ("launch_new_community", "Launch or accelerate a community/marketplace feature"),
        ("reduce_moderation_load", "Reduce moderation, fraud ops, or support workload"),
        ("unlock_growth_ops", "Unlock a new revenue or growth motion"),
        ("meet_compliance", "Meet compliance or enterprise procurement requirements"),
        ("still_validating", "Still validating the best use case"),
    ],
    7: [
        ("ready_to_try", "I'm ready to try it — sounds valuable immediately"),
        ("curious_needs_proof", "Curious, but I need proof it works at scale"),
        ("privacy_skeptic", "Cautious — I need clarity on privacy and data use"),
        ("friction_worried", "Concerned it will add too much user friction"),
        ("not_relevant_now", "Not relevant to my current work"),
    ],
    8: [
        ("line_item_now", "Yes — I'd budget for it this planning cycle"),
        ("budget_with_roi", "Likely, if ROI is proven quickly"),
        ("maybe_later", "Maybe later, once we scale further"),
        ("unlikely_purchase", "Unlikely — other initiatives win first"),
        ("need_more_context", "Need more context before deciding"),
    ],
}

OLD_OPTIONS = {
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


def update_options(apps, schema_editor, mapping):
    Question = apps.get_model("surveys", "Question")
    QuestionOption = apps.get_model("surveys", "QuestionOption")

    for question_id, options in mapping.items():
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            continue
        QuestionOption.objects.filter(question=question).exclude(
            value__in=[value for value, _ in options]
        ).delete()
        for order, (value, label) in enumerate(options, start=1):
            QuestionOption.objects.update_or_create(
                question=question,
                value=value,
                defaults={"label": label, "order": order},
            )


def apply_new_options(apps, schema_editor):
    update_options(apps, schema_editor, NEW_OPTIONS)


def revert_new_options(apps, schema_editor):
    update_options(apps, schema_editor, OLD_OPTIONS)


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0009_refresh_question_copy"),
    ]

    operations = [
        migrations.RunPython(apply_new_options, revert_new_options),
    ]


