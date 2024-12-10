import unittest
from time import sleep

from owasp_juice_utils import *


class TestJuiceShop(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = get_webdriver(target_browser=Browser.CHROME)  # also support Browser.FIREFOX and Browser.EDGE
        self.driver.get(owasp_juice_shop_url)
        dismiss_owasp_juice_popups(self.driver)


    def tearDown(self) -> None:
        if self.driver:
            self.driver.close()
            self.driver.quit()


    def test_web_task1(self) -> None:
        '''
        change number of items per page to max and verify all displayed
        by counting item tiles and comparing values
        '''
        max_per_pg = 48
        change_items_per_page(self.driver, max_per_pg)
        expect_num_items = get_num_items_on_page_bottom_bar(self.driver)
        actual_num_items  = count_num_items_on_cur_page(self.driver)
        self.assertEqual(expect_num_items, actual_num_items, f"# of items did not match, expected {expect_num_items} but found {actual_num_items}")


    def test_web_task2(self) -> None:
        '''
        click on product, test popup is triggered, test popup has img, check if reviews exist, if so expand bar, wait, exit
        '''
        click_product_by_name(self.driver, "Apple Juice")
        sleep(def_wait_time)
        popup_elements = self.driver.find_elements(By.XPATH, '//div[@class="cdk-overlay-pane"]') # top most html tag [div] associated with popup
        num_popup_elements = len(popup_elements)
        expected_num_popups = 1
        self.assertEqual(expected_num_popups, num_popup_elements,
            f"Expected {expected_num_popups} and instead found {num_popup_elements}")

        target_popup = popup_elements[0]
        popup_img = target_popup.find_element(By.XPATH, '//img[@class="img-thumbnail"]')
        self.assertTrue(popup_img.is_displayed(), "Popup image is NOT being displayed")

        infobar_num_reviews = get_num_product_reviews(self.driver)
        counted_num_reviews = 0
        if infobar_num_reviews > 0:
            # <mat-expansion-panel _ngcontent-mfm-c42="" aria-label="Expand for Reviews"
            review_bar_elem = target_popup.find_element(By.XPATH, '//mat-expansion-panel[@aria-label="Expand for Reviews"]')
            review_bar_elem.click()
            sleep(min_wait_time)
            # <div _ngcontent-mfm-c42="" class="comment ng-star-inserted">
            review_comments_elems = target_popup.find_elements(By.XPATH, '//div[contains(@class, "comment")]')
            counted_num_reviews   = len(review_comments_elems)

        sleep(def_wait_time)
        # <button _ngcontent-mfm-c42="" mat-stroked-button="" mat-dialog-close="" aria-label="Close Dialog" class="mat-focus-indicator close-dialog buttons mat-stroked-button mat-button-base" type="button">
        close_popup_btn = target_popup.find_element(By.XPATH, '//button[@aria-label="Close Dialog"]')
        scroll_to_given_element(self.driver, close_popup_btn)
        close_popup_btn.click()

        # ideally only one assertion per test function, and test would end on assert


    def test_web_task3(self) -> None:
        '''
        test register user fields have error validation messages then register user and test for successful registration msg
        '''
        navigate_to_user_registration(self.driver)


        #self.driver.get(owasp_juice_login_url)
        # shortcut but direction state to navigate not url hop
        sleep(def_wait_time)

        #dismiss_owasp_juice_popups(self.driver)


        click_email_field(self.driver)
        click_user_reg_title(self.driver)
        email_err = get_field_errors(self.driver)
        self.assertIsNotNone(email_err, f"Expected email input field error message, instead found {email_err}")


        self.driver.refresh() # to reset error msg(s)
        sleep(min_wait_time)

        click_password_field(self.driver)
        click_user_reg_title(self.driver)
        pw_err = get_field_errors(self.driver)
        self.assertIsNotNone(pw_err, f"Expected password input field error message, instead found {pw_err}")

        self.driver.refresh()
        sleep(min_wait_time)


        click_repeat_password_field(self.driver)
        click_user_reg_title(self.driver)
        rpw_err = get_field_errors(self.driver)
        self.assertIsNotNone(rpw_err, f"Expected repeat password input field error message, instead found {rpw_err}")

        self.driver.refresh()
        sleep(min_wait_time)


        click_security_question_field(self.driver)
        #click_user_reg_title(self.driver) # click intercept error
        actions = ActionChains(self.driver)
        sec_quest_field = self.driver.find_element(By.XPATH, '//mat-select[@name="securityQuestion"]')
        actions.move_to_element(sec_quest_field).perform()
        actions.move_by_offset(-333, 0).click().perform() # click far enough left that not in drop down but not cclicking something else
        # ToDo be real fancy and make it based off percentage layout and use webdriver options to set browser dimensions
        sleep(min_wait_time)
        sq_err = get_field_errors(self.driver)
        self.assertIsNotNone(sq_err, f"Expected security question field error message, instead found {sq_err}")

        self.driver.refresh()
        sleep(min_wait_time)


        click_security_answer_field(self.driver)
        click_user_reg_title(self.driver)
        sa_err = get_field_errors(self.driver)
        self.assertIsNotNone(sa_err, f"Expected security answer field error message, instead found {sa_err}")
        self.driver.refresh()
        sleep(min_wait_time)

        click_password_advice(self.driver)
        sleep(min_wait_time)
        register_test_user(self.driver)
        #success_msg = "Registration completed successfully. You can now log in."
        # make both lower case so that way we don't have to worry about case sensitivity
        success_prefix = "Registration completed successfully.".lower()
        registration_msg = get_registration_message(self.driver).lower()

        self.assertTrue(success_prefix in registration_msg, f"Registration unsuccessful, could not find {success_prefix} in {registration_msg}" )

        login_with_test_user(self.driver)

        # no assertion that login with new user was successful?


    def test_web_task4(self) -> None:
        '''
        login with test user, adds first five products to basket, inc apple juice, delete apple juice, check price changed
        navigate through entirety of checkout (add addy info, test wallet empty, add cc info, click thru confirmation)
        '''
        try:
            # since unittests meant to be ran in any order, possibility that test user to login won't exist
            navigate_to_user_registration(self.driver)
            register_test_user(self.driver, use_random_email=False)
        except Exception as e:
            print(f"Error registering default test user. \nSee following for error details; {e}")
            self.fail("unable to create default test user, unable to proceed with test, marking as FAILED.")
        login_with_test_user(self.driver)

        sleep(def_wait_time)
        all_product_elements  = get_all_product_elements(self.driver)
        first_five_prod_elems = all_product_elements[:5]
        for cur_prod_elem in first_five_prod_elems:
            cur_prod_add_basket_btn = cur_prod_elem.find_element(By.XPATH, ".//button[@aria-label='Add to Basket']")
            scroll_to_given_element(self.driver, cur_prod_add_basket_btn)
            cur_prod_add_basket_btn.click()
            sleep(min_wait_time)
            cur_prod_popup_msg = get_angular_popup_msg(self.driver)
            self.assertIsNotNone(cur_prod_popup_msg, f"Expected a popup msg for adding to basket, instead found {cur_prod_popup_msg}")
            sleep(min_wait_time)


        navigate_to_basket(self.driver)
        five_product_price = get_current_basket_total_price(self.driver)
        increase_item_in_basket(self.driver, "Apple Juice")
        six_product_price = get_current_basket_total_price(self.driver)
        self.assertGreater(six_product_price, five_product_price, f"Expected increase product price {six_product_price} to be greater than {five_product_price}")


        delete_item_in_basket(self.driver, "Apple Juice")
        four_product_price = get_current_basket_total_price(self.driver)

        self.assertLess(four_product_price, six_product_price, f"Expected decrease product price {four_product_price} to be less than {six_product_price}")
        # overkill assertion below
        self.assertLess(four_product_price, five_product_price, f"Expected decrease product price {four_product_price} to be less than {five_product_price}")

        click_checkout_from_basket(self.driver)
        click_add_new_addy_from_chkout(self.driver)
        fill_out_addy_info(self.driver)
        select_addy_by_index(self.driver, 0)
        select_delivery_method_by_index(self.driver, 0)
        wallet_bal = get_wallet_balance_from_payment_options(self.driver)
        self.assertEqual(wallet_bal, 0, f"Expected wallet balance to be 0, instead found balance of {wallet_bal}")
        add_cc_info_at_payment_options(self.driver)
        select_cc_by_index_payment_options(self.driver, 0)
        go_to_order_review_from_payment_options(self.driver)
        checkout_at_order_review(self.driver)

        # again with not ending on assertion- just running to completion never a good idea to use as pass chk



if __name__ == '__main__':

    unittest.main()

