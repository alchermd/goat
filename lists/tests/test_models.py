from django.test import TestCase

from lists.models import Item, List


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
