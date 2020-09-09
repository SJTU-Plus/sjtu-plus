from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Group


class TestCategoryPage(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create()
        self.group = Group.objects.create(category=self.category)

    def test_index_page(self):
        response = self.client.get(reverse('index', args=(self.category.id,)))
        self.assertEqual(response.status_code, 200)
