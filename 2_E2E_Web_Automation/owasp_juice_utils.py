
from enum import Enum
from random import randint
from time import sleep
from unittest import TestCase

from selenium import webdriver
from selenium.common.exceptions import \
    TimeoutException, NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException, StaleElementReferenceException, InvalidSelectorException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class Browser(Enum):
    CHROME  = 1
    FIREFOX = 2
    EDGE    = 3

owasp_juice_shop_url = "https://juice-shop.herokuapp.com/#/"
owasp_juice_registration_url = "https://juice-shop.herokuapp.com/#/register"
owasp_juice_login_url = 'https://juice-shop.herokuapp.com/#/login'
# highly recommend running own instance of the owasp juice shop given how frequently the herokuapp version crashes and is unavailable


# ToDo swap sleeps that aren't to avoid ddos trigger to expectedcondition wait format

##wait = WebDriverWait(given_webdriver, 10)  # Wait for up to 10 seconds
##element = wait.until(EC.element_to_be_clickable((By.ID, "some-id")))
long_wait_time = 10
def_wait_time = 3
min_wait_time = 1

# really should have credentials in env variable or something similar, plain text non encrypted bad idea
test_cred_email = "test_account@gmail.com"
test_random_email = f"test_account{randint(0,999)}{randint(100,999)}{randint(100,999)}@gmail.com" # to avoid issues with registering same account twice
test_cred_pw    = "notArealpassword123"


def get_webdriver(target_browser:Browser = Browser.CHROME) -> webdriver:
    driver_opts = None
    if target_browser == Browser.CHROME:
        driver_opts = ChromeOptions()
    elif target_browser == Browser.FIREFOX:
        driver_opts = FirefoxOptions()
    elif target_browser == Browser.EDGE:
        driver_opts = EdgeOptions()
    else:
        raise ValueError(f"Unsupported Browser provided; {target_browser}.  Valid values for target_browser in load_url are; { ['Browser.'+cur_mem.name for cur_mem in Browser] }")
    driver_opts.add_argument("--window-size=1920,1080");
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

    return driver



def navigate_to_user_registration(given_webdriver:webdriver=None):
    #<button _ngcontent-tiu-c124="" mat-button="" fxhide.lt-md="" fxshow="" aria-label="Show/hide account menu" id="navbarAccount" class="mat-focus-indicator mat-menu-trigger buttons mat-button mat-button-base" style="vertical-align: middle; height: 48px;" aria-haspopup="menu">
    account_btn = given_webdriver.find_element(By.XPATH, "//button[@aria-label='Show/hide account menu']")
    account_btn.click()
    sleep(min_wait_time)

    #<button _ngcontent-tiu-c124="" mat-menu-item="" routerlink="/login" aria-label="Go to login page" id="navbarLoginButton"
    login_btn = given_webdriver.find_element(By.XPATH, "//button[@aria-label='Go to login page']")
    login_btn.click()
    sleep(min_wait_time)

    # <a _ngcontent-tiu-c48="" routerlink="/register" translate="" class="primary-link" href="#/register">Not yet a customer?</a>
    register_new_btn = given_webdriver.find_element(By.XPATH, "//a[@href='#/register']")
    register_new_btn.click()
    sleep(min_wait_time)

def click_user_reg_title(given_webdriver:webdriver=None):
    '''
     since error msg for input fields on registration will not trigger until clicked out of
    '''
    #user_reg_title = given_webdriver.find_element(By.XPATH, '//h1[@text="User Registration"]')
    user_reg_title = given_webdriver.find_element(By.TAG_NAME, 'h1')
    scroll_to_given_element(given_webdriver, user_reg_title)
    user_reg_title.click()
    sleep(min_wait_time)

