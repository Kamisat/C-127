from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


scraped_data = []

url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))
browser.get(url)

soup = BeautifulSoup(browser.page_source, "html.parser")


def scrape():
    bright_star_table = soup.find("table", attrs = {"class", "wikitable sortable jquery-tablesorter"})
    table_body = bright_star_table.find("tbody")

    table_rows = table_body.find_all("tr")

    for row in table_rows:
        table_cols = row.find_all("td")
        print(table_cols)
        temp_list = []

        for col_data in table_cols:
            data = col_data.text.strip()
            print(data)
            temp_list.append(data)
        scraped_data.append(temp_list)

    stars_data = []
    for i in range(0, len(scraped_data)):

        names = scraped_data[i][1]
        distance = scraped_data[i][3]
        mass = scraped_data[i][5]
        radius = scraped_data[i][6]
        lum = scraped_data[i][7]

        required_data = [names, distance, mass, radius, lum]
        stars_data.append(required_data)
    
    headers = ["Star Name", "Distance", "Mass", "Radius", "Luminosity"]
    star_df_1 = pd.DataFrame(stars_data, columns = headers)
    star_df_1.to_csv("scraped_data.csv", index = True, index_label = "id")


scrape()