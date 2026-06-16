from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class GymManagementComprehensiveTests(TestCase):

    def setUp(self):
        self.klient = User.objects.create_user(
            username='jan_kowalski',
            email='jan@kowalski.pl',
            password='BezpieczneHaslo123!'
        )

        self.admin = User.objects.create_superuser(
            username='admin_testowy',
            email='admin@test.pl',
            password='AdminHaslo123!'
        )

    def test_user_model_creation(self):
        uzytkownik = User.objects.get(username='jan_kowalski')
        self.assertEqual(uzytkownik.email, 'jan@kowalski.pl')
        self.assertFalse(uzytkownik.is_staff)

    def test_superuser_permissions(self):
        administrator = User.objects.get(username='admin_testowy')
        self.assertTrue(administrator.is_staff)
        self.assertTrue(administrator.is_superuser)

    def test_strona_glowna_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_rejestracja_podstrona_status_code(self):
        response = self.client.get('/rejestracja/')
        self.assertEqual(response.status_code, 200)

    def test_panel_admina_redirect_dla_anonima(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_poprawne_logowanie_uzytkownika(self):
        login_success = self.client.login(username='jan_kowalski', password='BezpieczneHaslo123!')
        self.assertTrue(login_success)

    def test_bledne_logowanie_uzytkownika(self):
        login_success = self.client.login(username='jan_kowalski', password='ZleHaslo!')
        self.assertFalse(login_success)