def click_email_field(given_webdriver:webdriver=None):
    # <input _ngcontent-tiu-c32="" id="emailControl" type="text" matinput="" aria-label="Email address field" class="mat-input-element mat-form-field-autofill-control ng-tns-c21-13 ng-pristine ng-invalid cdk-text-field-autofill-monitored ng-touched" required="" aria-required="true" aria-describedby="mat-error-2">
    email_field = given_webdriver.find_element(By.XPATH, '//input[@id="emailControl"]')
    email_field.click()
    return email_field

def click_password_field(given_webdriver:webdriver=None):
    pw_field = given_webdriver.find_element(By.XPATH, '//input[@id="passwordControl"]')
    pw_field.click()
    return pw_field

def click_repeat_password_field(given_webdriver:webdriver=None):
    rpw_field = given_webdriver.find_element(By.XPATH, '//input[@id="repeatPasswordControl"]')
    rpw_field.click()
    return rpw_field

def click_security_question_field(given_webdriver:webdriver=None):
    sec_quest_field = given_webdriver.find_element(By.XPATH, '//mat-select[@name="securityQuestion"]')
    sec_quest_field.click()
    return sec_quest_field

def click_security_answer_field(given_webdriver:webdriver=None):
    security_ans_field = given_webdriver.find_element(By.XPATH, '//input[@id="securityAnswerControl"]')
    security_ans_field.click()
    return security_ans_field

def click_password_advice(given_webdriver:webdriver=None):
    pw_adv_elem = given_webdriver.find_element(By.TAG_NAME, 'mat-slide-toggle')
    pw_adv_elem.click()


def get_field_errors(given_webdriver:webdriver=None)->[str]:
    error_list = []
    try:
        error_elems  = given_webdriver.find_elements(By.TAG_NAME, 'mat-error')
        error_list   = [cur_err.text for cur_err in error_elems]
    except Exception as e:
        print(e)
    return error_list



def click_register_button(given_webdriver:webdriver=None):
    register_btn = given_webdriver.find_element(By.XPATH, '//button[@id="registerButton"]')
    register_btn.click()




def register_test_user(given_webdriver:webdriver=None, use_random_email:bool=True):
    email_elem = click_email_field(given_webdriver)
    email_to_use = test_random_email if use_random_email else test_cred_email
    email_elem.send_keys(email_to_use)

    pw_elem = click_password_field(given_webdriver)
    pw_elem.send_keys(test_cred_pw)

    rpw_elem = click_repeat_password_field(given_webdriver)
    rpw_elem.send_keys(test_cred_pw)

    sa_elem = click_security_answer_field(given_webdriver)
    sa_elem.send_keys(test_cred_pw)

    sq_elem = click_security_question_field(given_webdriver)
    actions = ActionChains(wd)
    actions.move_to_element(sq_elem).perform()
    actions.click().perform()

    click_register_button(given_webdriver)
    sleep(min_wait_time)


def get_registration_message(given_webdriver:webdriver=None)->str:
    #class="mat-simple-snack-bar-content"
    registration_msg = given_webdriver.find_element(By.XPATH, '//*[@class="mat-simple-snack-bar-content"]').text
    return registration_msg

def get_angular_popup_msg(given_webdriver:webdriver=None)->str:
    #class="mat-simple-snack-bar-content"
    popup_msg = given_webdriver.find_element(By.XPATH, '//*[@class="mat-simple-snack-bar-content"]').text
    return popup_msg

def click_login_email(given_webdriver:webdriver=None):
    login_email_field = given_webdriver.find_element(By.XPATH, '//input[@id="email"]')
    login_email_field.click()
    return login_email_field

def click_login_password(given_webdriver:webdriver=None):
    login_pw_field = given_webdriver.find_element(By.XPATH, '//input[@id="password"]')
    login_pw_field.click()
    return login_pw_field

def click_login_button(given_webdriver:webdriver=None):
    login_btn = given_webdriver.find_element(By.XPATH, '//button[@id="loginButton"]')
    login_btn.click()




