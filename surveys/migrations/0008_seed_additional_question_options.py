from django.db import migrations

QUESTION_OPTIONS = {
    9: [
        ("top_funnel", "Top of funnel — lead capture or marketing forms"),
        ("onboarding", "Onboarding & signup workflow"),
        ("engagement_loops", "Engagement loops such as comments or messaging"),
        ("marketplace_trust", "Marketplace / community interactions"),
        ("support_escalations", "Support, chargebacks, or escalations"),
    ],
    10: [
        ("integration_effort", "Engineering capacity or integration effort"),
        ("user_friction", "Worried about degrading user experience"),
        ("cost_uncertainty", "Cost or pricing is unclear"),
        ("compliance_review", "Legal/compliance approvals take time"),
        ("no_owner", "No clear owner or OKR for verification"),
    ],
    11: [
        ("urgent_this_quarter", "Urgent — we must address it this quarter"),
        ("scheduled_this_year", "Scheduled for later this year"),
        ("watching_future", "Monitoring but not scheduled yet"),
        ("not_required", "Not required for our business"),
        ("unsure", "Unsure / need guidance"),
    ],
    12: [
        ("already_scoping", "Already scoping vendors or proofs of concept"),
        ("next_two_quarters", "Likely within the next two quarters"),
        ("after_scale_up", "After we scale customer volume further"),
        ("only_if_required", "Only if required by a partner or regulator"),
        ("no_current_plan", "No current plan to pilot"),
    ],
    13: [
        ("product_lead", "Product leadership or GM"),
        ("eng_lead", "Engineering or platform leadership"),
        ("security_team", "Security, risk, or compliance team"),
        ("ops_support", "Operations or support leadership"),
        ("founder", "Founder / CEO makes the call"),
    ],
    14: [
        ("mau_tier", "Monthly active user tiering"),
        ("usage_api", "Usage-based pricing (per API call)"),
        ("flat_subscription", "Flat monthly subscription"),
        ("success_fee", "Outcome or savings-based fee"),
        ("undecided", "Undecided — depends on ROI modeling"),
    ],
}


def seed_options(apps, schema_editor):
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


def unseed_options(apps, schema_editor):
    QuestionOption = apps.get_model("surveys", "QuestionOption")
    QuestionOption.objects.filter(
        question_id__in=list(QUESTION_OPTIONS.keys())
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0007_expand_question_bank"),
    ]

    operations = [
        migrations.RunPython(seed_options, unseed_options),
    ]


