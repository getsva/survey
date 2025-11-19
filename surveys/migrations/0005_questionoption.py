from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0004_delete_waitlistentry"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestionOption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=50)),
                ("label", models.CharField(max_length=255)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="options",
                        to="surveys.question",
                    ),
                ),
            ],
            options={
                "ordering": ["question_id", "order", "id"],
                "unique_together": {("question", "value")},
            },
        ),
    ]


