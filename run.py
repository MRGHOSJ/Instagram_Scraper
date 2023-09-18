import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random


# This will ask the user to give the instagram acc credentials
def prompt_credentials():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    return username, password


def navigate_to_profile(bot, userToScrap):
    bot.get(f"https://www.instagram.com/{userToScrap}/")
    time.sleep(3.5)

# This will try to auth with the user credentials
def login(bot, username, password):
    bot.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
    time.sleep(random.randint(1,10))

    form_element = bot.find_element(By.CSS_SELECTOR, "._ab3b")
    
    username_input = form_element.find_element(By.XPATH, "//*[@aria-label='Phone number, username, or email']")
    username_input.send_keys(username)
    time.sleep(random.randint(1,10))

    username_input = form_element.find_element(By.XPATH, "//*[@aria-label='Password']")
    username_input.send_keys(password)
    time.sleep(random.randint(1,10))

    button_element = form_element.find_element(By.XPATH, "//*[@type='submit']")
    button_element.click()

# Scrap followers will go to the desired user and check the followers

def scrape_followers(bot, userToScrap):
    navigate_to_profile(bot,userToScrap)
    WebDriverWait(bot, 15).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]")))
    num_followers = get_followers_count(bot, userToScrap)
    load_all_followers(bot, num_followers, userToScrap)
    scrap_data_followers(bot, num_followers, userToScrap)

    time.sleep(2)

# This will check how much the user has followers

def get_followers_count(bot, userToScrap):
    print(f"[Info] - Gettings Number Of Followers for {userToScrap}...")
    followers_link = bot.find_element(By.XPATH, "//a[contains(@href, '/followers')]")
    span_element = followers_link.find_element(By.TAG_NAME, "span")
    num_followers = span_element.get_attribute("title")
    followers_link.click()
    print(f"[Success] - {userToScrap} has {num_followers} followers")
    return int(num_followers.replace(",", ""))    

# This will load all the followers (12 at a time)

def load_all_followers(bot, num_followers, userToScrap):
    print(f"[Info] - Loading {num_followers} followers for {userToScrap}...")
    n = 0
    time.sleep(5)
    while num_followers > n:
        bot.execute_script("document.querySelector('._aano').scrollTo(0, document.querySelector('._aano').scrollHeight);")
        n += 12
        time.sleep(2)
        estimated_time = time.strftime("%H:%M:%S", time.gmtime((num_followers - n) * 2))
        print(f"[Info] - Loading {n}/{num_followers}... ({estimated_time} left till finish)")
        if num_followers == n:
            break
    print(f"[Success] - Followers for {userToScrap} are loaded")

# This will save all the followers names in a txt file

def scrap_data_followers(bot, user_input, userToScrap):
    print(f"[Info] - Scraping followers for {userToScrap}...")

    users = set()
    while len(users) < user_input:
        followers = bot.find_elements(By.XPATH, "//a[contains(@href, '/') and @class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd']")

        for i in followers:
            estimated_time = time.strftime("%H:%M:%S", time.gmtime((user_input - len(users))))
            print(f"[Info] - Scraping {len(users)}/{user_input}... ({estimated_time} left till finish)")
            if i.get_attribute('href'):
                users.add(i.get_attribute('href').split("/")[3])
            else:
                continue

        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(1)

    users = list(users)[:user_input]  # Trim the user list to match the desired number of followers

    print(f"[Success] - Saving followers for {userToScrap}...")
    check_and_delete_file(f'output/{userToScrap}_followers.txt')
    with open(f'output/{userToScrap}_followers.txt', 'a') as file:
        file.write('\n'.join(users) + "\n")

# Scrap all the following

def scrape_following(bot, userToScrap):
    bot.get(f'https://www.instagram.com/{userToScrap}/')
    time.sleep(3.5)
    WebDriverWait(bot, 15).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]")))
    num_following = get_num_following(bot, userToScrap)
    load_all_following(bot, num_following, userToScrap)
    scrap_data_following(bot, num_following, userToScrap)

# Get all the following number

def get_num_following(bot, userToScrap):
    print(f"[Info] - Gettings Number Of Following for {userToScrap}...")
    following_link = bot.find_element(By.XPATH, "//a[contains(@href, '/following')]")
    span_element = following_link.find_element(By.TAG_NAME, "span")
    num_following = span_element.text
    following_link.click()
    print(f"[Success] - {userToScrap} has {num_following} following")
    return int(num_following.replace(",", ""))

# Load all the following (12 at a time)

def load_all_following(bot, num_following, userToScrap):
    print(f"[Info] - Loading {num_following} of following for {userToScrap}...")
    n = 0
    time.sleep(5)
    while num_following > n:
        bot.execute_script("document.querySelector('._aano').scrollTo(0, document.querySelector('._aano').scrollHeight);")
        n += 12
        time.sleep(2)
        estimated_time = time.strftime("%H:%M:%S", time.gmtime((num_following - n) * 2))
        print(f"[Info] - Loading {n}/{num_following}... ({estimated_time} left till finish)")
        if num_following == n:
            break
    
    print(f"[Success] - Following for {userToScrap} are loaded")

# Get all the following names and save them inside of .txt file