def login_with_test_user(given_webdriver:webdriver=None):
    given_webdriver.get(owasp_juice_login_url)
    sleep(def_wait_time)

    dismiss_owasp_juice_popups(wd)
    email_field = click_login_email(given_webdriver)
    email_field.send_keys(test_cred_email)

    password_field = click_login_password(given_webdriver)
    password_field.send_keys(test_cred_pw)

    click_login_button(given_webdriver)


def get_all_product_elements(given_webdriver:webdriver=None)->[WebElement]:
    product_elements = given_webdriver.find_elements(By.TAG_NAME, 'mat-grid-tile')
    return product_elements

# ToDo move to test case
def add_one_each_first_five_products(given_webdriver:webdriver=None):
    sleep(def_wait_time)
    all_product_elements  = get_all_product_elements(given_webdriver)
    first_five_prod_elems = all_product_elements[:5]
    for cur_prod_elem in first_five_prod_elems:
        #print(cur_prod_elem.find_element(By.XPATH, './/div[@class="item-name"]').text)
        cur_prod_add_basket_btn = cur_prod_elem.find_element(By.XPATH, ".//button[@aria-label='Add to Basket']")
        scroll_to_given_element(given_webdriver, cur_prod_add_basket_btn)
        cur_prod_add_basket_btn.click()
        sleep(min_wait_time)
        print(get_angular_popup_msg(given_webdriver))
        sleep(min_wait_time)


def get_num_items_in_basket(given_webdriver:webdriver=None):
    product_cnt_int = 0
    product_cnt_elem = given_webdriver.find_element(By.XPATH, '//span[contains(@class,"mat-button-wrapper")]//span[contains(@class, "fa-layers-counter")]')
    try:
        product_cnt_int = int(product_cnt_elem.text)
    except Exception as e:
        print(f"Error occured while trying to extract number of items in basket.  Please see {e}")

    return product_cnt_int


def navigate_to_basket(given_webdriver:webdriver=None):
    #<button _ngcontent-seh-c124="" mat-button="" routerlink="/basket" aria-label="Show the shopping cart"
    sleep(min_wait_time)
    cart_btn = given_webdriver.find_element(By.XPATH, '//button[@aria-label="Show the shopping cart"]')
    scroll_to_given_element(given_webdriver, cart_btn)
    cart_btn.click()
    sleep(min_wait_time)


def get_current_basket_total_price(given_webdriver:webdriver=None)->float:
    basket_total = 0.0
    # <div _ngcontent-seh-c18="" id="price" class="ng-star-inserted">Total Price: 1.99¤</div>
    basket_total_elem = given_webdriver.find_element(By.XPATH, '//div[@id="price"]')
    basket_total = float(basket_total_elem.text.replace("¤", "").replace("Total Price:", "").strip())

    return basket_total


def increase_item_in_basket(given_webdriver:webdriver=None, item_name:str=""):
    root_label = given_webdriver.find_element(By.XPATH, f'//mat-cell[contains(text(), "{item_name}")]')
    #print(f"base {root_label.get_attribute('outerHTML')}")
    associated_row = root_label.find_element(By.XPATH, "..")
    #print(f"parent {associated_row.get_attribute('outerHTML')}")
    # ToDo find better way than relying on index of buttons in row, trying to match on svg didn't work, need to figure out why or alt way
    item_buttons = associated_row.find_elements(By.TAG_NAME, 'button')
    # index 0 is dec, index 1 is inc, index 2 is delete
    inc_item_btn = item_buttons[1]
    inc_item_btn.click()

    #inc_item_btn =  associated_row.find_element(By.XPATH, './/svg[contains(@class,"fa-plus-square")]')
    #inc_item_btn.click()
    sleep(min_wait_time)

