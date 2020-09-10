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
        _list = List.objects.create()
        response = self.client.get(f"/lists/{_list.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item 1", list=other_list)
        Item.objects.create(text="other list item 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

    def test_passes_correct_list_to_templates(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/new_item/",
            data={"item_text": "A new item for an existing list."}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()

        self.assertEqual(new_item.text, "A new item for an existing list.")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/new_item/",
            data={"item_text": "A new item for an existing list."}
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")