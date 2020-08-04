from selenium import webdriver
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'hashthat\\venv\Scripts\geckodriver.exe')


browser = webdriver.Firefox(executable_path=path)
browser.get('http://127.0.0.1:8000/')

assert browser.page_source.find('install') < 0