def delete_item_in_basket(given_webdriver:webdriver=None, item_name:str=""):
    root_label = given_webdriver.find_element(By.XPATH, f'//mat-cell[contains(text(), "{item_name}")]')
    associated_row = root_label.find_element(By.XPATH, "..")
    #print(f"parent {associated_row.get_attribute('outerHTML')}")

    item_buttons = associated_row.find_elements(By.TAG_NAME, 'button')
    # index 0 is dec, index 1 is inc, index 2 is delete
    del_item_btn = item_buttons[2]
    del_item_btn.click()

    sleep(min_wait_time)


def click_checkout_from_basket(given_webdriver:webdriver=None):
    #<button _ngcontent-woe-c19="" id="checkoutButton"
    chkout_btn = given_webdriver.find_element(By.ID, "checkoutButton")
    chkout_btn.click()
    sleep(min_wait_time)


def click_add_new_addy_from_chkout(given_webdriver:webdriver=None):
    add_new_addy_btn = given_webdriver.find_element(By.XPATH, "//button[@aria-label='Add a new address']")
    add_new_addy_btn.click()
    sleep(min_wait_time)

def fill_out_addy_info(given_webdriver:webdriver=None):
    # could use IDs but mat-input-# doesnt seem stable/reliable or readilable updatable should something change
    country_box = given_webdriver.find_element(By.XPATH, "//input[@data-placeholder='Please provide a country.']")
    country_box.send_keys("Ionia")

    name_box = given_webdriver.find_element(By.XPATH, "//input[@data-placeholder='Please provide a name.']")
    name_box.send_keys("Xerxes")

    phone_num_box = given_webdriver.find_element(By.XPATH, "//input[@data-placeholder='Please provide a mobile number.']")
    phone_num_box.send_keys("8675309")

    zip_box = given_webdriver.find_element(By.XPATH, "//input[@data-placeholder='Please provide a ZIP code.']")
    zip_box.send_keys("20004")

    address_box = given_webdriver.find_element(By.XPATH, "//textarea[@data-placeholder='Please provide an address.']")
    address_box.send_keys("1600 Pennsylvania Avenue")

    city_box = given_webdriver.find_element(By.XPATH, "//input[@data-placeholder='Please provide a city.']")
    city_box.send_keys("Washington")

    state_box = given_webdriver.find_element(By.XPATH, "//input[@data-placeholder='Please provide a state.']")
    state_box.send_keys("DC")

    submit_btn = given_webdriver.find_element(By.ID, "submitButton")
    submit_btn.click()

def select_addy_by_index(given_webdriver:webdriver=None, addy_index:int=0):
    sleep(min_wait_time)
    #<input type="radio" class="mat-radio-input" id="mat-radio-42-input" tabindex="0">
    addy_radio_btns = given_webdriver.find_elements(By.TAG_NAME, "mat-radio-button") #"//input[@class='mat-radio-input']")
    num_radio_btns = len(addy_radio_btns)
    if addy_index >= num_radio_btns:
        raise IndexError(f"given index {addy_index} is not within the available address buttons of length [{num_radio_btns}]")
    target_rbtn = addy_radio_btns[addy_index]
    target_rbtn.click()

    continue_btn = given_webdriver.find_element(By.XPATH, "//button[@aria-label='Proceed to payment selection']")
    continue_btn.click()

def select_delivery_method_by_index(given_webdriver:webdriver=None, deliv_index:int=0):
    deliv_radio_btns = given_webdriver.find_elements(By.TAG_NAME, "mat-radio-button") #"//input[@class='mat-radio-input']")
    num_deliv_btns = len(deliv_radio_btns)
    if deliv_index >= num_deliv_btns:
        raise IndexError(f"given index {deliv_index} is not within the available delivery buttons of length [{num_deliv_btns}]")
    target_dbtn = deliv_radio_btns[deliv_index]
    target_dbtn.click()

    continue_btn = given_webdriver.find_element(By.XPATH, "//button[@aria-label='Proceed to delivery method selection']")
    continue_btn.click()

