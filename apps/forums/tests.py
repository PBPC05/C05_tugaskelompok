from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Forums, ForumsReplies, ForumView
import uuid

class ForumsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")
        self.forum = Forums.objects.create(user=self.user1, title="Test Forum", content="This is a test forum.")
        self.client = Client()

    def test_forum_creation(self):
        self.assertEqual(self.forum.title, "Test Forum")
        self.assertEqual(self.forum.forums_views, 0)
        self.assertEqual(self.forum.forums_replies_counts, 0)

    def test_forum_view_increment(self):
        response = self.client.get(reverse("forums:show_forum_detail", args=[self.forum.forums_id]))
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forums_views, 1)

        self.client.login(username="user2", password="pass1234")
        response = self.client.get(reverse("forums:show_forum_detail", args=[self.forum.forums_id]))
        self.forum.refresh_from_db()
        self.assertEqual(self.forum.forums_views, 2)

    def test_forum_like_toggle(self):
        self.client.login(username="user2", password="pass1234")
        url = reverse("forums:like_forum", args=[self.forum.forums_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.forum.refresh_from_db()
        self.assertTrue(self.forum.user_has_liked(self.user2))

        response = self.client.post(url)
        self.forum.refresh_from_db()
        self.assertFalse(self.forum.user_has_liked(self.user2))

    def test_forum_create_edit_delete(self):
        self.client.login(username="user2", password="pass1234")

        create_url = reverse("forums:create_forum")
        response = self.client.post(create_url, {"title": "New Forum", "content": "Content"})
        self.assertEqual(response.status_code, 302)
        new_forum = Forums.objects.get(title="New Forum")
        self.assertEqual(new_forum.user, self.user2)

        edit_url = reverse("forums:edit_forum", args=[new_forum.forums_id])
        response = self.client.post(edit_url, {"title": "Updated Forum", "content": "Updated"})
        self.assertEqual(response.status_code, 302)
        new_forum.refresh_from_db()
        self.assertEqual(new_forum.title, "Updated Forum")

        delete_url = reverse("forums:delete_forum", args=[new_forum.forums_id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Forums.objects.filter(pk=new_forum.forums_id).exists())

    def test_reply_create_like_delete(self):
        self.client.login(username="user2", password="pass1234")
        reply_url = reverse("forums:create_reply", args=[self.forum.forums_id])

        response = self.client.post(reply_url, {"replies_content": "This is a reply"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.forum.forum_replies.count(), 1)
        reply = self.forum.forum_replies.first()
        self.assertEqual(reply.replies_content, "This is a reply")
        self.assertEqual(reply.user, self.user2)

        like_url = reverse("forums:like_reply", args=[reply.id])
        response = self.client.post(like_url)
        reply.refresh_from_db()
        self.assertTrue(reply.user_has_liked(self.user2))

        response = self.client.post(like_url)
        reply.refresh_from_db()
        self.assertFalse(reply.user_has_liked(self.user2))

        delete_url = reverse("forums:delete_reply", args=[reply.id])
        response = self.client.post(delete_url)
        self.assertFalse(ForumsReplies.objects.filter(pk=reply.id).exists())

    def test_load_more_replies(self):
        self.client.login(username="user2", password="pass1234")
        for i in range(10):
            ForumsReplies.objects.create(forums=self.forum, user=self.user1, replies_content=f"Reply {i+1}")
        
        url = reverse("forums:load_more_replies", args=[self.forum.forums_id])
        response = self.client.post(url, {"offset": 0, "limit": 5})
        data = response.json()
        self.assertEqual(len(data["replies"]), 5)
