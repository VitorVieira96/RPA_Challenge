from RPA.Browser.Selenium import Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from robocorp.tasks import task
from setup import URL, SEARCH_PHRASE,NUMBER_OF_MONTHS
from util import (

    write_csv_data,
    download_image_from_url,
    check_for_dolar_sign,
    date_limit,
    format_date,
    create_image_folder,
    count_matches,
)


class SeleniumScraper:
    def __init__(self):
        self.browser_lib = Selenium()

    def close_browser(self) -> None:
        self.browser_lib.close_browser()

    def open_website(self, url: str) -> None:
        self.browser_lib.open_available_browser(url)
        self.browser_lib.maximize_browser_window()
        #driver.execute_script("window.FSR.setFSRVisibility(true);")
                              
    def get_element_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_text(path)
        return ""

    def get_image_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_element_attribute(path, "src")
        return ""

    def begin_search(self, search_phrase: str) -> None:
        try:
            search_xpath = "//button[@data-element='search-button']"
            self.browser_lib.click_button_when_visible(locator=search_xpath)
            field_xpath = "//input[@name='q']"
            self.browser_lib.input_text(locator=field_xpath, text=search_phrase)
            go_button_xpath = "//button[@type='submit']" 
            self.browser_lib.click_button_when_visible(locator=go_button_xpath)
        except ValueError as e:
            raise f"Error on execution of begin_search -> {e}"

    def sort_newest_news(self, list_value="1") -> None:
        try:
            sort_dropdow_btn = "//select [@class='select-input']"
            self.browser_lib.select_from_list_by_value(sort_dropdow_btn, list_value)

        except ValueError as e:
            raise f"Error on execution of sort_newest_news -> {e}"

    def extract_website_data(self, search_phrase: str) -> None:
        extracted_data = [
            ["Title",
            "Description",
            "Date",
            "Picture File Name",
            "Search phrases in the title and description",
            "Contains Dollar sign"]
        ]

        dt_limit = date_limit(NUMBER_OF_MONTHS)

        element_list = "//ps-promo[@class='promo promo-position-large promo-medium']"
        
        title_xpath = "//h3/a[@class='link']"
        #title_xpath = "//ps-promo[@class='promo promo-position-large promo-medium']//h3/a[@class='link']"
        title_field = self.browser_lib.get_webelements(title_xpath)
        description_xpath = "//p[@class='promo-description']"
        #description_xpath = "//ps-promo[@class='promo promo-position-large promo-medium']//p[@class='promo-description']"
        description_field = self.browser_lib.get_webelements(description_xpath)
        date_xpath = "//p[contains(@class, 'promo-timestamp')]"
        #date_xpath = "//ps-promo[@class='promo promo-position-large promo-medium']//p[contains(@class, 'promo-timestamp')]"
        date_field = self.browser_lib.get_webelements(date_xpath)

        while(True):
            news_list_elements = self.browser_lib.get_webelements(element_list)
            for i in range(1, len(news_list_elements)+1):
                title = self.get_element_value(f"//li[{i}]{element_list}{title_xpath}")
                description = self.get_element_value(f"//li[{i}]{element_list}{description_xpath}")
                date = self.get_element_value(f"//li[{i}]{element_list}{date_xpath}")
                formated_date = format_date(date)
                if dt_limit > formated_date:
                    break
                self.get_element_value(f"{element_list}//span[@data-testid]")
                image = download_image_from_url(
                self.get_image_value(f"//li[{i}]{element_list}//img[@class='image']")
                )
                extracted_data.append(
                    [
                    title,
                    description,
                    formated_date.strftime("%B %d, %Y"),
                    image,
                    count_matches( SEARCH_PHRASE, title + description),
                    check_for_dolar_sign(title + description)
                    ]
                )
            if dt_limit > format_date(date):
                write_csv_data(extracted_data)
                break
            self.click_next_page()


    def click_next_page(self) -> None: 
        next_xpath = "//div[@class ='search-results-module-next-page']/a"
        next_page = self.browser_lib.find_element(locator=next_xpath)
        self.browser_lib.go_to(next_page.get_attribute('href'))
        

    def main(self) -> None:
        try:
            create_image_folder()
            self.open_website(url=URL)
            self.click_next_page()
            print("Website open")
            self.begin_search(search_phrase=SEARCH_PHRASE)
            print("Search done")
            self.sort_newest_news()
            print("News Filtered")
            self.extract_website_data(search_phrase=SEARCH_PHRASE)
        finally:
            self.close_browser()

if __name__ == "__main__":
    obj = SeleniumScraper()
    obj.main()
