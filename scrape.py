import config
from scrape_utils import Earth2Scraper

e2s = Earth2Scraper(config.silent_mode, config.language, config.chromedriver_path)
e2s.init_browser()
e2s.go_to_marketplace()
_ = e2s.scrape_all_country_info(export=True, delay_sec=config.delay_sec)