def get_wallet_balance_from_payment_options(given_webdriver:webdriver=None)->float:
    wallet_balance = None
    #<span _ngcontent-msd-c86="" class="confirmation card-title"> 0.00</span>
    wallet_balance_elem = given_webdriver.find_element(By.XPATH, "//span[@class='confirmation card-title']")
    wallet_balance = float(wallet_balance_elem.text.strip())
    return wallet_balance


def add_cc_info_at_payment_options(given_webdriver:webdriver=None):
    #<mat-expansion-panel
    sleep(def_wait_time)
    dropdown_menus = given_webdriver.find_elements(By.TAG_NAME, 'mat-expansion-panel')
    add_cc_bar = dropdown_menus[0]
    #index 0 is add cc, 1 is add coupon, 2 is other payment options

    add_cc_bar.click()
    sleep(def_wait_time)

    all_input_boxes = given_webdriver.find_elements(By.XPATH, '//input[contains(@id, "mat-input")]')
    all_dropdowns = given_webdriver.find_elements(By.XPATH, '//select[contains(@id, "mat-input")]')
    #(By.TAG_NAME, 'input')

    name_box = all_input_boxes[1]  #given_webdriver.find_element(By.XPATH, '//mat-label[contains(text(), "Name")]')
    scroll_to_given_element(given_webdriver, name_box)
    #WebDriverWait( given_webdriver, def_wait_time ).until( EC.element_to_be_clickable(name_box) )
    #(By.ID, 'mat-input-13') # not reliable
    name_box.send_keys("Xerxes")

    cc_num_box = all_input_boxes[2]
    #cc_num_box.click()
    cc_num_box.send_keys('8675309012345678')

    cc_month_dropdown = all_dropdowns[0]
    cc_month_select = Select(cc_month_dropdown)
    cc_month_select.select_by_value("7")

    cc_year_dropdown = all_dropdowns[1]
    cc_year_select = Select(cc_year_dropdown)
    cc_year_select.select_by_value("2099")
    sleep(min_wait_time)

    submit_info_btn = given_webdriver.find_element(By.ID, 'submitButton')
    WebDriverWait( given_webdriver, def_wait_time ).until( EC.element_to_be_clickable(submit_info_btn) )
    submit_info_btn.click()


def select_cc_by_index_payment_options(given_webdriver:webdriver=None, cc_index:int=0):
    sleep(min_wait_time)
    cc_radio_btns = given_webdriver.find_elements(By.TAG_NAME, "mat-radio-button")
    num_cc_btns = len(cc_radio_btns)
    if cc_index >= num_cc_btns:
        raise IndexError(f"given index {cc_index} is not within the available credit card info buttons of length [{num_cc_btns}]")
    target_ccbtn = cc_radio_btns[cc_index]
    target_ccbtn.click()


def go_to_order_review_from_payment_options(given_webdriver:webdriver=None):
    continue_btn = given_webdriver.find_element(By.XPATH, "//button[@aria-label='Proceed to review']")
    continue_btn.click()
    sleep(min_wait_time)

def checkout_at_order_review(given_webdriver:webdriver=None):
    chkout_btn = given_webdriver.find_element(By.ID, "checkoutButton")
    chkout_btn.click()


def dismiss_owasp_juice_popups(given_webdriver:webdriver=None):
    try:
        cookie_btn = given_webdriver.find_element(By.XPATH, '//a[@aria-label="dismiss cookie message"]')
        cookie_btn.click()
        sleep(min_wait_time)
    except (NoSuchElementException, ElementNotInteractableException) as does_not_exist_err:
        print(f"Could not find cookie popup close button. Please ensure said popup exists to dismiss. \nSee {does_not_exist_err}")

    try:
        dismiss_welcome_btn = given_webdriver.find_element(By.XPATH, '//button[@aria-label="Close Welcome Banner"]')
        dismiss_welcome_btn.click()
        sleep(min_wait_time)
    except (NoSuchElementException, ElementNotInteractableException) as does_not_exist_err:
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




