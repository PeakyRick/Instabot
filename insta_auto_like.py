# need to explicitly wait till the page loads
# Next: Deal with "Page not available" for wrong tags

""" Instagram Liking Bot
This instagram bot is able to login to an account with provided credentials
Then go to the desired hashtags and click on the like buttons of a number of photos 
under that hashtag as well as under the explore page.
"""

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import random

# Import credentials that are saved as dictionaries from file "insta_credentials"
from insta_credentials import user1_cred as user1
from insta_credentials import user2_cred as user2

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
firefox_service = Service("/Users/eric8/Downloads/geckodriver.exe")

class InstagramLikes:
    def __init__(self, username, password):
        """Initialize the bot and credentials"""
        self.count = 0
        self.username = username
        self.pw = password
        self.bot = webdriver.Firefox(service=firefox_service, options=options)

    def login(self):
        self.bot.get('https://instagram.com')
        time.sleep(2)
        self.bot.find_element(By.NAME,'username').send_keys(self.username)
        self.bot.find_element(By.NAME,'password').send_keys(self.pw + Keys.RETURN)
        time.sleep(10)

    def search_hashtag(self, hashtag):
        self.bot.get('https://www.instagram.com/explore/tags/' + hashtag)
        time.sleep(6)

    def search_explore(self):
        print("Searching through Explore")
        self.bot.get('https://www.instagram.com/explore')
        time.sleep(3)
        self.bot.execute_script("window.scrollTo(0, 2160)")
        time.sleep(2)

    def like_photos(self, amount = np.nan):
        images = self.bot.find_elements(By.CLASS_NAME, '_aagw')
        while len(images) == 0:
            time.sleep(2)
            images = self.bot.find_elements(By.CLASS_NAME, '_aagw')
        images[0].click()
        time.sleep(2)

        if np.isnan(amount):
            # In case an amount is specified
            amount = len(images) - 1
        for i in range(amount):
            like_bttn = self.bot.find_elements(By.CLASS_NAME, "_aamw")
            if len(like_bttn) != 0:
                like_bttn[0].click()
                if self._photo_not_liked():
                    like_bttn[0].click()
                else:
                    self.count += 1
            time.sleep(random.randint(2,3))
            next_bttn = self.bot.find_elements(By.CLASS_NAME, "_aaqg")
            if len(next_bttn) == 0: # If there isn't a next button
                break
            else:
                next_bttn[0].click()
            time.sleep(random.randint(2,3))

    def _photo_not_liked(self):
        """ Check if the post is not yet liked"""
        # hrt_elements = self.bot.find_element(By.CSS_SELECTOR, ".x1ykxiw6 svg")
        hrt_elements = self.bot.find_element(By.CSS_SELECTOR, ".x1ykxiw6 svg")
        if hrt_elements:
            fill_color = hrt_elements.get_attribute("fill")
            if fill_color == "rgb(245, 245, 245)":
                return True  # Post is unliked
        return False  # Post is liked
 
tags1 = ["takemagazine","agameoftones","winter","portraitphotography","portrait","portraitmood","portraitpage",
            "explorepage","autumn","fall","cinematic","streetphotography","35mm","love","etczine","nature",
            "photography","architecture","shotoniphone","travelphotography","urban","toronto","ottawa","travel",
            "film","cinematicphotography","ontario","mcmaster","nikon",
            "like4like","likeforlike","follow4follow"]
            
tags2 = ["cuteboys","asianboys","handsomeman","bollywoodboys","instaboys","follow4follow",
            "followforfollow","like4like","likeforlike","likeforlikes","recentforrecent",
            "selfie","nice","instaselfie","asianguy","chineseboy","under1k","chinese",
            "philippines","indian","indianboy","gym","gymselfie","malemodel","random", "menfashion",
            "me","gamerboy","likeme","nerd","eboy","candid","tattooboys","koreanboys","followers","asiangirls"]

user1["TAGS"] = tags1
user2["TAGS"] = tags2

def run_bot(user):
    insta = InstagramLikes(user["USERNAME"], user["PASSWORD"])
    insta.login()
    for tag in user["TAGS"]:
        print(f"In {tag}. Liked {insta.count} posts so far.\n")
        insta.search_hashtag(tag)
        insta.like_photos()

    insta.search_explore()
    insta.like_photos()

    print(f"Liked {insta.count} posts in total.")
    return

# insta = InstagramLikes(user1["USERNAME"], user1["PASSWORD"])
# insta.login()
# insta.like_feed()

for cred in [user1,user2]:
    run_bot(cred)
