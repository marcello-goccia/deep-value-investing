import os
import time
import platform
import pickle
from bs4 import BeautifulSoup

from utilities.common_methods import getDebugInfo
from utilities.common_methods import EthernetProblems as eth_problems
from utilities.globals import paths

from utilities import log
from website_scraping.investing_dot_com.common_investing_com import Timers as timers

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets import tables

name_popup_close_button = "popupCloseIcon"  # popupCloseIcon largeBannerCloser
name_popup_consent_button = "closer"

debug = False
raspberry_pi = False


class Scraping:

    exception_raised = False
    # connection_problems = False
    # counter_connection_problems = 0
    # max_counter = 20

    def __init__(self):
        try:

            self.driver = None
            self.soup = None
            # self.connection_problems = False
            # self.counter_connection_problems = 0
            # self.exception_raised = False

            if raspberry_pi:
                self.path_chromedriver = "/usr/bin/chromedriver"
            else:
                self.path_chromedriver = "/usr/local/bin/chromedriver"

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def instantiate_driver(self, invisible=False):
        try:
            if os.getenv("environment") == "production":
                self.driver = webdriver.PhantomJS()  # PhantomJS does not open the webrowser.

            elif platform.system() == 'Darwin' or platform.system() == 'Linux':  # ##### MacOs or Linux

                chrome_options = webdriver.ChromeOptions()
                preferences = {"download.default_directory": paths.downloads}
                chrome_options.add_argument('--no-sandbox')
                if invisible:
                    chrome_options.add_argument('--headless')
                # chrome_options.add_argument('--disable-gpu')

                chrome_options.add_experimental_option("prefs", preferences)

                self.driver = webdriver.Chrome(self.path_chromedriver, chrome_options=chrome_options)

            else:                               # ##### 'Windows'
                import sys
                sys.exit("Cannot deal with this now!")

            if self.driver is None:
                raise Exception("Something went wrong cannot instantiate the webdriver.")

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_cookies(self, website):
        """
        Use this to be able to update the cookies.

        You place this method after having instantiated the driver.
        Place a breakpoint on pickle.dump(...)
        Login with your credentials and do everything you need to store all the cookies.
        Then proceed with pickle.dump. Close the app, and comment/delete the calling to this method. Job done!!
        @param website the website to access
        @return Nothing
        """
        self.driver.get(website)
        # place a breakpoint just after this comment
        pickle.dump(self.driver.get_cookies(), open(paths.cookies, "wb"))

    def add_cookies(self, website):
        self.driver.get(website)
        cookies = pickle.load(open(paths.cookies, "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.driver.add_cookie(cookie)
            # for key, value in cookie.items():
            #     self.driver.add_cookie({'name': key, 'value': value})

    def set_driver(self, driver):
        """
        @function set_driver
        Used to set the driver from another already instantiated class.
        """
        try:
            self.driver = driver
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def close_popup_if_present(self):
        try:
            try:
                self.driver.find_element_by_class_name(name_popup_close_button).click()
            except Exception as e:
                pass
            try:
                self.driver.find_element_by_xpath(f"//i[@class='{name_popup_close_button} largeBannerCloser']").click()
            except Exception as e:
                pass
        except Exception as e:
            pass
        try:
            self.driver.find_element_by_class_name(name_popup_consent_button).click()
        except Exception as e:
            pass

    def give_web_page_to_beautiful_soup(self):
        """
        @function give_web_page_to_beautiful_soup
        The method copies the page source from the webdriver to beautiful soup to
        retrieve the needed information.
        """
        try:
            self.soup = None

            try:
                self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            except Exception as e:
                if 'timeout' in str(e):
                    message = ''
                    if self.soup is None:
                        message = 'beautifulsop is None'
                    raise Exception(f'Received a timeout from webdriver, and {message}')
                else:
                    raise Exception(f'General problem with page timing!')

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem when giving the page to beautiful soup!: {e}\n{getDebugInfo()}")

    def wait_until_element_appears_through_id(self, element_name):
        """
        @function wait_until_element_appears_through_id
        The webdriver waits for the page to load until the element passed as input parameter appears.
        Otherwise an exception is raised.
        IUt first waits 2 seconds because the new page could not be event started to be loaded.
        :param element_name: the element to appear in the page.
        :return:
        """
        try:
            time.sleep(timers.waiting)
            WebDriverWait(self.driver, timers.webdriver_wait).until(EC.presence_of_element_located((By.ID, element_name)))
            return True
        except TimeoutException as e:
            Scraping.exception_raised = True
            log.error(f"Exception: could not find the element we are looking for")
            return False

    def wait_until_appears_part_of_text_through_xpath(self, tag, input_text):
        """
        @function wait_until_appears_part_of_text_through_xpath
        The webdriver waits for the page to load until the element passed as input parameter appears.
        Otherwise an exception is raised.
        The seraching method is performed by using xpath, so it looks for containing text.
        :param element_name: the element to appear in the page.
        :return:
        """
        try:
            time.sleep(timers.waiting)
            xpath_string = f"//{tag}[contains(text(), '{input_text}')]"
            WebDriverWait(self.driver, timers.webdriver_wait).until(EC.presence_of_element_located((By.XPATH, xpath_string)))
        except TimeoutException as e:
            Scraping.exception_raised = True
            log.info(f"Exception {e}")

    def loop_locators_to_find_correct_one(self, locators):
        """
        @function loop_locators_to_find_correct_one
        The method tries different locator to find the one suitable for my purposes.
        When succeded it returns the correct locator, otherwise it returns none.
        @param locators list of locator to test on the webpage
        @return locator to suitable locator if any.
        """
        self.give_web_page_to_beautiful_soup()
        for locator in locators:
            found, element = self.wait_until_appears_attrib_through_my_way(locator)
            if found:
                return element

        log.info("Did not find any of the locators we tried")
        return None  # did not find any

    def wait_until_appears_attrib_through_my_way(self, locator):
        """
        @function wait_until_appears_attrib_through_my_way
        The web-driver waits for the page to load until the element passed as input parameter appears.
        Otherwise an exception is raised.
        The searching method is performed by using xpath, so it looks for containing text.

        @param tag_to_find the tag where the attribute should be present
        @param attribute_to_find: the attribute we are looking for
        @param attribute_value: the value of the attribute we are looking for

        @return:
        """
        try:
            found = False
            element = None

            start_t = time.monotonic()
            intermdiate = 0.0
            while intermdiate < timers.wait_appears_attribute:
                found, element = self.check_page_loaded_css_selector_tag_attr_value(locator)
                if found:
                    break
                self.give_web_page_to_beautiful_soup()
                intermdiate = time.monotonic() - start_t

            log.info(f"time to load page: {time.monotonic() - start_t} seconds")
            return found, element

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"Exception {e}")
            return False

    def check_page_loaded_css_selector_tag_attr_value(self, locator):
        """
        @function check_page_loaded_css_selector
        It is a check the page with the list of assets has loaded corretly.
        The che is done by looking at a text change in the page.
        @param element_to_find the element (attribute) to look for needed to help to easily find the text_to_compare.
        @param text_to_compare the text we want to compare to see if it exists
        @return true if loaded
        """
        try:
            tag = locator['tag']
            attrib = locator['attrib']
            attrib_value = locator['name']

            found = self.soup.find(tag, {attrib: attrib_value})
            #found = self.driver.find_element_by_css_selector(f"{tag}[{attrib}='{attrib_value}']")

            if found:
                return True, found
            return False, None
        except NoSuchElementException:
            return False, None
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"Exception {e}")

    def wait_until_appears_part_of_text_through_my_way(self, element_to_find, input_text):
        """
        @function wait_until_appears_part_of_text_through_xpath
        The webdriver waits for the page to load until the element passed as input parameter appears.
        Otherwise an exception is raised.
        The seraching method is performed by using xpath, so it looks for containing text.
        :param element_name: the element to appear in the page.
        :return:
        """
        try:
            counter = 0
            for i in range(timers.times_loop_to_load_page_appears_part_of_text):
                counter += 1
                if self.check_page_loaded_css_selector(element_to_find, input_text):  # float_lang_base_1 inlineblock
                    break
                time.sleep(timers.atomical_sleep)
            log.info(f"time to load page: {counter * timers.atomical_sleep} seconds")

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"Exception {e}")

            if "no such element" in str(e):  # connection problems??
                eth_problems.counter_connection_problems += 1
                if eth_problems.counter_connection_problems > eth_problems.max_counter:
                    eth_problems.connection_problems = True
                    log.error("In the method: check_page_loaded_css_selector")
                    log.error(f"Connection error!!! So far it happened {eth_problems.counter_connection_problems} times")

    def check_page_loaded_css_selector(self, element_to_find, text_to_compare):
        """
        @function check_page_loaded_css_selector
        It is a check the page with the list of assets has loaded corretly.
        The che is done by looking at a text change in the page.
        @param element_to_find the element (attribute) to look for needed to help to easily find the text_to_compare.
        @param text_to_compare the text we want to compare to see if it exists
        @return true if loaded
        """
        try:
            text__retrieved = self.driver.find_element_by_css_selector(element_to_find)
            if text_to_compare in text__retrieved.text:
                return True
            return False
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"Exception {e}")

            if "no such element" in str(e):  # connection problems??
                eth_problems.counter_connection_problems += 1
                if eth_problems.counter_connection_problems > eth_problems.max_counter:
                    eth_problems.connection_problems = True
                    log.error("In the method: check_page_loaded_css_selector")
                    log.error(f"Connection error!!! So far it happened {eth_problems.counter_connection_problems} times")

    def wait_until_appears_part_of_attribute_through_css(self, tag, case, element_name):
        """
        @function wait_until_appears_part_of_attribute_through_css
        The webdriver waits for the page to load until the element passed as input parameter or part of it appears.
        Otherwise an exception is raised.
        IU first waits 2 seconds because the new page could not be event started to be loaded.
        @param tag can be any needed, div, table etc.
        @param case can be any needed, id, class text, etc..
        @param element_name: the element to appear in the page.
        """
        try:
            time.sleep(timers.waiting)
            css_string = f"{tag}[{case}*='{element_name}']"
            element_found = EC.presence_of_element_located((By.CSS_SELECTOR, css_string))
            WebDriverWait(self.driver, timers.webdriver_wait).until(element_found)
        except TimeoutException as e:
            Scraping.exception_raised = True
            log.error(f"Exception {e}")
        finally:
            pass

    def set_equity_extraction_completed(self, equity):
        """
        @function set_equity_extraction_completed
        The class sets completed if the fundamental data of the equity have been correctly retrieved.
        :param equity: the equity of which we want to set as completed.
        """
        try:
            if not Scraping.exception_raised:
                log.info(f"No exception was raised, exception_raised = {Scraping.exception_raised}")
                Scraping.check_ok(tables.equity.add_single_element(equity, 'all done', True), expected=0, identifier='all done')
                db_mngr.commit_to_database()
            else:
                log.info(f"It seems as exception was raised, exception_raised = {Scraping.exception_raised}")
                Scraping.exception_raised = False
                Scraping.check_ok(tables.equity.add_single_element(equity, 'all done', False), expected=0, identifier='all done')
                db_mngr.commit_to_database()

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def look_for_some_text_through_webdriver(self, tag, input_text):
        """
        @function look_for_some_text_through_webdriver
        Supposed to be very generalist!!!! The webdriver looks for text by passing the tag, where the text is contained
        and the string of text.
        @param tag can be any needed, div, table etc.
        @param input_text: the text to appear in the page.
        """
        try:
            try:
                return self.driver.find_element_by_xpath(f"//{tag}[contains(text(), '{input_text}')]")
            except NoSuchElementException as e:
                return None
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def look_for_some_element_through_webdriver(self, tag, attribute, value):
        """
        @function look_for_some_element_through_webdriver
        Supposed to be very generalist!!!! The webdriver looks for anything you need by passing the tag,
        the element you are looking for and the text which identifies it (value)
        @param tag can be any needed, div, table etc.
        @param attribute can be any needed, id, class text, etc..
        @param value: the text to appear in the page.
        """
        try:
            return self.driver.find_element_by_css_selector(f"{tag}[{attribute}*='{value}']")
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def look_for_some_element_through_soup(self, tag, attribute, value):
        """
        @function look_for_some_element_through_soup
        Supposed to be very generalist!!!! The soup looks for anything you need by passing the tag,
        the element you are looking for and the text which identifies it (value)
        @param tag can be any needed, div, table etc.
        @param attribute can be any needed, id, class text, etc..
        @param value: the text to appear in the page.
        """
        try:
            found = self.soup.select(f'{tag}[{attribute}*="{value}"]')

            if not found:
                return None

            assert(len(found) == 1)
            return found[0]
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def check_page_contains_element(self, element_name, by_what=By.ID):
        try:
            self.close_popup_if_present()
            WebDriverWait(self.driver, timers.webdriver_wait).until(EC.presence_of_element_located((by_what, element_name)))
            self.close_popup_if_present()
            return True
        except TimeoutException as e:
            log.error(f"It is possible the element you are looking for is not present")
            return False

    @staticmethod
    def check_ok(action, expected, identifier):
        """
        @function check_ok
        It checks it action is the expected one, if not is raises and exception.
        """
        try:
            if action != expected:
                raise Exception(f"Problems checking: {identifier}")
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def click_on_link_until_found(self, text_link):

        try:
            timeout = time.time() + 60  # 1 minutes from now
            while True:
                try:
                    element = self.driver.find_element_by_link_text(text_link)
                except NoSuchElementException:
                    break
                if element:
                    element.click()
                if time.time() > timeout:
                    Scraping.exception_raised = True
                    log.error(f"Taking too long in the method click_on_link_until_found! ")
                    break

        except Exception as e:
            if 'element not interactable' in str(e) or \
                    'is not clickable' in str(e):
                return

            Scraping.exception_raised = True
            log.error(f"There is a problem when clinking on the following {text_link}: {e}\n{getDebugInfo()}")
