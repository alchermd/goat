import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_list_in_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Micah has heard about a cool new online to-do app. She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists.
        self.assertIn("To Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual("To Do", header_text)

        # She is invited to enter a to-do item straight away.
        inputbox = self.browser.find_element_by_id("new_item")
        self.assertEqual(
            "Enter a to-do item",
            inputbox.get_attribute("placeholder"),
        )

        # She types "Buy watercolor paint" into a text box (Micah's hobby is painting pictures of flamingoes).
        inputbox.send_keys("Buy watercolor paint")

        # When she hits enter, the page updates, and now the page lists:
        # "1. Buy watercolor paint" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_list_in_table("1. Buy watercolor paint")

        # There is still a text box inviting her to add another item. She enters "Add water to the watercolor paint".
        inputbox = self.browser.find_element_by_id("new_item")
        inputbox.send_keys("Add water to the watercolor paint")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list.
        self.wait_for_row_list_in_table("1. Buy watercolor paint")
        self.wait_for_row_list_in_table("2. Add water to the watercolor paint")

        # Micah wonders whether the site will remember her list. Then she sees that the site has generated a unique URL for
        # her -- there is some explanatory text to that effect.
        self.fail("Finish the test!")

        # She visits that URL -- her to-do list is still there.

        # Satisfied, she goes back to sleep.
