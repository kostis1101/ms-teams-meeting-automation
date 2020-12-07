from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import re
from selenium.common.exceptions import *


emailaddress =  "" # put your email here
password = "" # put your password here

if not emailaddress:
        emailaddress = input('please enter your e-mail address: ')
if not password:
        password = input('Please enter your password: ')

options = Options()
options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1
  })

driver = webdriver.Chrome(options=options)
driver.get('https://teams.microsoft.com')

def go_to_teams(email, password):
	#---- SIGNS IN ----#

	email_field = WebDriverWait(driver, 10).until(
		        EC.presence_of_element_located((By.ID, "i0116"))
		    )
	email_field.send_keys(emailaddress)

	goon = False
	
	next_button = driver.find_element_by_id('idSIButton9')
	while not goon:
		try:
			goon = True
			next_button.click()
		except ElementNotInteractableException:
			pass

	# time.sleep(2)
	try:
		password_field = WebDriverWait(driver, 10).until(
		        EC.presence_of_element_located((By.ID, "i0118"))
		    )
	except:
		print('something went wrong')
		driver.quit()
	print('password field found')
	password_field.send_keys(password)
	print(password_field)

	signin_button = driver.find_element_by_id('idSIButton9')
	procced = False
	while not procced:
		try:
			signin_button.click()
			procced = True
		except:
			try:
				signin_button = driver.find_element_by_id('idSIButton9')
			except:
				time.sleep(1)

	next_button = WebDriverWait(driver, -1).until(
		        EC.presence_of_element_located((By.ID, "idSIButton9"))
		    )
	procced = False
	while not procced:
		try:
			next_button.click()
			procced = True
		except:
			next_button = driver.find_element_by_id('idSIButton9')

	use_web_app_link = driver.find_element_by_class_name('use-app-lnk')
	use_web_app_link.click()

def join_active_meeting():
	#---- GOES TO CALENDER ----#
	time.sleep(5)
	print('going to calender')
	try:
		calender_button = WebDriverWait(driver, 60).until(
		        EC.presence_of_element_located((By.ID, "app-bar-ef56c0de-36fc-4ef8-b417-3d82ba9d073c"))
		    )
	except:
		print('something went wrong')
		driver.quit()

	calender_button.click()

	# time.sleep(10)

	#---- FIND ACTIVE CALL ----#

	calender_items = driver.find_elements_by_class_name('node_modules--msteams-bridges-components-calendar-event-card-dist-es-src-renderers-event-card-renderer-event-card-renderer__eventCard--h5y4X')

	items_amount = len(calender_items)
	while items_amount == 0:
		calender_items = driver.find_elements_by_class_name('node_modules--msteams-bridges-components-calendar-event-card-dist-es-src-renderers-event-card-renderer-event-card-renderer__eventCard--h5y4X')
		items_amount = len(calender_items)
		time.sleep(0.2)

	active_call = False

	while not active_call:
		print('waiting for active call...')
		for item in calender_items:
			if 'activeCall' in item.get_attribute('class'):
				item.click()
				active_call = True
				break
		if not active_call:
			time.sleep(30)
	print('itmes in calender amount', len(calender_items))

	#--------- JOIN -----------#

	try:
		join_button = WebDriverWait(driver, 10).until( # '/html/body/div[8]/div/div/div/div[3]/div/div/div[1]/div[2]/div[3]/button[1]' '//*[@id="AAMkADA2ZjczNjZhLWY3ZDItNGIxOS1hNDlhLTgwYzg4ODRkNDhkNwFRAAgI2JpDCljAAEYAAAAAHFaEdm3OaUm8CTp_8I5CngcAW5bPsR-74UCJ-NVJRztGkwAAAAABDQAAW5bPsR-74UCJ-NVJRztGkwAAmZHbOgAAEA=="]/div[2]/button'
		        EC.presence_of_element_located((By.XPATH, '/html/body/div[9]/div/div/div/div[3]/div/div/div[1]/div[2]/div[3]/button[1]'))
		    )
		print(join_button)
	except Exception as e:
		print('something went wrong')
		print('no joining button now')
		join_active_meeting()
	join_button.click()

	# toggle cam-mic
	try:
		toggle_cam = WebDriverWait(driver, 60).until(
		        EC.presence_of_element_located((By.XPATH, '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button'))
		    )
		toggle_mic = WebDriverWait(driver, 60).until(
		        EC.presence_of_element_located((By.XPATH, '//*[@id="preJoinAudioButton"]'))
		    )
	except Exception as e:
		print('something went wrong')
		print(e)

	html = toggle_cam.get_attribute('outerHTML')
	if 'OFF' in html:
		toggle_cam.click()

	html = toggle_mic.get_attribute('outerHTML')
	if 'OFF' in html:
		toggle_mic.click()

	#------ JOIN THE MEETING ------#
	join_button = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
	join_button.click()

def join_scheduled_metting():
	global driver
	print('joining scheduled metting')
	teams = WebDriverWait(driver, 60).until(
		EC.presence_of_element_located(By.CLASS_NAME, 'match-parent team left-rail-item-kb-l2'))
	print(teams)
	for team in teams:
		name = team.find_element_by_class_name('name-channel-type')
		html = name.get_attribute('innerHTML')
		name = re.findall(r'title="(.+)"')
		print(name[0])

def show_participants():
	global driver

	participants_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'roster-button')))
	participants_button.click()

	time.sleep(5)

	'//*[@id="participant-8orgid1c21e24a20e2488bb4c1f669f86e3808"]'
	'//*[@id="participant-8orgid83cef4adfc9640ee8953161429ab1648"]'

	try:
		participants = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-screen/div/div[2]/meeting-panel-components/calling-roster/div/div[2]/div/div[1]/accordion/div/accordion-section[2]/div/calling-roster-section/div/div[2]/div/ul')
	except:
		while participants == None:
			participants = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-screen/div/div[2]/meeting-panel-components/calling-roster/div/div[3]/div/div[1]/accordion/div/accordion-section[2]/div/calling-roster-section/div/div[2]/div/ul')
			time.sleep(.5)
	
	html = participants.get_attribute('innerHTML')

	
	most_participants = 0
	number_of_participants = 0

	in_call = True

	
	while in_call:
		html = participants.get_attribute('innerHTML')
		number_of_participants = len(re.findall(r'</span><!----></skype-status><!----></div></ng-transclude>(.+)', html))
		if number_of_participants > most_participants:
			print(f'there are {number_of_participants} number of people in the call, the most people in the meeting at once were {most_participants}')
			most_participants = number_of_participants
		elif number_of_participants < most_participants * 0.3:
			hangup_button = driver.find_element_by_id('hangup-button')
			driver.execute_script('arguments[0].click();', hangup_button)
			print('hanging up...')
			in_call = False
		time.sleep(5)

	join_active_meeting()


proceed = False

go_to_teams(emailaddress, password)
join_active_meeting()
show_participants()
