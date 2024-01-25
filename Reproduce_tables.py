
from selenium.webdriver.common.by import By
import zipfile,glob
import webbrowser,shutil,os
import time, csv


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

def Get_Atomic_Test_Data(driver):

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


#Fetches the test data for testing polarizability. The test data here is
# the Version 3 downloaded data.
def Get_Polarizability_Test_Data(driver,url,data_directory,element):

    # load the web page
    driver.get(url)

    driver.implicitly_wait(10)

    test_table_dictionary = {}

    WebElement = ''

    # Find the Download CSV button and click it.
    try:
       WebElement = driver.find_element(By.XPATH,'//a[@href="'+"/atom/dev/version3/polarizability-files/Li1Pol.zip"+'"]')
    except:
        return test_table_dictionary

    webbrowser.open(WebElement.get_attribute('href'))
  
    time.sleep(5)  

    # Download the zip folder and extract the CSV files.
    path_to_downloaded_zip_folder = data_directory + element + 'Pol.zip'

    path_to_extracted_files = data_directory + element + 'Pol/'
    if(os.path.exists(path_to_extracted_files) == False):
        with zipfile.ZipFile(path_to_downloaded_zip_folder, 'r') as zip_ref:
            zip_ref.extractall(data_directory)


        #On MACOS, an extra folder __MACOSX is created after runnin the unzip command.
        #Remove this folder if present
        MACOSX_folder = data_directory + '/__MACOSX'
        if(os.path.exists(MACOSX_folder)):
            shutil.rmtree(MACOSX_folder)

    #List all the extracted CSV files
    csv_files = glob.glob(path_to_extracted_files + '*.csv')

    for file_path in csv_files:
        with open(file_path, mode ='r')as file:
            file_content = list(csv.reader(file))
            header = file_content[0]
            state = header[1]
            file_content.remove(header)
            test_table_dictionary[state] = file_content

    return test_table_dictionary
