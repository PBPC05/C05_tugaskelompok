from django.test import TestCase
from django.contrib.auth.models import User
from .models import Forums, ForumsReplies
import datetime
import uuid

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
        self.assertEqual(self.forum.forums_likes, 0)
        self.assertFalse(self.forum.is_hot)

    def test_increment_views(self):
        self.forum.increment_views()
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forums_views, 1)

    def test_increment_and_decrement_likes(self):
        self.forum.increment_likes()
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forums_likes, 1)
        self.forum.decrement_likes()
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forums_likes, 0)

    def test_increment_and_decrement_replies(self):
        self.forum.increment_replies_counts()
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forums_replies_counts, 1)
        self.forum.decrement_replies_counts()
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forums_replies_counts, 0)

    def test_hot_flags(self):
        self.forum.is_hot_True()
        self.forum.refresh_from_db()
        self.assertTrue(self.forum.is_hot)
        self.forum.is_hot_False()
        self.forum.refresh_from_db()
        self.assertFalse(self.forum.is_hot)

    def test_get_duration_since_created(self):
        duration = self.forum.get_duration_since_created()
        self.assertIsInstance(duration, datetime.timedelta)
        self.assertTrue(duration.total_seconds() < 0)


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
        self.assertEqual(self.reply.forums_replies_likes, 0)
        self.assertEqual(self.reply.forums, self.forum)
        self.assertEqual(self.reply.user, self.user)

    def test_increment_and_decrement_likes(self):
        self.reply.increment_likes()
        self.reply.refresh_from_db()
        self.assertEqual(self.reply.forums_replies_likes, 1)
        self.reply.decrement_likes()
        self.reply.refresh_from_db()
        self.assertEqual(self.reply.forums_replies_likes, 0)

    def test_get_duration_since_created(self):
        duration = self.reply.get_duration_since_created()
        self.assertIsInstance(duration, datetime.timedelta)
        self.assertTrue(duration.total_seconds() < 0)
