from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .models import Item, List
from .views import home_page


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        _list = List()
        _list.save()

        first_item = Item.objects.create(text="The first (ever) list item", list=_list)
        second_item = Item.objects.create(text="Item the second", list=_list)

        saved_list = List.objects.first()
        self.assertEqual(saved_list, _list)

        saved_items = Item.objects.all()
        self.assertEquals(saved_items.count(), 2)

        first_saved_item, second_saved_item = saved_items
        self.assertEquals(first_saved_item.text, first_item.text)
        self.assertEquals(first_saved_item.list, _list)
        self.assertEquals(second_saved_item.text, second_item.text)
        self.assertEquals(second_saved_item.list, _list)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        response = self.client.post("/lists/", data={"item_text": "A new list item"})

        self.assertEquals(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEquals(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/", data={"item_text": "A new list item"})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')