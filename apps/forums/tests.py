from django.test import TestCase
from django.contrib.auth.models import User
from .models import Forums, ForumsReplies, ForumView
from django.utils import timezone
import datetime

class ForumsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.forum = Forums.objects.create(
            user=self.user,
            title="Test Forum",
            content="This is a test forum content."
        )

    def test_forum_creation(self):
        self.assertEqual(self.forum.title, "Test Forum")
        self.assertEqual(self.forum.content, "This is a test forum content.")
        self.assertEqual(self.forum.forums_views, 0)
        self.assertEqual(self.forum.forums_replies_counts, 0)
        self.assertFalse(self.forum.is_hot)

    def test_increment_views(self):
        self.forum.increment_views()
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forums_views, 1)

    def test_user_likes_forum(self):
        self.assertFalse(self.forum.user_has_liked(self.user))
        self.forum.forums_likes.add(self.user)
        self.assertTrue(self.forum.user_has_liked(self.user))
        self.forum.forums_likes.remove(self.user)
        self.assertFalse(self.forum.user_has_liked(self.user))

    def test_hot_flag_toggle(self):
        self.forum.is_hot = True
        self.forum.save()
        self.forum.refresh_from_db()
        self.assertTrue(self.forum.is_hot)

        self.forum.is_hot = False
        self.forum.save()
        self.forum.refresh_from_db()
        self.assertFalse(self.forum.is_hot)

    def test_get_duration_since_created(self):
        duration = self.forum.get_duration_since_created()
        self.assertIsInstance(duration, datetime.timedelta)
        self.assertTrue(duration.total_seconds() <= 0)


class ForumsRepliesModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='replyuser', password='password123')
        self.forum = Forums.objects.create(
            user=self.user,
            title="Forum with replies",
            content="Forum content"
        )
        self.reply = ForumsReplies.objects.create(
            forums=self.forum,
            user=self.user,
            replies_content="This is a test reply"
        )

    def test_reply_creation(self):
        self.assertEqual(self.reply.replies_content, "This is a test reply")
        self.assertEqual(self.reply.forums, self.forum)
        self.assertEqual(self.reply.user, self.user)

    def test_user_likes_reply(self):
        self.assertFalse(self.reply.user_has_liked(self.user))
        self.reply.forums_replies_likes.add(self.user)
        self.assertTrue(self.reply.user_has_liked(self.user))
        self.reply.forums_replies_likes.remove(self.user)
        self.assertFalse(self.reply.user_has_liked(self.user))

    def test_get_duration_since_created(self):
        duration = self.reply.get_duration_since_created()
        self.assertIsInstance(duration, datetime.timedelta)
        self.assertTrue(duration.total_seconds() <= 0)


class ForumViewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="viewuser", password="password123")
        self.forum = Forums.objects.create(user=self.user, title="Forum View Test", content="Content")
        self.view = ForumView.objects.create(forum=self.forum, user=self.user)

    def test_forum_view_creation(self):
        self.assertEqual(str(self.view), f"{self.user.username} viewed {self.forum.title}")

    def test_forum_view_unique_constraint(self):
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError):
            ForumView.objects.create(forum=self.forum, user=self.user)
