
import time
from urllib.request import URLError

from website_scraping.scraping import Scraping
from utilities.globals import websites
from website_scraping.investing_dot_com.common_investing_com import Timers as timers

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities import log


class ScrapingInvesting(Scraping):
    def __init__(self):
        try:

            super(ScrapingInvesting, self).__init__()

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def open_website(self, url, title=''):
        """
        @function open_website
        The method opens the browser and the chosen main website.
        """
        try:
            self.driver.set_page_load_timeout(timers.page_load_timeout)
            for i in range(timers.times_getting_url):
                try:
                    time.sleep(0.5)
                    self.driver.get(url)
                    log.info(f"debug only: webpage {url} opened")
                    break
                except Exception as e:
                    if 'timeout' in str(e):
                        log.info(f"Timeout reached with the following url: {url}. Trying again")
                        time.sleep(0.5)
                        break

            # do the following only if I send something.
            if title:
                log.info(f"Website title: {self.driver.title}")
                if title == 'Company Profile' or title == 'Dividends':
                    assert websites.investing_title in self.driver.title
                else:
                    assert title in self.driver.title
            self.close_popup_if_present()

        except URLError as e:
            Scraping.exception_raised = True
            raise Exception("Cannot open url.")
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def try_clicking_on_link(self, element_to_find):
        try:
            max_counter = timers.times_cliking_on_links

            for i in range(max_counter):

                try:
                    if i == 0:
                        self.click_by_action_chains(element_to_find)
                    elif i == 1:
                        self.click_by_web_driver_wait(element_to_find)
                    elif i == 2:
                        self.click_by_link(element_to_find)
                    log.info(f"found {element_to_find}!")
                    break
                except NoSuchElementException as e:
                    log.info(f"{element_to_find} not found, trying again.")
                    self.close_popup_if_present()
                except Exception as e:
                    log.info(f"cannot click on {element_to_find} try again")
                    self.close_popup_if_present()

                time.sleep(timers.waiting)
                self.close_popup_if_present()

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code! Really cannot click on the link: {e}\n{getDebugInfo()}")

    def click_by_link(self, element_to_find):
        try:
            link_text = self.driver.find_element_by_link_text(element_to_find)
            link_text.click()
        except Exception as e:
            raise Exception("Could not click!")

    def click_by_web_driver_wait(self, element_to_find):
        try:
            # an Explicit elementToBeClickable Wait:
            wait = WebDriverWait(self.driver, timers.webdriver_wait)
            element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, element_to_find)))
            element.click()
        except Exception as e:
            raise Exception("Could not click!")

    def click_by_action_chains(self, element_to_find):
        try:
            link_text = self.driver.find_element_by_link_text(element_to_find)
            actions = ActionChains(self.driver)
            actions.move_to_element(link_text)
            actions.click(link_text)
            actions.perform()

        except Exception as e:
            raise Exception("Could not click!")

    def open_link_page(self, name_page, link='', tag=''):
        """
        @function open_link_page
        The method tries to press on the element passed as input (name_page), if a link is passed directly
        it automatically opens the link page through the web-browser.
        @param name_page the name given to the element to press.
        @param link the link of the page to open
        @param tag the tag where the name of the page can be found to be sure the page was correctly open.
        @return:
        """
        try:
            if not link:
                self.try_clicking_on_link(name_page)
            else:
                self.open_website(link, name_page)
                self.wait_until_appears_part_of_text_through_xpath(tag, name_page)
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def open_link_list_of_assets(self, link='', tag=''):
        """
        @function open_link_list_of_assets
        The method tries is a simplified version of the method open_link_page because I found sometimes difficult
        dealing with assert the title and with checking something appeared in the website page.
        So I decided to do a version mainly for asset scraping, but I will try to implement for others as well.
        @param name_page the name given to the element to press.
        @param link the link of the page to open
        @param tag the tag where the name of the page can be found to be sure the page was correctly open.
        @return:
        """
        try:

            methods.perform_until_succeed(10, self.driver.get, link)

            time.sleep(1)
            class_name = "js-total-results"

            counter = 0
            sleep = timers.atomical_sleep
            for i in range(timers.times_loop_to_load_page):
                counter += 1
                if self.check_list_loaded(class_name):
                    break
                time.sleep(sleep)
            seconds = counter * sleep

            log.info("time to load page: %.2f seconds" % seconds)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def check_list_loaded(self, class_name):
        """
        @function check_list_loaded
        It is a check the page with the list of assets has loaded corretly.
        The che is done by looking at a text change in the page.
        @param class_name the name of the class of the element
        @return true if loaded
        """
        try:
            total_results = methods.perform_until_succeed(10, self.driver.find_element_by_class_name, class_name)
            time.sleep(1)

            if not total_results:
                raise Exception(f"Trying several times but cannot open the element {class_name}")

            total_results = int(total_results.text)
            if total_results > 0:
                return True
            return False
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"Problem checking the list loaded: {e}\n{getDebugInfo()}")

    def get_correct_link_financials(self, original_link, financial_string):
        """
        @function get_correct_link_financials
        The method tries to parse the original link in input to produce the final link able to open the desired
        financial pace of investing.com
        @param the original link of investing equity
        @param the desired financial page to open
        @return the updated link
        """
        try:
            substring_to_find = '?cid='
            index = original_link.find(substring_to_find)
            if index != -1:
                output = ''.join([original_link[:index], financial_string, original_link[index:]])
            else:
                output = ''.join([original_link, financial_string])
            return output
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
