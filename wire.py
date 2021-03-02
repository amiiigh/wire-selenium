from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
from datetime import datetime
import os
from pathlib import Path

password_path = Path('../passwords.txt')

DOWNLOAD_PATH = os.path.abspath(os.getcwd() + '/download')

def get_credentials(n: 'line # (zero based) in password file for the sender/receiver credentials pair') -> 'dictionary':
	with open(password_path) as password_file:
		lines = password_file.readlines()
		words = lines[n].strip().split()
		return {'sender': (words[0], words[1]), 'receiver': (words[2], words[3])}

def send_text(driver, text):
	input_bar = driver.find_element_by_id('conversation-input-bar-text')
	input_bar.send_keys(text, Keys.RETURN)
	input_bar.send_keys(Keys.RETURN)

def logout(driver):
	settings_button = driver.find_element_by_class_name("conversations-settings")
	settings_button.click()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log out')]"))).click()
	# log_out_modal = driver.find_element_by_xpath("//*[@id='modals']/modal/div/div/div[2]/div[3]/input[2]")
	# log_out_modal.click()

def login(driver, username, password):
	driver.get("https://app.wire.com")
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-uie-name="go-login"]'))).click()
	username_field = driver.find_element_by_name("email")
	username_field.send_keys(username)
	password_field = driver.find_element_by_name("password-login")
	password_field.send_keys(password)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@data-uie-name="enter-public-computer-sign-in"]'))).click()
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-uie-name="do-sign-in"]'))).click()
	#ignore history confirm

	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-uie-name="do-history-confirm"]'))).click()

def get_message_type(message):
	if len(message.find_elements(By.XPATH, './/image-asset')) >0:
		return 'IMAGE'
	elif len(message.find_elements(By.XPATH, './/file-asset')) >0:
		return 'FILE'
	else:
		return 'TEXT'

def log_time(file):
	file.write(str(datetime.now().timestamp()))
	file.write('\n')
	file.flush()

def get_messages(driver):
	messages = driver.find_elements(By.CLASS_NAME, 'message')
	return messages

def go_to_chat(driver, buddy):
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.TAG_NAME, "conversations-recent-icon"))).click()
	chat = driver.find_element_by_xpath("//*[contains(text(),'"+ buddy +"')]/../..")
	chat.click()

def delete_files():
	print(DOWNLOAD_PATH)
	files_path = [os.path.abspath(x) for x in os.listdir(DOWNLOAD_PATH)]
	for f in files_path:
		os.remove(f)
	print('Download Folder has been cleared!')

def download_file(message):
	while True:
		loading = message.find_elements(By.XPATH, '//div[@class="asset-placeholder loading-dots"]')
		if len(loading) == 0:
			print('Loading complete!')
			break
	message.find_element(By.XPATH, './/div[@data-uie-name="file"]').click()
	print('Downloading ... ')
	while True:
		icon = message.find_elements(By.XPATH, './/div[@data-uie-name="file-icon"]')
		if len(icon) == 1:
			print('Download complete!')
			break
	delete_files()


def send_picture(driver, filepath):
	driver.find_element_by_xpath("//*[@id='conversation-input-bar-photo']/input").send_keys(filepath)

def send_file(driver, filepath):
	driver.find_element_by_xpath("//*[@id='conversation-input-bar-files']/input").send_keys(filepath)
