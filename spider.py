from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import logging
from setlog import setlog
logging = setlog()

class TradeSpider(object):
    # Constructor for the TradeSpider class
    def __init__(self):
        logging.info("start TradeSpider!")  # Log the start of the spider

    # Method to set up the web driver
    def setDriver(self):
        self.driver = webdriver.PhantomJS()  # Initialize the PhantomJS driver
        # Uncomment the below code to use Firefox with headless options
        # options = Options()
        # options.add_argument("--headless")
        # self.driver = webdriver.Firefox(
        #     firefox_options=options, executable_path='./geckodriver')

    # Method to log in to the website
    def login(self, ac, pw):
        url = "https://www.trademap.org/Country_SelProduct_TS.aspx"  # Target URL
        self.driver.get(url)  # Load the webpage
        wait = WebDriverWait(self.driver, 10)  # Set wait time for elements to load
        # Click the login button
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="ctl00_MenuControl_Label_Login"]'))).click()
        # Switch to the login iframe
        wait.until(
            EC.frame_to_be_available_and_switch_to_it('iframe_login'))
        # Enter the username
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="PageContent_Login1_UserName"]'))).send_keys(ac)
        # Enter the password
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="PageContent_Login1_Password"]'))).send_keys(pw)
        # Click the login button
        self.driver.find_element_by_xpath(
            '//*[@id="PageContent_Login1_Button"]').click()

        # Check if the login was successful
        self.driver.switch_to_default_content()
        soup = bs(self.driver.page_source, "lxml")
        if "Trade Map" in soup.title.text:
            logging.info("ITC login success!")  # Log successful login
        else:
            logging.error("login failed")  # Log failed login

    # Method to select the type of record (Exports or Imports)
    def setRecords(self, n):
        '''
        Records = ["Exports", "Imports"]
        option = [1,2]  # 1 for Exports, 2 for Imports
        '''
        wait = WebDriverWait(self.driver, 10)
        # Click the dropdown option corresponding to the record type
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/form/div[3]/div[5]/table/tbody/tr[4]/td[2]/div/table/tbody/tr/td[3]/div[1]/select/option[{}]'.format(
                    str(n))
            ))).click()
        Records = ["Exports", "Imports"]
        logging.debug("setRecords " + Records[n - 1])  # Log the selected record type

    # Method to set the trade indicators (Values or Quantities)
    def setIndicators(self, n):
        '''
        Indicators = ["Values", "Quantities"]
        option = [1,2]  # 1 for Values, 2 for Quantities
        '''
        xpath = '/html/body/form/div[3]/div[5]/table/tbody/tr[4]/td[2]/div/table/tbody/tr/td[3]/div[4]/select/option[{}]'.format(
            str(n))
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        Indicators = ["Values", "Quantities"]
        logging.debug("setIndicators " + Indicators[n-1])  # Log the selected indicator

    # Method to set the time series page
    def setTimePage(self):
        wait = WebDriverWait(self.driver, 10)
        # Set the time series to "20 per page"
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/form/div[3]/div[5]/table/tbody/tr[4]/td[2]/div/table/tbody/tr/td[3]/div[2]/select/option[4]'
            ))).click()
        # Set the rows per page to "300 per page"
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/form/div[3]/table/tbody/tr[2]/td/div[1]/table/tbody/tr[2]/td[6]/div/select/option[7]'
            ))).click()
        logging.debug("set TimePage")  # Log the settings

    # Method to select the desired product
    def selectProducts(self, n):
        '''
        n: Select the nth option from the Products dropdown
        '''
        n = str(n)
        time.sleep(3)  # Pause to allow the page to load
        wait = WebDriverWait(self.driver, 10)
        # Select the product based on its option number
        xpath = "/html/body/form/div[3]/div[5]/table/tbody/tr[1]/td/div/table/tbody/tr/td[3]/select/option[{}]".format(
            n)
        item = wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).text
        logging.info("selectProducts: " + item)  # Log the selected product
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    # Method to save the extracted data
    def save(self, filename):
        table_source = self.driver.find_element_by_xpath(
            '/html/body/form/div[3]/table/tbody/tr[3]/td').get_attribute('innerHTML')
        df = pd.read_html(table_source)[0]  # Parse the table data into a DataFrame
        df.to_pickle(filename+'.pickle')  # Save the DataFrame to a pickle file
        logging.info("save {}.pickle".format(filename))  # Log the save operation

    # Method to display the DataFrame
    def showdf(self):
        table_source = self.driver.find_element_by_xpath(
            '/html/body/form/div[3]/table/tbody/tr[3]/td').get_attribute('innerHTML')
        df = pd.read_html(table_source)[0]  # Parse the table data into a DataFrame
        print(df.head())  # Print the first few rows of the DataFrame

    # Method to close the web driver
    def close(self):
        self.driver.close()  # Close the driver
        logging.info("Close Driver!!")  # Log the driver closure

if __name__ == "__main__":
    ac = "chroma.favours@icloud.com"  # Account username
    pw = "PKNrKASJRZzYt4?*=)"  # Account password
    s = TradeSpider()  # Instantiate the TradeSpider class
    s.setDriver()  # Set up the web driver
    s.login(ac, pw)  # Log in to the website
    s.setTimePage()  # Set the time series page
    for n in [5, 12, 10]:  # Select products by option number
        s.selectProducts(n)
    s.setRecords(1)  # Set the record type to Exports
    s.setIndicators(1)  # Set the indicator to Values
    # s.save("test")  # Save the data (commented out)
    s.showdf()  # Display the DataFrame
    s.close()  # Close the driver
