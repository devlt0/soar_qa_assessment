
from enum import Enum
from random import randint
from time import sleep
from unittest import TestCase

from selenium import webdriver
from selenium.common.exceptions import \
    TimeoutException, NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException, InvalidSelectorException
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class Browser(Enum):
    CHROME  = 1
    FIREFOX = 2
    EDGE    = 3
    #OPERA   = 4

owasp_juice_url = "https://juice-shop.herokuapp.com/#/"

long_wait_time = 10
def_wait_time = 3
min_wait_time = 1

def load_url( target_url:str = owasp_juice_url, target_browser:Browser = Browser.CHROME, wait_time_on_load:int=def_wait_time ) -> webdriver:
    driver_opts = None
    if target_browser == Browser.CHROME:
        driver_opts = ChromeOptions()
    elif target_browser == Browser.FIREFOX:
        driver_opts = FirefoxOptions()
    elif target_browser == Browser.EDGE:
        driver_opts = EdgeOptions()
    else:
        raise ValueError(f"Unsupported Browser provided; {target_browser}.  Valid values for target_browser in load_url are; { ['Browser.'+cur_mem.name for cur_mem in Browser] }")

    driver_opts.add_argument("--disable-gpu");
    driver_opts.add_argument("--disable-cache");
    driver_opts.add_argument("--disable-extensions");
    #driver_opts.add_argument("--headless");

    driver = None

    if target_browser == Browser.CHROME:
        driver = webdriver.Chrome(options=driver_opts)
    elif target_browser == Browser.FIREFOX:
        driver = webdriver.Firefox(options=driver_opts)
    elif target_browser == Browser.EDGE:
        driver = webdriver.Edge(options=driver_opts)

    driver.delete_all_cookies()

    driver.get(target_url)
    sleep(wait_time_on_load)

    return driver



def navigate_to_user_registration():
    pass

def register_user():
    pass

def login_with_user():
    pass



def navigate_to_basket():
    pass

def get_current_basket_total_price():
    pass

def inc_item_in_basket():
    pass

def dec_item_in_basket():
    pass


def navigate_to_checkout():
    pass

def form_fill_checkout_info():
    pass


def dismiss_owasp_juice_popups(given_webdriver:webdriver=None):
    try:
        cookie_btn = given_webdriver.find_element(By.XPATH, '//a[@aria-label="dismiss cookie message"]')
        cookie_btn.click()
        sleep(min_wait_time)
    except NoSuchElementException as does_not_exist_err:
        print(f"Could not find cookie popup close button. Please ensure said popup exists to dismiss. \nSee {does_not_exist_err}")

    try:
        dismiss_welcome_btn = given_webdriver.find_element(By.XPATH, '//button[@aria-label="Close Welcome Banner"]')
        dismiss_welcome_btn.click()
        sleep(min_wait_time)
    except NoSuchElementException as does_not_exist_err:
        print(f"Could not find welcome banner close button. Please ensure said Welcome Banner exists to dismiss. \nSee {does_not_exist_err}")




def scroll_to_bottom_of_page(given_webdriver:webdriver=None):
    given_webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scroll_to_given_element(given_webdriver:webdriver=None, target_element:WebElement=None):
    given_webdriver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", target_element)

def change_items_per_page(given_webdriver:webdriver=None, new_items_per_page:int = 48 ) -> bool:
    changed_to_new_ipp = False  #ipp items per page

    valid_items_per_page = [12, 24, 36, 48]
    target_selector = ""
    match new_items_per_page: #requires python 3.10+ for match case
        case 12:
            target_selector = "//mat-option[@id='mat-option-0']"
        case 24:
            target_selector = "//mat-option[@id='mat-option-1']"
        case 36:
            target_selector = "//mat-option[@id='mat-option-2']"
        case 48:
            target_selector = "//mat-option[@id='mat-option-3']"
        case _:
            raise ValueError(f"Invalid value; {new_items_per_page} . Accepted values for change_items_per_page are {valid_items_per_page}")

    # id="mat-select-0"
    try:
        items_per_page_menu = given_webdriver.find_element(By.XPATH, '//div[contains(@class, "mat-select-value")]')
    except NoSuchElementException as does_not_exist_err:
        print(f"Could not find menu to change items per page. \nSee {does_not_exist_err}")


    if items_per_page_menu.text == str(new_items_per_page):
        # do nothing, already have the number of items to display selected
        changed_to_new_ipp = True
        return changed_to_new_ipp

    given_webdriver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", items_per_page_menu)

    try:
        items_per_page_menu.click()
    except InvalidSelectorException as elem_not_in_view_err:
        print(f"Could not properly click the menu for number of items per page. Please scroll element into view.  See {elem_not_in_view_err}")
    except ElementClickInterceptedException as elem_blocked_err:
        print(f"Could not properly click the menu for number of items per page. Please close any and all popups blocking the element.  See {elem_blocked_err}")

    sleep(min_wait_time)

    target_value_opt = given_webdriver.find_element(By.XPATH, target_selector)
    target_value_opt.click()
    sleep(min_wait_time)

    try:
        items_per_page_menu = given_webdriver.find_element(By.XPATH, '//div[contains(@class, "mat-select-value")]')
    except NoSuchElementException as does_not_exist_err:
        print(f"Could not find menu to change items per page. \nSee {does_not_exist_err}")

    if items_per_page_menu.text == str(new_items_per_page):
        changed_to_new_ipp = True

    return changed_to_new_ipp



