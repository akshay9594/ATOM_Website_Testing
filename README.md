
# ATOM Website Testing

This README provides instructions on how to run the scripts to test
Version 3 against Version 2 of the website. Details about the 
various directories has also been provided.

## Dependencies

1. Software level
    (a) Python 3.0 and above
    (b) Google Chrome

2. Python packages
    (a) Selenium
    (b) bs4
    (c) requests
    (d) html_table_parser

## Directory Structure

    Directories and what they contain:
    1. Data - Stores all the downloaded data (Ground truth and Test)
              according to the properties

    2. fetch_Gnd_Truth_Data - Contains scripts from fetching the
                        ground truth data

    3. test_scripts - Contains scripts that perform the actual testing
                      for each property

    4. root directory - Contains the master script and some utility scripts

## Installing Python packages

    Install the required python packages using pip or pip3 package manager,
    Using the command:
    ```python
    pip3 install -r requirements.txt
    ```
    ***Note: A package that is not listed but requried is "BeautifulSoup4".
    The reason it is not listed is that installing through the text file
    creates issues which are yet to be understood (possibly conflicts with the pacakge
    html_table_parser). Install this package after installing the packages within
    requirements.txt as follows:
    ```
    pip3 install bs4
    ```

## Running the scripts and testing

    The master script is the "dynamic_scrape_and_test.py" script. Run this script
    using the following command: 
    ```
    python3 dynamic_scrape_and_test.py
    ```
    An interactive menu opens prompting the user to choose the property to test for.
    Choose a property by entering the appropriate number. Once a selection is made
    the testing initiates.

    For more details about the mismatched data, run the master script using the flag
    "-v" as follows:
    ```
    python3 dynamic_scrape_and_test.py -v
    ```

    Note: The ground truth and test data have already been downloaded and placed in
          the "Data" directory. This is just to save time for testing of these
          scripts. Going forward every run of the master script will open the ground
          truth and test websites and download the requried data.

## Constraints (As of Now)

1. The element to be tested is set to "Li" within the master script. 

2. Rows of Test and Ground truth tables are matched. It is a string
   match because of the way data is displayed on the website.