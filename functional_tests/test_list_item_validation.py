from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Micah goes to the home page and accidentally tries to submit an empty list item. She hits enter on the
        # empty input box

        # The home page refreshes, and there is an error message saying that the list cannot be blank

        # She tries again with some text for the item, which now works

        # Perversely, she decides to submit a second blank item

        # She receives a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail("write me!")