def get_num_items_on_page_bottom_bar(given_webdriver:webdriver=None)->int:
    '''
    Read the number 'of X' from 1 to Y of X
    from element <div class="mat-paginator-range-label"> 1 – 37 of 37 </div>
    '''
    paginator_elem = given_webdriver.find_element(By.XPATH, '//div[@class="mat-paginator-range-label"]')
    raw_paginator_text = paginator_elem.text
    num_items_by_display_cnt = 0
    last_elem_index = -1

    if "of" in raw_paginator_text:
        num_items_by_display_cnt = int(raw_paginator_text.split("of")[last_elem_index].strip())
    else:
        raise ValueError("Could not extract the total number of item from the informational bottom bar")

    return num_items_by_display_cnt


def count_num_items_on_cur_page(given_webdriver:webdriver=None)->int:
    store_items_elems = given_webdriver.find_elements(By.XPATH, '//div[@class="mat-grid-tile-content"]')
    num_items_elems = len(store_items_elems)
    return num_items_elems



def click_product_by_name(given_webdriver:webdriver=None, target_product_name:str="") -> bool:
    product_clicked_on = False
    try:
        target_item_elem = given_webdriver.find_element(By.XPATH, f'//div[contains(text(), "{target_product_name}")]')
        target_item_elem.click()
        sleep(def_wait_time)
        product_clicked_on = True
    except NoSuchElementException as does_not_exist_err:
        print(f"Could not click product {target_product_name} by name.\n See {does_not_exist_err}")
    return product_clicked_on

def get_num_product_reviews(given_webdriver:webdriver=None)->int:
    product_review_exists = 0

    product_review_bar = given_webdriver.find_element(By.XPATH, '//span[contains(@class, "mat-content")]')
    raw_reviews_text   = product_review_bar.text
    num_reviews_text   = raw_reviews_text.replace("Reviews", "").replace("(", "").replace(")", "").strip()
    num_reviews_int    = int(num_reviews_text)
    return num_reviews_int

def expand_product_review(given_webdriver:webdriver=None):
    pass



if __name__ == '__main__':
    # ToDo pull the load_url and dismiss owasp_juice popups to setup stage of testcase class
    # task 3 outline # ToDo convert to unitest TestCase

    wd = load_url(target_browser=Browser.CHROME)

    try:
        dismiss_owasp_juice_popups(wd)

    except Exception as e:
        print(e)

    wd.close()
    wd.quit()





    '''
    # task 2 outline # ToDo convert to unitest TestCase
    wd = load_url(target_browser=Browser.CHROME)

    try:
        dismiss_owasp_juice_popups(wd)
        click_product_by_name(wd, "Apple Juice")
        sleep(def_wait_time)
        popup_elements = wd.find_elements(By.XPATH, '//div[@class="cdk-overlay-pane"]') # top most html tag [div] associated with popup
        num_popup_elements = len(popup_elements)
        expected_num_popups = 1
        print(f'num of popups found {num_popup_elements}')
        ##print(TestCase().assertEqual(num_popup_elements, expected_num_popups ))
        # assertion for associated popup ==> assert # popups == 1

        target_popup = popup_elements[0]
        popup_img = target_popup.find_element(By.XPATH, '//img[@class="img-thumbnail"]')
        print(f'popup has img displayed; {popup_img.is_displayed()}')
        ##TestCase().assertTrue(popup_img.is_displayed()))
        # assertTrue(popup_img.is_displayed()

        # verify url of img exists/response code 200
        # selenium img_elem.is_displayed() + verify img_elem.size['width'] img_elem.size['height'] > 0


        infobar_num_reviews = get_num_product_reviews(wd)
        counted_num_reviews = 0
        if infobar_num_reviews > 0:
            # <mat-expansion-panel _ngcontent-mfm-c42="" aria-label="Expand for Reviews"
            review_bar_elem = target_popup.find_element(By.XPATH, '//mat-expansion-panel[@aria-label="Expand for Reviews"]')
            review_bar_elem.click()
            sleep(min_wait_time)
            # <div _ngcontent-mfm-c42="" class="comment ng-star-inserted">
            review_comments_elems = target_popup.find_elements(By.XPATH, '//div[contains(@class, "comment")]')
            counted_num_reviews   = len(review_comments_elems)

        print(f"info bar # of reviews; {infobar_num_reviews}")
        print(f"counted # of reviews;  {counted_num_reviews}")
        # assert info bar # of reviews == counted # of reviews

        sleep(def_wait_time)
        # <button _ngcontent-mfm-c42="" mat-stroked-button="" mat-dialog-close="" aria-label="Close Dialog" class="mat-focus-indicator close-dialog buttons mat-stroked-button mat-button-base" type="button">
        close_popup_btn = target_popup.find_element(By.XPATH, '//button[@aria-label="Close Dialog"]')
        scroll_to_given_element(wd, close_popup_btn)
        close_popup_btn.click()
        sleep(long_wait_time)

        # close popup
    except Exception as e:
        print(e)

    wd.close()
    wd.quit()
    '''


    '''
    # task 1 outline # ToDo convert to unitest TestCase
    wd = load_url(target_browser=Browser.CHROME)

    try:
        dismiss_owasp_juice_popups(wd)
        print(change_items_per_page(wd))
        expect_num_items = get_num_items_on_page_bottom_bar(wd)
        actua_num_items  = count_num_items_on_cur_page(wd)
    except Exception as e:
        print(e)

    wd.close()
    wd.quit()
    '''