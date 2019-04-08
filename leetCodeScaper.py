import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import unittest
import time
import csv
import pandas as pd

class loginScraper(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://leetcode.com/accounts/login/')

    def test_login(self):
        driver = self.driver
        f = open('credentials.txt', 'r')
        credList = f.read().split('\n')
        f.close()
        leetCodeUsername = credList[0]
        leetCodePass = credList[1]

        userId = 'username-input'
        passId = 'password-input'
        buttonPath = '//button[@id="sign-in-button"]'

        emailFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(userId))
        passFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passId))
        loginButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(buttonPath))
        emailFieldElement.clear()
        emailFieldElement.send_keys(leetCodeUsername)
        passFieldElement.clear()
        passFieldElement.send_keys(leetCodePass)
        time.sleep(2)
        loginButtonElement.click()
        time.sleep(3)

        top100Path = '//a[@href="/problemset/top-100-liked-questions/"]'
        top100Q = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(top100Path))
        top100Q.click()
        time.sleep(2)

        #use src for BeautifulSoup Scraping
        src = driver.page_source 
        df = pd.DataFrame()
        df = self.scrape(src, 'https://leetcode.com/problemset/top-100-liked-questions/', df)
        
        nextPagePath = '//a[@href="#page-2"]'
        nextPageBut = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(nextPagePath))
        nextPageBut.click()
        time.sleep(2)

        src = driver.page_source
        df = self.scrape(src, 'https://leetcode.com/problemset/top-100-liked-questions/#page-2', df)
        self.dfToCSV(df)



    def scrape(self, src, url, df):
        soup = BeautifulSoup(src, features='html.parser')
        table_body = soup.find('tbody')
        rows = table_body.find_all('tr')
        table = []
        baseurl = 'https://leetcode.com'
        for row in rows:
            cols = row.find_all('td')
            link = row.find_all('a', href=True)
            link = link[0]['href']
            tempUrl = baseurl + link
            cols = [x.text.strip() for x in cols]
            del cols[0]
            del cols[2]
            del cols[4]
            cols.append(tempUrl)
            table.append(cols)

        #headers = ['ID', 'Question Name', 'Acceptance', 'Difficulty']
        df1 = pd.DataFrame(table)
        df = df.append(df1)
        return df

    def dfToCSV(self, df):
        df.to_csv('LeetCodeTop100.csv', header=['ID', 'Question Name', 'Acceptance', 'Difficulty', 'URL'], index=False)
        

if __name__=='__main__':
    unittest.main()