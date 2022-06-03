import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class XiorScraper:

    def __init__(self):
        self.data_delft = {
            "country": "Netherlands",
            "city": "Delft"
        }
        self.working_data = {
            "country": "Germany"
        }

        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920x1480")
        options.add_argument("disable-dev-shm-usage")
        # options.headless = True
        self.browser = webdriver.Chrome(
            options=options, executable_path=ChromeDriverManager().install()
        )
        self.browser.get("https://www.xior-booking.com/#")
        self.browser.maximize_window()

        form = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "form-select")))
        print(form)

    def close(self):
        self.browser.quit()

    def click_option(self, option_id, text):
        time.sleep(1)
        option_button = self.browser.find_element(By.ID, option_id)
        option_button.click()
        time.sleep(1)
        option = option_button.find_element(By.XPATH, f"//option[contains(text(),'{text}')]")
        option.click()

    def get_results(self, data):
        self.browser.refresh()
        if 'country' in data:
            self.click_option("country", data['country'])
        if 'city' in data:
            self.click_option("city", data['city'])
        self.click_option("unlock_key", "Without code")

        time.sleep(1)
        search_results = self.browser.find_element(By.ID, "search-results")
        time.sleep(1)
        results = search_results.find_elements(By.CLASS_NAME, "card")
        lista = []
        for result in results:
            lista.append({"url": result.find_element(By.TAG_NAME, "a").get_attribute("href")})
        return lista


    def get_data_delft(self):
        return self.get_results(self.data_delft)

    def get_working_data(self):
        return self.get_results(self.working_data)


if __name__ == "__main__":
    scraper = None
    try:
        scraper = XiorScraper()
        print(scraper.get_working_data())
    except:
        traceback.print_exc()
    finally:
        scraper.close()
