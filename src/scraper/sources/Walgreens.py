import random
import time
from datetime import datetime

from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from logger import logger
from models.sources.AppointmentSource import AppointmentSource
from models.sources.AvailabilityWindow import AvailabilityWindow
from models.sources.DisplayProperties import DisplayProperties
from models.sources.Location import Location


class Walgreens(AppointmentSource):
    name = "Walgreens"
    scrape_url = 'https://www.walgreens.com/findcare/vaccination/covid-19?ban=covid_vaccine_landing_schedule'
    global_booking_link = 'https://www.walgreens.com/findcare/vaccination/covid-19/'
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Walgreens_Logo.svg/2560px-Walgreens_Logo.svg.png",
        "3CB371")

    def scrape_locations(self):
        chrome_options = Options()
        chrome_options.headless = True  # detected in headless mode
        driver = webdriver.Chrome(executable_path=config('DRIVER_PATH'), options=chrome_options)
        try:
            self.nav_to_location_screening(driver)
            search_button = self.wait_for_search_button(driver)
            self.random_sleep(2000, 5000, 500)
            self.enter_zip_code(driver)
            self.click_random_interval(search_button, driver)
            appointments_available = self.validate_availability(driver)
            if appointments_available:
                self.locations = [Location(self.name,
                                           self.get_global_booking_link(),
                                           datetime.now(),
                                           [AvailabilityWindow(1, datetime.now())])]
        except Exception as e:
            logger.log("Walgreens scrape error\n {}".format(driver.page_source[:1000]))
        finally:
            driver.close()

    def wait_for_search_button(self, driver):
        button = WebDriverWait(driver, 10) \
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                               "#wag-body-main-container > section "
                                               "> section > section > section > "
                                               "section.LocationSearch_container.mt25 > div > span > button")))
        return button

    def nav_to_location_screening(self, driver):
        driver.get(self.scrape_url)
        redirect_button = driver.find_element_by_link_text("Schedule new appointment")
        self.random_sleep(1000, 3000, 250)
        self.click_random_interval(redirect_button, driver)

    def enter_zip_code(self, driver):
        input_element = driver.find_element_by_id("inputLocation")
        self.random_sleep(100, 500, 50)
        input_element.clear()
        self.random_sleep(300, 500, 50)
        input_element.send_keys("0")
        self.random_sleep(10, 50, 5)
        input_element.send_keys("2")
        self.random_sleep(10, 50, 5)
        input_element.send_keys("1")
        self.random_sleep(10, 50, 5)
        input_element.send_keys("3")
        self.random_sleep(10, 50, 5)
        input_element.send_keys("9")

    def validate_availability(self, driver):
        appointments_available = None
        try:
            appointments_available = WebDriverWait(driver, 3) \
                .until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                         "#wag-body-main-container > section > section > section > "
                                                         "section > section.eligibleScreens > section > div > a > "
                                                         "span:nth-child(2) > p"))).text
        except Exception as e:
            print("no appointments this time")
        return appointments_available

    def click_random_interval(self, button, driver):
        webdriver.ActionChains(driver).move_to_element(button).perform()
        self.random_sleep(100, 1000, 50)
        webdriver.ActionChains(driver).click_and_hold(button).perform()
        self.random_sleep(100, 1000, 50)
        webdriver.ActionChains(driver).release(button).perform()

    def random_sleep(self, lower_limit_millis, upper_limit_millis, noise):
        lower_jitter = random.randint(lower_limit_millis - noise, lower_limit_millis + noise)
        upper_jitter = random.randint(upper_limit_millis - noise, upper_limit_millis + noise)
        rand = random.randint(lower_jitter, upper_jitter) / 1000
        time.sleep(rand)
