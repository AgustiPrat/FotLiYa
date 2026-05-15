from behave import given, when, then
from splinter import Browser
from django.contrib.auth.models import User
from FotLiYa.models import ProposedQuestion, Question
from django.test.utils import setup_test_environment
import time


def get_base_url():
    return "http://localhost:8080"


def get_browser():
    return Browser("chrome", headless=True)


@given('existe un usuario "{username}" con password "{password}"')
def step_create_user(context, username, password):
    User.objects.filter(username=username).delete()
    User.objects.create_user(username=username, password=password)


@given('existe un admin "{username}" con password "{password}"')
def step_create_admin(context, username, password):
    User.objects.filter(username=username).delete()
    user = User.objects.create_user(username=username, password=password)
    user.is_staff = True
    user.is_superuser = True
    user.save()


@given('existe una proposed question de "{username}" con texto "{text}"')
def step_create_question(context, username, text):
    user = User.objects.get(username=username)
    ProposedQuestion.objects.all().delete()
    question = ProposedQuestion.objects.create(
        text=text,
        category="party",
        mechanics="repte",
        created_by=user,
        status="pending",
    )
    context.question_pk = question.pk

@when('vaig a editar la meva pregunta')
def step_go_edit_own_question(context):
    context.browser.visit(get_base_url() + f"/questions/{context.question_pk}/edit/")
    print("\nURL ACTUAL:", context.browser.url)
    print("\nHTML ACTUAL:\n", context.browser.html[:2000])

@when('vaig a eliminar la meva pregunta')
def step_go_delete_own_question(context):
    context.browser.visit(get_base_url() + f"/questions/{context.question_pk}/delete/")
    print("\nURL ACTUAL:", context.browser.url)
    print("\nHTML ACTUAL:\n", context.browser.html[:2000])

@when('voy a "{path}"')
def step_visit(context, path):
    if not hasattr(context, "browser"):
        context.browser = get_browser()
    context.browser.visit(get_base_url() + path)
    print("\nURL ACTUAL:", context.browser.url)
    print("\nHTML ACTUAL:\n", context.browser.html[:2000])

@when('hago login como "{username}" con password "{password}"')
def step_login(context, username, password):
    if not hasattr(context, "browser"):
        context.browser = get_browser()
    context.browser.visit(get_base_url() + "/login/")
    context.browser.fill("username", username)
    context.browser.fill("password", password)
    context.browser.find_by_text("Entrar").first.click()
    time.sleep(1)


@when('relleno el formulario de pregunta con texto "{text}", categoria "{category}" y mecanica "{mechanics}"')
def step_fill_question_form(context, text, category, mechanics):
    context.browser.find_by_css('textarea[name="text"]').first.fill(text)
    context.browser.find_by_css('input[name="category"]').first.fill(category)
    context.browser.find_by_css('input[name="mechanics"]').first.fill(mechanics)

@when('cambio el texto de la pregunta a "{text}"')
def step_change_text(context, text):
    context.browser.find_by_css('textarea[name="text"]').first.fill(text)


@when('envio el formulario')
def step_submit_form(context):
    context.browser.find_by_tag("button").first.click()
    time.sleep(1)


@when('confirmo la eliminacion')
def step_confirm_delete(context):
    context.browser.find_by_tag("button").first.click()
    time.sleep(1)


@when('apruebo la pregunta pendiente')
def step_approve_question(context):
    context.browser.find_by_text("Aprovar").first.click()
    time.sleep(1)


@when('voy a rebutjar la pregunta pendiente')
def step_go_reject(context):
    context.browser.find_by_text("Rebutjar").first.click()
    time.sleep(1)


@when('escribo la nota de rechazo "{note}"')
def step_fill_reject_note(context, note):
    context.browser.fill("admin_note", note)


@then('debería ver "{text}"')
def step_should_see_text(context, text):
    assert text in context.browser.html


@then('debería ser redirigido al login')
def step_should_redirect_login(context):
    assert "/login/" in context.browser.url or "Login" in context.browser.html

@then('la pregunta hauria d\'estar aprovada')
def step_question_should_be_approved(context):
    question = ProposedQuestion.objects.get(pk=context.question_pk)
    assert question.status == "approved"
    assert Question.objects.filter(text=question.text, source="proposed").exists()


@then('la pregunta hauria d\'estar rebutjada amb la nota "{note}"')
def step_question_should_be_rejected_with_note(context, note):
    question = ProposedQuestion.objects.get(pk=context.question_pk)
    assert question.status == "rejected"
    assert question.admin_note == note

@when("vaig a editar la pregunta d'un altre usuari")
def step_go_edit_other_user_question(context):
    context.browser.visit(get_base_url() + f"/questions/{context.question_pk}/edit/")


@then("hauria de veure un error o redirecció")
def step_should_see_error_or_redirect(context):
    assert (
        "Not Found" in context.browser.html
        or "/questions/" in context.browser.url
        or "/login/" in context.browser.url
    )