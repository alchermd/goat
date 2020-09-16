import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):
    MAX_WAIT = 10

    def setUp(self):
        self.browser = webdriver.Firefox()

        if staging_server := os.environ.get("STAGING_SERVER"):
            self.live_server_url = "http://" + staging_server

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

    def test_can_start_a_list_for_one_user(self):
        # Micah has heard about a cool new online to-do app. She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists.
        self.assertIn("To Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("To Do", header_text)

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

        # She visits that URL -- her to-do list is still there.

        # Satisfied, she goes back to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Micah starts a new to-do list.
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("new_item")
        inputbox.send_keys("Buy watercolor paint")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_list_in_table("1. Buy watercolor paint")

        # She notices that her list has a unique URL.
        micah_list_url = self.browser.current_url
        self.assertRegex(micah_list_url, '/lists/.+')

        # Now a new user, Alcher, comes along to the site.

        ## We use a new browser session to make sure that no information of Micah's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Alcher visits the home page. There is no sign of Micah's list.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy watercolor paint', page_text)

        # Alcher starts a new list by enter a new item. He is less interesting than Micah...
        inputbox = self.browser.find_element_by_id("new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_list_in_table("1. Buy milk")

        # Alcher gets his own URL.
        alcher_list_url = self.browser.current_url
        self.assertRegex(alcher_list_url, '/lists/.+')
        self.assertNotEqual(alcher_list_url, micah_list_url)

        # Again, there is no trace of Micah's list.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy watercolor paint', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep.

    def test_layout_and_styling(self):
        # Micah goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices that the input box is nicely centered
        inputbox = self.browser.find_element_by_id("new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input there is nicely centered too
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_list_in_table("1. testing")
        inputbox = self.browser.find_element_by_id("new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )
