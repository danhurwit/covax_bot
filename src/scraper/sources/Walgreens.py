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
    global_booking_link = 'https://www.walgreens.com/topic/promotion/covid-vaccine.jsp'
    display_properties = DisplayProperties(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Walgreens_Logo.svg/2560px-Walgreens_Logo.svg.png",
        "3CB371")

    def scrape_locations(self):
        locations = []
        chrome_options = Options()
        chrome_options.headless = True
        driver = webdriver.Chrome(executable_path=config('DRIVER_PATH'), options=chrome_options)
        driver.get(self.scrape_url)
        time.sleep(random.randint(1, 3))
        driver.find_element_by_link_text("Schedule new appointment").click()
        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                "#wag-body-main-container > section > section > section > section > section.LocationSearch_container.mt25 > div > span > button")))
            logger.log("page_source\n" + driver.page_source)
            time.sleep(random.randint(1, 5))

            button.click()
            alert_text = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
                "#wag-body-main-container > section > section > section > section > div > a > span:nth-child(2) > p"))).text

            if alert_text != "Appointments unavailable":
                locations.append(Location(self.name,
                                          self.get_global_booking_link(),
                                          datetime.now(),
                                          [AvailabilityWindow(1, datetime.now())]))
            self.locations = locations
        except:
            logger.log("page source on error\n" + driver.page_source)
