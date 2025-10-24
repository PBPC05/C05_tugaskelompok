# ...existing code...
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from apps.authentication.models import UserProfile, BanHistory

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # regular user
        self.user = User.objects.create_user(username='ammar', email='ammar@example.com', password='password123')
        # superuser
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        # another user for admin actions
        self.other = User.objects.create_user(username='faiq', email='faiq@example.com', password='secret123')

    def test_userprofile_signal_created_on_user_creation(self):
        u = User.objects.create_user(username='newuser', password='pw123456')
        # signal should create profile
        self.assertTrue(hasattr(u, 'profile'))
        self.assertIsInstance(u.profile, UserProfile)

    def test_banhistory_model_and_str(self):
        bh = BanHistory.objects.create(user=self.other, banned_by=self.admin, reason="test ban")
        self.assertIn("banned at", str(bh))
        self.assertTrue(bh.is_active)

    def test_register_view_get_and_post_creates_user_and_profile(self):
        url = reverse('authentication:register')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # post valid data
        data = {
            'username': 'erik',
            'password1': 'complexpassword1',
            'password2': 'complexpassword1'
        }
        resp = self.client.post(url, data, follow=True)
        # redirect to login
        self.assertContains(resp, "Please login", status_code=200, msg_prefix="Should notify to login")
        self.assertTrue(User.objects.filter(username='erik').exists())
        user = User.objects.get(username='erik')
        self.assertTrue(hasattr(user, 'profile'))

    def test_login_and_logout_flow(self):
        login_url = reverse('authentication:login')
        # login
        resp = self.client.post(login_url, {'username': 'ammar', 'password': 'password123'}, follow=True)
        self.assertTrue('_auth_user_id' in self.client.session)
        messages = list(get_messages(resp.wsgi_request))
        # should welcome user
        self.assertTrue(any('Welcome back' in str(m) or 'Welcome' in str(m) for m in messages))
        # logout
        resp = self.client.get(reverse('authentication:logout'), follow=True)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertContains(resp, "You have been logged out", status_code=200)

    def test_edit_user_updates_fields_and_profile(self):
        edit_url = reverse('authentication:edit_user', args=[self.other.id])
        self.client.login(username='admin', password='adminpass')
        data = {
            'username': 'faiq_updated',
            'email': 'faiq2@example.com',
            'is_active': 'on',
            # profile fields (if implemented in view)
            'phone_number': '+628123',
            'address': 'New Address',
            'bio': 'Updated bio',
        }
        resp = self.client.post(edit_url, data, follow=True)
        self.other.refresh_from_db()
        self.assertEqual(self.other.username, 'faiq_updated')
        self.assertEqual(self.other.email, 'faiq2@example.com')
        # profile should exist and be updated if view handles it
        if hasattr(self.other, 'profile'):
            self.assertIn('Updated', self.other.profile.bio or '')

    def test_delete_user_by_admin_and_prevent_self_deletion(self):
        # admin cannot delete self
        self.client.login(username='admin', password='adminpass')
        resp = self.client.get(reverse('authentication:delete_user', args=[self.admin.id]), follow=True)
        self.assertTrue(User.objects.filter(id=self.admin.id).exists())
        # admin can delete other user
        resp = self.client.get(reverse('authentication:delete_user', args=[self.other.id]), follow=True)
        self.assertFalse(User.objects.filter(id=self.other.id).exists())

    def test_ban_user_creates_history_and_toggles_status(self):
        self.client.login(username='admin', password='adminpass')
        url = reverse('authentication:ban_user', args=[self.user.id])
        # ban (toggle off)
        resp = self.client.get(url, follow=True)
        self.user.refresh_from_db()
        # if view implemented, user should become inactive and a BanHistory should be created
        self.assertFalse(self.user.is_active)
        self.assertTrue(BanHistory.objects.filter(user=self.user).exists())
        last = BanHistory.objects.filter(user=self.user).first()
        self.assertTrue(last.is_active)
        # unban (toggle back on)
        resp = self.client.get(url, follow=True)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        # a second BanHistory record may be created to record unban
        self.assertGreaterEqual(BanHistory.objects.filter(user=self.user).count(), 1)

    def test_view_profile_visibility_for_banned_users(self):
        # ban target user
        self.user.is_active = False
        self.user.save()
        # normal user cannot view banned profile (should 404)
        self.client.login(username='ammar', password='password123')
        resp = self.client.get(reverse('authentication:view_profile', args=[self.user.username]))
        self.assertEqual(resp.status_code, 404)
        # admin can view
        self.client.login(username='admin', password='adminpass')
        resp = self.client.get(reverse('authentication:view_profile', args=[self.user.username]))
        self.assertEqual(resp.status_code, 200)