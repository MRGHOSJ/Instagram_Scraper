# Instagram Scraper Readme

This Python script is designed to scrape data from Instagram profiles, including followers, following, and identifying users who aren't following back. It utilizes the Selenium library for web automation to interact with Instagram's web interface.

## Prerequisites

Before using this script, make sure you have the following prerequisites installed:

* Python: You need Python 3.x installed on your system.
* Selenium: You can install Selenium using pip:

```bash
  pip install selenium
```
or 
```bash
pip install requirements.txt
```
* Webdriver: You will need a compatible WebDriver for your browser (e.g., Chrome WebDriver, Firefox WebDriver, etc.) installed. Make sure to add the WebDriver's location to your system's PATH or specify its path explicitly in the script.

## Usage

1. Run the script by executing the following command in your terminal:

```bash
python run.py
```

2. The script will prompt you for your Instagram username and password. Enter your credentials when prompted.

3. You will also need to enter the Instagram username of the profile you want to scrape. Ensure that the target Instagram profile is public.

4. The script will perform the following actions:

+ Login to Instagram using the provided credentials.
+ Scrape the followers of the target profile and save their usernames to a text file (output/username_followers.txt).
+ Scrape the accounts that the target profile is following and save their usernames to a text file (output/username_following.txt).
+ Identify users who are not following the target profile back and save their usernames to a text file (output/not_following_back_username.txt).

5. After the script has completed execution, it will generate an HTML file (output/not_following_back_username.html) that visually displays the list of users who aren't following back. You can open this HTML file in your web browser to view the results.

## Notes

+ The script uses the Selenium library for web automation, which simulates user interactions with the Instagram website. As a result, it may be subject to changes in the Instagram website structure. If the script stops working due to changes on Instagram, you may need to update the script accordingly.

+ Please be aware of Instagram's terms of service and policies regarding automation. Excessive or unauthorized scraping may result in the suspension of your Instagram account. Use this script responsibly and within Instagram's guidelines.

+ Instagram scraping is resource-intensive and may take a significant amount of time to complete, especially if the target profile has a large number of followers or accounts they are following.

## File Structure

+ `run.py`: The main Python script for scraping Instagram data.
+ `output/`: A directory where the script saves the output files.
+ `output/username_followers.txt`: Text file containing the usernames of the target profile's followers.
+ `output/username_following.txt`: Text file containing the usernames of accounts that the target profile is following.
+ `output/not_following_back_username.txt`: Text file containing the usernames of accounts that are not following the target profile back.
+ `output/not_following_back_username.html`: HTML file generated from the text file, displaying users who aren't following back in a visually organized format.

## Disclaimer

This script is provided for educational and informational purposes only. Use it responsibly and in compliance with Instagram's terms of service and policies. The author and OpenAI are not responsible for any misuse or consequences resulting from the use of this script.

## Acknowledgments

+ This script was created using the Selenium library, which is subject to its own licensing and terms. Please review the Selenium documentation and terms for more information.
+ Instagram is a registered trademark of Instagram, Inc. This script is not affiliated with or endorsed by Instagram, Inc.

## Author

[MRGHOSJ]
[GitHub Repository](https://github.com/MRGHOSJ)