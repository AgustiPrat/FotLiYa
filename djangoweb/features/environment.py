import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projecteweb.settings")
os.environ["DB_ENGINE"] = "postgres"
os.environ["DB_NAME"] = "fotliya"
os.environ["DB_USER"] = "fotliya"
os.environ["DB_PASSWORD"] = "fotliya"
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DEBUG"] = "True"

import django
django.setup()


def before_scenario(context, scenario):
    from django.contrib.auth.models import User
    from FotLiYa.models import ProposedQuestion, Question

    ProposedQuestion.objects.all().delete()
    Question.objects.filter(source="proposed").delete()
    User.objects.filter(username__in=[
        "user1", "user2", "user3", "user4", "user5", "admin1", "admin2"
    ]).delete()


def after_scenario(context, scenario):
    if hasattr(context, "browser"):
        context.browser.quit()