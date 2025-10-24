from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import News, Comment
import uuid

# Create your tests here.
class NewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="Verstappen", password="1234")
        self.newsItem = News.objects.create(title="News Test", content="This is news", category="other", is_featured=True)
        self.comment = Comment.objects.create(news=self.newsItem, content="This is a comment")

    def test_news_model(self):
        self.assertEqual(self.newsItem.title, "News Test")
        self.assertEqual(self.newsItem.content, "This is news")
        self.assertEqual(self.newsItem.category, "other")
        self.assertEqual(self.newsItem.is_featured, True)
        self.assertEqual(self.newsItem.news_views, 0)
        self.assertEqual(self.newsItem.news_comments, 0)

    def test_news_views(self):
        response = self.client.get(reverse("news:show_news_detail", args=[self.newsItem.id]))
        self.newsItem.refresh_from_db()
        self.assertEqual(self.newsItem.news_views, 1)

    def test_news_edit(self):
        self.client.login(username="Verstappen", password="1234")

        data = {
            "title": "News Test 2",
            "content": "This is another news",
            "category": "driver",
            "thumbnail": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/2022_Honda_Civic_Touring_in_Lunar_Silver_Metallic%2C_Front_Left%2C_05-10-2022.jpg/1920px-2022_Honda_Civic_Touring_in_Lunar_Silver_Metallic%2C_Front_Left%2C_05-10-2022.jpg"
            # is_featured is absent
        }

        response = self.client.post(reverse("news:edit_news_ajax", args=[self.newsItem.id]), data)
        self.newsItem.refresh_from_db()

        self.assertEqual(self.newsItem.title, "News Test 2")
        self.assertEqual(self.newsItem.content, "This is another news")
        self.assertEqual(self.newsItem.category, "driver")
        self.assertNotEqual(self.newsItem.thumbnail, None)
        self.assertEqual(self.newsItem.is_featured, False)

    def test_news_create_delete(self):
        self.client.login(username="Verstappen", password="1234")

        create_url = reverse("news:create_news_ajax")
        response = self.client.post(create_url, {"title": "New News", "content": "New News Content", "category": "other", "is_featured": True})
        self.assertEqual(response.status_code, 302)
        new_news = News.objects.get(title="New News")
        self.assertEqual(new_news.user, self.user)

        delete_url = reverse("news:delete_news", args=[new_news.id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(News.objects.filter(pk=new_news.id).exists())

    def test_comment_model(self):
        self.assertEqual(self.comment.content, "This is a comment")
        self.assertEqual(self.comment.news, self.newsItem)

    def test_comment_create_delete(self):
        self.client.login(username="Verstappen", password="1234")

        create_url = reverse("news:post_comment", args=[self.newsItem.id])
        response = self.client.post(create_url, {"comment-body": "New Comment"})
        self.assertEqual(response.status_code, 302)
        new_comment = Comment.objects.get(content="New Comment")
        self.assertEqual(new_comment.user, self.user)

        delete_url = reverse("news:delete_comment", args=[self.newsItem.id, new_comment.id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(News.objects.filter(pk=new_comment.id).exists())
