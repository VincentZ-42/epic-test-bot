from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from private import email, password, path, web_url
import time
import math

# Common static variables
driver = webdriver.Chrome(executable_path=path)
email_input = email
password_input = password
delay = 10
sec = 1
min = 60 * sec
hour = 60 * min
options = {
	'hunt': {'command': 'rpg hunt', 'count': 0, 'cooldown': 1 * min},
	'heal': {'command': 'rpg heal', 'count': 0, 'cooldown': 0},
	'farm': {'command': 'rpg axe', 'count': 0, 'cooldown': 5 * min - delay},
	'open': {'command': 'rpg open', 'count': 0, 'cooldown': 0},
	'loot': {'command': 'rpg buy uncommon lootbox', 'count': 0, 'cooldown': 3 * hour - 36 * delay},
	'adventure': {'command': 'rpg adv', 'count': 0, 'cooldown': 1 * hour - 12 * delay}
	# Add additional options when you figure out how to monitor chat from bot
	# Implement Training n Quest options
}

# This function takes a text input and then uses the enum options to output the command message in chat
def execute_order(choice):
	chat = driver.find_element_by_xpath(xpath)
	chat.send_keys(options[choice]['command'], Keys.RETURN)
	options[choice]['count'] += 1
	if not (choice == 'open' or choice == 'heal'):
		print("\033[1;32;40m{} = {}\033[1;37;40m".format(options[choice]['command'], options[choice]['count']), flush=True)
	time.sleep(1)
	# Sleep instead of adding to time_passed b/c other command conditions need
	# to be met and we would skip right through it if we added seconds here
	# Plus: this sleeping time accounts for the latency

# This function is our one second timer
def one_second():
	time.sleep(1)
	return 1

#These variable functions adjusts the timer to display correct time passed
adjust_by_10 = lambda x : math.ceil(x / 10) % 6 * 10
adjust_by_5 = lambda x : math.ceil(x / 5) % 12 * 5

# This function takes an integer, time_passed, and displays it on the terminal
def time_display(time_passed):
	if time_passed % 60 == 0:
		print("{}".format(60))
	elif time_passed % 10 == 0:
		print("{}".format(adjust_by_10(time_passed)))
	elif time_passed % 5 == 0:
		print("{}".format(adjust_by_5(time_passed)), end='', flush=True)
	else:
		print(".", end='', flush=True)

# This part enters email and password into login web page
driver.set_page_load_timeout("10")
driver.get(web_url)
email = driver.find_element_by_css_selector("[type=email]")
password = driver.find_element_by_css_selector("[type=password]")
email.send_keys(email_input)
password.send_keys(password_input, Keys.RETURN)
time.sleep(6)

# This part identifies the chatbox element on webpage and begins our program with the message "Let's start"
xpath = '//*[@id="app-mount"]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div[1]/form/div/div/div/div[3]/div/div/span/span/span'
chatbox = driver.find_element_by_xpath(xpath)
chatbox.send_keys("Let's start", Keys.RETURN)
time.sleep(1)
xpath = '//*[@id="app-mount"]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div[1]/form/div/div/div/div[3]/div[2]/div/span/span/span'

# Initiate variables and change according to your own needs
time_passed = 0
healing_interval = 1
open_lootbox_interval = 10

# This infinite while loop is the script that operates continuously until canceled on terminal by host

while True:
	time_display(time_passed)
	if time_passed % options['loot']['cooldown'] == 0:
		execute_order('open')
		execute_order('loot')
		execute_order('open')
	if time_passed % options['adventure']['cooldown'] == 0:
		execute_order('heal')
		execute_order('adventure')
		execute_order('heal')
	if time_passed % options['farm']['cooldown'] == 0:
		execute_order('farm')
	if time_passed % options['hunt']['cooldown'] == 0:
		execute_order('hunt')
	if options['hunt']['count'] % healing_interval == 0:
		execute_order('heal')
			# Open any earned lootboxes
	if options['hunt']['count'] % open_lootbox_interval == 0:
		execute_order('open')
	time_passed += one_second()

# # Ctrl + C to stop script from running

# # Ways to improve....
# # Find a way to read reply from webpage and react to
# # 1. Surprise lootboxes
# # 2. Enemy ambushes

# -------------------- This is the old code -------------------------------------------
# seconds = 0
# hunt_count = 0
# farm_count = 0
# adv_count = 0
# potions_used = 0

# hunt_msg = 'rpg hunt'
# farm_msg = 'rpg chop'
# adv_msg = 'rpg adv'

# def on_the_prowl(hunt, path, prey):
# 	chat = driver.find_element_by_xpath(path)
# 	chat.send_keys(hunt, Keys.RETURN)
# 	prey += 1
# 	print("prey hunted = {}".format(prey))
# 	return prey

# def in_the_field(farm, path, crops):
# 	chat = driver.find_element_by_xpath(path)
# 	chat.send_keys(farm, Keys.RETURN)
# 	crops += 1
# 	print("crops harvested = {}".format(crops))
# 	return crops

# def adventure_time(adv, path, journeys):
# 	chat = driver.find_element_by_xpath(path)
# 	chat.send_keys(adv, Keys.RETURN)
# 	journeys += 1
# 	print("journeys taken = {}".format(journeys))
# 	return journeys

# while True:
# 	# Cooldown for adventure is 45 min
# 	# Cooldown for training is 15 min
# 	# Cooldown for farming is 5 min
# 	# the timing for these are a bit off......
# 	# minus 4 seconds because of cumlative delays from 5 hunts
# 	# if seconds % (3600 - 70) == 0:		# adventure cooldown = 1 hour
# 	# 	adv_count = adventure_time(adv_msg, xpath, adv_count)
# 	# 	time.sleep(1)
# 	if seconds % (300 - 4) == 0:		# farming cooldown = 5 mins
# 		farm_count = in_the_field(farm_msg, xpath, farm_count)
# 		time.sleep(1)
# 		# hunt_count = on_the_prowl(hunt_msg, xpath, hunt_count)
# 	if seconds % 60 == 0:		# hunt cooldown = 1 min
# 		hunt_count = on_the_prowl(hunt_msg, xpath, hunt_count)
# 		time.sleep(1)
# 	# if hunt_count % 3 == 0 & seconds % 60 == 0:
# 	# 	potions_used = on_the_prowl("rpg heal", xpath, potions_used)
# 	# 	time.sleep(1)
# 	seconds += one_second()