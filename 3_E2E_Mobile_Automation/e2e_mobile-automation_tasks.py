import unittest
from time import sleep
from appium import webdriver  #, TouchAction
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys



capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    app='C:\\Users\\human-c137\\Documents\\GitHub\\soar_qa_assessment\\3_E2E_Mobile_Automation/WikipediaSample.apk',
    language='en',
    locale='US'
)


appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.short_wait = 3
        self.min_wait = 1
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        try:
            # dismiss warning about version of android being too new
            # //android.widget.Button[@resource-id="android:id/button1"]
            ok_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.Button[@resource-id="android:id/button1"]')
            ok_el.click()
        except Exception as e:
            print(e)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()


    def test_mobile_task1(self) -> None:
        '''
        scroll down, cycle thru bottom buttons on app, scroll up
        '''


        # scroll to bottom
        window_size = self.driver.get_window_size()
        mid_X = window_size['width'] / 2
        top_Y = window_size['height'] * .85
        bottom_Y = window_size['height'] * 0.15
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, 'touch'))
        num_times_scroll = 5
        for x in range(num_times_scroll):
            actions.w3c_actions.pointer_action.move_to_location(mid_X, top_Y)
            actions.w3c_actions.pointer_action.click_and_hold()
            actions.w3c_actions.pointer_action.move_to_location(mid_X,bottom_Y)
            actions.w3c_actions.pointer_action.release()
            actions.w3c_actions.perform()
            sleep(self.min_wait)

        sleep(self.short_wait)
        # click on my lists button and wait 3s
        # //android.widget.FrameLayout[@content-desc="My lists"]
        my_lists_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.FrameLayout[@content-desc="My lists"]')
        my_lists_el.click()
        sleep(self.short_wait)

        # click on history button and wait 3s
        #//android.widget.FrameLayout[@content-desc="History"]
        history_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.FrameLayout[@content-desc="History"]')
        history_el.click()
        sleep(self.short_wait)

        # click on nearby button and wait 3s
        # //android.widget.FrameLayout[@content-desc="Nearby"]
        nearby_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.FrameLayout[@content-desc="Nearby"]')
        nearby_el.click()
        sleep(self.short_wait)

        # click browse
        #//android.widget.TextView[@content-desc="Search Wikipedia"]
        #//android.widget.FrameLayout[@content-desc="Explore"]
        browse_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.FrameLayout[@content-desc="Explore"]')
        browse_el.click()

        # scroll up to top
        for x in range(num_times_scroll):
            actions.w3c_actions.pointer_action.move_to_location(mid_X, bottom_Y)
            actions.w3c_actions.pointer_action.click_and_hold()
            actions.w3c_actions.pointer_action.move_to_location(mid_X,top_Y)
            actions.w3c_actions.pointer_action.release()
            actions.w3c_actions.perform()
            sleep(self.min_wait)

        sleep(self.short_wait)


    def test_mobile_task2(self) -> None:
        '''
        search new york, assert search bar expanded with results, close search go home
        '''
        # navigate thru search bars
        # //android.widget.LinearLayout[@resource-id="org.wikipedia.alpha:id/search_container"]
        search_bar_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.LinearLayout[@resource-id="org.wikipedia.alpha:id/search_container"]')
        search_bar_el.click()
        sleep(self.min_wait)
        # //android.widget.AutoCompleteTextView[@resource-id="org.wikipedia.alpha:id/search_src_text"]
        new_search_bar_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.AutoCompleteTextView[@resource-id="org.wikipedia.alpha:id/search_src_text"]')
        new_search_bar_el.click()

        # search for query / New York
        query = "New York"
        new_search_bar_el.send_keys(query)
        #(//android.widget.LinearLayout[@resource-id="org.wikipedia.alpha:id/page_list_item_container"])
        sleep(self.short_wait)
        # assert results exist by ensuring result count > 0
        result_elems = self.driver.find_elements(by=AppiumBy.XPATH, value='//android.widget.LinearLayout[@resource-id="org.wikipedia.alpha:id/page_list_item_container"]')
        num_search_results = len(result_elems)
        self.assertTrue(num_search_results > 0)

        # //android.widget.ImageView[@content-desc="Clear query"]
        exit_search_elem = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageView[@content-desc="Clear query"]')
        exit_search_elem.click()
        sleep(self.min_wait)
        exit_search_elem.click()


    def test_mobile_task3(self) -> None:
        '''
        go into settings, toggle all options, return home
        '''
        # get to settings menu
        # //android.widget.TextView[@content-desc="More options"]
        ellipses_menu_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@content-desc="More options"]')
        ellipses_menu_el.click()
        sleep(self.min_wait)
        # //android.widget.TextView[@resource-id="org.wikipedia.alpha:id/explore_overflow_settings"]
        settings_menu_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.TextView[@resource-id="org.wikipedia.alpha:id/explore_overflow_settings"]')
        settings_menu_el.click()

        sleep(self.short_wait)

        # toggle options
        # (//android.widget.Switch[@resource-id="org.wikipedia.alpha:id/switchWidget"])[1]
        img_toggle_el = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.Switch[@resource-id="org.wikipedia.alpha:id/switchWidget"])[1]')
        img_toggle_el.click()

        # (//android.widget.Switch[@resource-id="org.wikipedia.alpha:id/switchWidget"])[2]
        preview_link_toggle_el = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.Switch[@resource-id="org.wikipedia.alpha:id/switchWidget"])[2]')
        preview_link_toggle_el.click()

        # (//android.widget.Switch[@resource-id="org.wikipedia.alpha:id/switchWidget"])[3]
        send_usage_toggle_el = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.Switch[@resource-id="org.wikipedia.alpha:id/switchWidget"])[3]')
        send_usage_toggle_el.click()

        # (//android.widget.Switch[@resource-id="org.wikipedia.alpha:id/switchWidget"])[4]
        send_crash_toggle_el = self.driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.Switch[@resource-id="org.wikipedia.alpha:id/switchWidget"])[4]')
        send_crash_toggle_el.click()

        # go home
        # //android.widget.ImageButton[@content-desc="Navigate up"]
        go_home_el = self.driver.find_element(by=AppiumBy.XPATH, value='//android.widget.ImageButton[@content-desc="Navigate up"]')
        go_home_el.click()

if __name__ == '__main__':
    unittest.main()