
from selenium.webdriver.common.by import By

#Function to scrape table column titles from the HTML
def Reproduce_Column_titles(driver):
    column_titles = driver.find_elements(By.TAG_NAME, "th")
    reproduced_titles = []
    if(len(column_titles)>0):
        for title in column_titles:
            reproduced_titles.append(title.text)
    return reproduced_titles

#Function to scrape the data within table columns from the HTML
def Reproduce_Data(driver):
    rows = driver.find_elements(By.TAG_NAME, "tr")
    reproduced_data = []
    for row in rows:
    #print ii.tag_name
        cols = row.find_elements(By.TAG_NAME, "td")
        row_data = []
        if(len(cols) > 0):
            for entry in cols:
                row_data.append(entry.text)
            reproduced_data.append(row_data)

    return reproduced_data