from .models import ProposedQuestion


def pending_questions_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {
            "pending_questions_count": ProposedQuestion.objects.filter(status="pending").count()
        }
    return {"pending_questions_count": 0}