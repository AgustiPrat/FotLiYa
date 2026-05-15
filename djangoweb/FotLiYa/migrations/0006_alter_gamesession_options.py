from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FotLiYa', '0005_alter_question_source'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamesession',
            options={'ordering': ['-created_at']},
        ),
    ]
