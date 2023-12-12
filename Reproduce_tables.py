
from selenium.webdriver.common.by import By

#Function to scrape table column titles from the HTML
def Reproduce_Column_titles(driver):
    reproduced_titles = []
    try:
        column_titles = driver.find_elements(By.TAG_NAME, "th")
    except:
        return reproduced_titles
    
    if(len(column_titles)>0):
        for title in column_titles:
            reproduced_titles.append(title.text)
    return reproduced_titles

#Function to scrape the data within table columns from the HTML
def Reproduce_Data(driver):
    reproduced_data = []
    try:
        rows = driver.find_elements(By.TAG_NAME, "tr")
    except:
        return reproduced_data
    
    for row in rows:
    #print ii.tag_name
        cols = row.find_elements(By.TAG_NAME, "td")
        row_data = []
        if(len(cols) > 0):
            for entry in cols:
                row_data.append(entry.text)
            reproduced_data.append(row_data)

    return reproduced_data


#Atomic data tables reproduced in a different way (A better routine than the above two routines)
# TODO: Replace above two routines with this routine for all element properties.

def Reproduce_Atomic_Tables(driver):

    Reproduced_tables = []
    WebElement_tables_list = []

    try:
       WebElement_tables_list = driver.find_elements(By.XPATH,"//table[contains(@class, 'table-auto text-center')]")
    except:
        return WebElement_tables_list
    
    # Going through each table element and reproducing the table from the element
    for WebElement_table in WebElement_tables_list:
   
        #Table header web element
        table_head = WebElement_table.find_element(By.TAG_NAME,"thead")

        table_WebElement_Column_titles = table_head.find_elements(By.TAG_NAME, "th")

        table_body = WebElement_table.find_element(By.TAG_NAME,"tbody")

        #Reproducing table column titles
        table_Column_titles = []
        for WebElement in table_WebElement_Column_titles:
            table_Column_titles.append((WebElement.text).replace("\n","").replace("Ref",""))


        #Reproducing table data from each Web element row
        table_WebElement_rows = table_body.find_elements(By.TAG_NAME, "tr")
        table_data = []
        for WebElement_row in table_WebElement_rows:
            #Getting the entries in each row
            Entries_WebElement = WebElement_row.find_elements(By.TAG_NAME, "td")
            
            row_data = []
            if(len(Entries_WebElement)>0):
                #Saving each entry
                for entry in Entries_WebElement:
                    row_data.append(entry.text)

                table_data.append(row_data)

        #Putting the table together [Column titles,table Data]
        table_data.insert(0,table_Column_titles)
        Reproduced_tables.append(table_data)

    return Reproduced_tables