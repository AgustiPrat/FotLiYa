from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import ProposedQuestion, GameSession, Player


class AuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_incorrecte(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'incorrectes')

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class ProposedQuestionTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        self.question = ProposedQuestion.objects.create(
            text='Aquesta és una pregunta de prova per al test',
            category='humor',
            created_by=self.user,
            status='pending'
        )

    def test_question_list_requereix_login(self):
        response = self.client.get(reverse('question_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_question_list_autenticat(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('question_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aquesta és una pregunta')

    def test_crear_pregunta_correctament(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('question_create'), {
            'text': 'Aquesta és una nova pregunta de prova',
            'category': 'humor',
            'mechanics': 'votació',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ProposedQuestion.objects.filter(
            text='Aquesta és una nova pregunta de prova'
        ).exists())

    def test_crear_pregunta_text_curt(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('question_create'), {
            'text': 'Curta',
            'category': 'humor',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ProposedQuestion.objects.filter(text='Curta').exists())

    def test_editar_pregunta_propia(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('question_edit', args=[self.question.pk]),
            {
                'text': 'Pregunta modificada correctament per al test',
                'category': 'cultura',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, 'Pregunta modificada correctament per al test')

    def test_editar_pregunta_dun_altre(self):
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(
            reverse('question_edit', args=[self.question.pk]),
            {
                'text': 'Intent de modificació no autoritzat',
                'category': 'humor',
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_eliminar_pregunta_propia(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('question_delete', args=[self.question.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ProposedQuestion.objects.filter(pk=self.question.pk).exists())

    def test_eliminar_pregunta_dun_altre(self):
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(
            reverse('question_delete', args=[self.question.pk])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(ProposedQuestion.objects.filter(pk=self.question.pk).exists())


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass123'
        )
        self.question = ProposedQuestion.objects.create(
            text='Pregunta pendent de revisió per al test',
            category='humor',
            created_by=self.user,
            status='pending'
        )

    def test_admin_panel_requereix_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('admin_questions'))
        self.assertEqual(response.status_code, 302)

    def test_admin_panel_accessible_per_admin(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_questions'))
        self.assertEqual(response.status_code, 200)

    def test_aprovar_pregunta(self):
        self.client.login(username='admin', password='adminpass123')
        self.client.post(reverse('approve_question', args=[self.question.pk]))
        self.question.refresh_from_db()
        self.assertEqual(self.question.status, 'approved')

    def test_rebutjar_pregunta(self):
        self.client.login(username='admin', password='adminpass123')
        self.client.post(
            reverse('reject_question', args=[self.question.pk]),
            {'admin_note': 'Massa ofensiva'}
        )
        self.question.refresh_from_db()
        self.assertEqual(self.question.status, 'rejected')
        self.assertEqual(self.question.admin_note, 'Massa ofensiva')


class GameTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_game_setup(self):
        response = self.client.get(reverse('game_setup'))
        self.assertEqual(response.status_code, 200)

    def test_game_setup_minim_2_jugadors(self):
        response = self.client.post(reverse('game_setup'), {'num_players': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mínim')

    def test_game_sense_jugadors_redirigeix(self):
        response = self.client.get(reverse('game'))
        self.assertEqual(response.status_code, 302)