def scrap_data_following(bot, user_input, userToScrap):
    print(f"[Info] - Scraping followers for {userToScrap}...")

    users = set()
    while len(users) < user_input:
        followers = bot.find_elements(By.XPATH, "//a[contains(@href, '/') and @class='x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz notranslate _a6hd']")

        for i in followers:
            estimated_time = time.strftime("%H:%M:%S", time.gmtime((user_input - len(users))))
            print(f"[Info] - Scraping {len(users)}/{user_input}... ({estimated_time} left till finish)")
            if i.get_attribute('href'):
                users.add(i.get_attribute('href').split("/")[3])
            else:
                continue

        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(1)

    users = list(users)[:user_input]  # Trim the user list to match the desired number of followers

    print(f"[Success] - Saving followers for {userToScrap}...")
    check_and_delete_file(f'output/{userToScrap}_following.txt')
    with open(f'output/{userToScrap}_following.txt', 'a') as file:
        file.write('\n'.join(users) + "\n")

# This will check if the file .txt already exist or not and delete it if it exists
def check_and_delete_file(file_path):
  if os.path.exists(file_path):
    os.remove(file_path)

def check_not_following_back(following_file, followers_file):
    following_list = []
    followers_list = []

    with open("output/"+following_file, "r") as f:
        following_list = f.readlines()

    with open("output/"+followers_file, "r") as f:
        followers_list = f.readlines()
        
    following_list = [x.strip() for x in following_list]
    followers_list = [x.strip() for x in followers_list]

    not_following_back = []

    for name in following_list:
        if name not in followers_list:
            not_following_back.append(name)

    return not_following_back

def save_not_following_back(not_following_back,userToScrap):
    check_and_delete_file(f'output/not_following_back_{userToScrap}.txt')
    with open(f'output/not_following_back_{userToScrap}.txt', "a") as f:
        for name in not_following_back:
            f.write(name + "\n")

def convert_txt_to_html(txt_file_path, html_file_path):

  with open("output/"+txt_file_path, "r") as f:
    names = f.readlines()

  # Remove empty lines and trailing whitespace.
  names = [name.strip() for name in names if name]

  # Create the HTML header.
  html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Names List</title>
  <link href="https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css" rel="stylesheet">
</head>
<body>
  <link
	href="https://fonts.googleapis.com/css?family=Material+Icons|Material+Icons+Outlined|Material+Icons+Two+Tone|Material+Icons+Round|Material+Icons+Sharp"
	rel="stylesheet">
<div class="flex items-center justify-center min-h-screen bg-gray-900">
	<div class="col-span-12">
		<div class="overflow-auto lg:overflow-visible ">
			<table class="table text-gray-400 border-separate space-y-6 text-sm">
				<thead class="bg-gray-800 text-gray-500">
					<tr>
						<th class="p-3">User</th>
						<th class="p-3 text-left"></th>
						<th class="p-3 text-left"></th>
						<th class="p-3 text-left">Status</th>
						<th class="p-3 text-left">Action</th>
					</tr>
				</thead>
				<tbody>"""

  # Add each name to the HTML table.
  for name in names:
    if name:
        html += f"""
        <tr class="bg-gray-800">
            <td class="p-3">
                <div class="flex align-items-center">
                    <img class="rounded-full h-12 w-12  object-cover" src="https://api.dicebear.com/7.x/initials/svg?seed={name}" alt="unsplash image">
                    <div class="ml-3">
                        <div class="">{name}</div>
                        <div class="text-gray-500">{name}</div>
                    </div>
                </div>
            </td>
            <td class="p-3">
                
            </td>
            <td class="p-3 font-bold">
            </td>
            <td class="p-3">
                <span class="bg-red-400 text-gray-50 rounded-md px-2">Not Following</span>
            </td>
            <td class="p-3 ">
                <a href="https://www.instagram.com/{name}" target="_blank" class="text-gray-400 hover:text-gray-100  ml-2">
                    <i class="material-icons-round text-base">delete_outline</i>
                </a>
            </td>
        </tr>"""

  # Close the HTML table and body.
  html += """</tbody>
			</table>
		</div>
	</div>
</div>
<style>
	.table {
		border-spacing: 0 15px;
	}

	i {
		font-size: 1rem !important;
	}

	.table tr {
		border-radius: 20px;
	}

	tr td:nth-child(n+5),
	tr th:nth-child(n+5) {
		border-radius: 0 .625rem .625rem 0;
	}

	tr td:nth-child(1),
	tr th:nth-child(1) {
		border-radius: .625rem 0 0 .625rem;
	}
</style>
</body>
</html>"""

  with open("output/"+html_file_path, "w") as f:
    f.write(html)

# Script starts here
def main():
    try:
        username, password = prompt_credentials()
        userToScrap = input("Enter the Instagram username you want to scrape (make sure the instagram profile is public): ")

        driver = webdriver.Edge()

        login(driver, username, password)
        time.sleep(random.randint(1,10))

        scrape_followers(driver, userToScrap)
        time.sleep(random.randint(1,10))

        scrape_following(driver, userToScrap)

        driver.quit()
        print(f"[Success] - Scrapping was successfully done")
        
        print(f"[Info] - Checking for users that arent following {userToScrap} back")
        not_following_back = check_not_following_back(f"{userToScrap}_following.txt", f"{userToScrap}_followers.txt")
        save_not_following_back(not_following_back, userToScrap)
        print(f"[Success] - Saved all the users that arent following {userToScrap} back")
        convert_txt_to_html(f'not_following_back_{userToScrap}.txt', f'not_following_back_{userToScrap}.html')

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
