import requests
from bs4 import BeautifulSoup
import pandas as pd

class WebsiteScraper():
    def __init__(self, url):
        self.url = url

    def scrape_and_save(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            parsed_data = BeautifulSoup(response.text, "html.parser")
            article_elements = parsed_data.find_all("h2", class_="c-card__title")
            data = []

            for article in article_elements:
                article_title = article.find("a")
                if article_title:
                    title = article_title.text.strip()
                    link = article_title.get("href")
                    author_element = article.find_next("a", class_="c-card__author-name")
                    if author_element:
                        author_name = author_element.text.strip()
                    else:
                        author_name = "Unknown"
                    date_element = article.find_next("div", class_="c-card__time")
                    if date_element:
                        date = date_element.find("time")
                        if date:
                            date_text = date.get("datetime")
                        else:
                            date_text = "N/A"
                    else:
                        date_text = "N/A"

                    data.append([title, link, author_name, date_text])

            framed_data = pd.DataFrame(data, columns=["Article_Titles", "Links", "Authors", "Date"])
            data_file= "article_data.csv"
            framed_data.to_csv(data_file, index=False)
            print(f"data has been stored in article_data.csv{data_file}")
        else:
           return "Could not fetch data from the provided webpage"

if __name__=="__main__":

    url = "https://threatpost.com/"
    scraper = WebsiteScraper(url)
    scraper.scrape_and_save()
 