if __name__ == '__main__':
    is_herokuapp_available_and_stable = False # because its so fun to test when all your test data goes poof mid test
    if not is_herokuapp_available_and_stable:
        heroku_base_url = "https://juice-shop.herokuapp.com"
        local_base_url  = "http://127.0.0.1:3000"
        owasp_juice_shop_url         = owasp_juice_shop_url.replace(heroku_base_url, local_base_url)
        owasp_juice_registration_url = owasp_juice_registration_url.replace(heroku_base_url, local_base_url)
        owasp_juice_login_url        = owasp_juice_login_url.replace(heroku_base_url, local_base_url)

    # task 4 outline
    wd = get_webdriver(target_browser=Browser.CHROME)

    try:


        login_with_test_user(wd)
        add_one_each_first_five_products(wd)
        #print(get_num_items_in_basket(wd))
        navigate_to_basket(wd)
        #print(get_current_basket_total_price(wd))
        #increase_item_in_basket(wd, "Apple Juice")
        #print(get_current_basket_total_price(wd))
        #delete_item_in_basket(wd, "Apple Juice")
        #print(get_current_basket_total_price(wd))
        click_checkout_from_basket(wd)
        #click_add_new_addy_from_chkout(wd)
        #fill_out_addy_info(wd)
        select_addy_by_index(wd, 0)
        select_delivery_method_by_index(wd, 0)
        print(get_wallet_balance_from_payment_options(wd))
        add_cc_info_at_payment_options(wd)
        select_cc_by_index_payment_options(wd, 0)
        go_to_order_review_from_payment_options(wd)
        checkout_at_order_review(wd)
        sleep(long_wait_time)


    except Exception as e:
        print(e)

    wd.close()
    wd.quit()














##===============================================================
'''
# ToDo pull the load_url and dismiss owasp_juice popups to setup stage of testcase class
# task 3 outline # ToDo convert to unitest TestCase

wd = get_webdriver(target_browser=Browser.CHROME)

try:

    # ToDo pull navigation to its own test case and then load from registration url
    wd.get(owasp_juice_shop_url)
    sleep(def_wait_time)

    dismiss_owasp_juice_popups(wd)
    navigate_to_user_registration(wd)


    wd.get(owasp_juice_login_url)
    sleep(def_wait_time)

    dismiss_owasp_juice_popups(wd)


    click_email_field(wd)
    click_user_reg_title(wd)
    email_err = get_field_errors(wd)
    print(email_err)

    wd.refresh() # to reset error msg(s)
    sleep(min_wait_time)

    click_password_field(wd)
    click_user_reg_title(wd)
    pw_err = get_field_errors(wd)
    print(pw_err)
    wd.refresh()
    sleep(min_wait_time)


    click_repeat_password_field(wd)
    click_user_reg_title(wd)
    rpw_err = get_field_errors(wd)
    print(rpw_err)
    wd.refresh()
    sleep(min_wait_time)


    click_security_question_field(wd)
    #click_user_reg_title(wd) # click intercept error
    actions = ActionChains(wd)
    sec_quest_field = wd.find_element(By.XPATH, '//mat-select[@name="securityQuestion"]')
    actions.move_to_element(sec_quest_field).perform()
    actions.move_by_offset(-333, 0).click().perform()
    sleep(min_wait_time)
    sq_err = get_field_errors(wd)
    print(sq_err)
    wd.refresh()
    sleep(min_wait_time)


    click_security_answer_field(wd)
    click_user_reg_title(wd)
    sa_err = get_field_errors(wd)
    print(sa_err)
    wd.refresh()
    sleep(min_wait_time)

    click_password_advice(wd)
    sleep(min_wait_time)
    register_test_user(wd)
    #success_msg = "Registration completed successfully. You can now log in."
    registration_msg = get_registration_message(given_webdriver)
    # assert registration msg includes sucessful

    login_with_test_user(wd)



except Exception as e:
    print(e)

wd.close()
wd.quit()
'''




##===============================================================
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

##===============================================================
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