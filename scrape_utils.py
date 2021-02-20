import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

from file_utils import save_json

EARTH2_MARKETPLACE_URL = "https://app.earth2.io/#marketplace"


class Earth2Scraper:
    def __init__(
        self,
        silent_mode=True,
        language="en",
        chromedriver_path="chromedriver",
        delay_sec=2,
    ):
        """
        Arguments:
            silent_mode: Assign True to run browser in headless mode.
            language: en/tr
            chromedriver_path: Path to chromedriver
            delay_sec: delay seconds btw requests
        """
        self.silent_mode = silent_mode
        self.language = language
        self.chromedriver_path = chromedriver_path
        self.delay_sec = delay_sec
        self.browser = None

    def init_browser(self):
        """
        Creates a browser object, given input parameters.

        Sets:
            self.browser: A selenium browser object (webdriver.chrome.webdriver.WebDriver)
        """
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--lang=" + self.language)
        if self.silent_mode == 1:
            chrome_options.add_argument("--headless")

        # init browser
        browser = webdriver.Chrome(
            executable_path=self.chromedriver_path, options=chrome_options
        )
        self.browser = browser

    def press_enter(self):
        assert self.browser is not None, "init browser first"
        self.browser.find_element_by_name("Value").send_keys(Keys.RETURN)

    def go_to_url(self, url):
        self.browser.get(url)

        # delay
        time.sleep(self.delay_sec)

    def go_to_marketplace(self):
        self.go_to_url(EARTH2_MARKETPLACE_URL)

    def click_to_filter_by_country_flag(self):
        assert (
            self.browser.current_url == EARTH2_MARKETPLACE_URL
        ), "go to marketplace first"

        # click to filter by country button
        xpath = (
            "/html/body/app/content-holder/marketplace/div[2]/div[1]/div[2]/div/div/div"
        )
        elements = self.browser.find_elements_by_xpath(xpath)
        elements[0].click()

    def select_country(self, country_code="IT"):
        assert (
            self.browser.current_url == EARTH2_MARKETPLACE_URL
        ), "go to marketplace first"

        self.click_to_filter_by_country_flag()

        elements = self.browser.find_elements_by_xpath(
            '//li[contains(@data-country-code, "%s")]' % country_code
        )
        elements[0].click()

        # delay
        time.sleep(self.delay_sec)

    def price_per_tile(self, map_url):
        """
        Returns price per tile of the first row as str.
        """
        try:
            # open map url
            self.go_to_url(map_url)
            # find market value per tile
            elements = self.browser.find_elements_by_xpath(
                "//div[@class='price-secondary']"
            )
            per_tile = elements[0].text.split("E$")[1].split(")")[0]
        except:
            per_tile = "0"

        # switch back to marketplace page
        self.go_to_marketplace()

        return per_tile

    @property
    def map_url(self):
        """
        Returns map url of the first row as str.
        """
        assert (
            self.browser.current_url == EARTH2_MARKETPLACE_URL
        ), "go to marketplace first"

        try:
            search_text = "row"
            elements = self.browser.find_elements_by_xpath(
                '//div[@class="%s"]' % search_text
            )
            elements = elements[0].find_elements_by_xpath(".//a[@href]")
            for element in elements:
                if element.text == "BUY":
                    map_url = element.get_attribute("href")
        except:
            map_url = ""

        return map_url

    @property
    def country_list(self):
        assert (
            self.browser.current_url == EARTH2_MARKETPLACE_URL
        ), "go to marketplace first"

        self.click_to_filter_by_country_flag()

        elements = self.browser.find_elements_by_xpath("//li[@data-country-code]")
        country_list = []
        for element in elements:
            country_code = element.get_attribute("data-country-code")
            country_name = element.text
            country_list.append(
                {"country_code": country_code, "country_name": country_name}
            )

        self.click_to_filter_by_country_flag()

        return country_list

    def scrape_all_country_info(
        self,
        export=False,
    ):
        self.go_to_marketplace()
        country_list = self.country_list

        all_country_info = []
        for country in tqdm(country_list):
            self.select_country(country_code=country["country_code"])
            map_url = self.map_url
            price_per_tile = self.price_per_tile(map_url)
            country_info = {
                "country_name": country["country_name"],
                "country_code": country["country_code"],
                "price_per_tile": price_per_tile,
                "map_url": map_url,
            }
            if export:
                save_path = "data/{}/{}".format(
                    time.strftime("%Y%m%d"), country["country_code"]
                )
                save_json(country_info, save_path)
            all_country_info.append(country_info)
        all_country_info.sort(key=lambda x: float(x["price_per_tile"]), reverse=False)
        if export:
            save_path = "data/{}/{}".format(time.strftime("%Y%m%d"), "all")
            save_json(all_country_info, save_path)
        return all_country_info
