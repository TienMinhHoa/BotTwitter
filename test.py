import pandas as pd
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import filedialog
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox
import re
def getInfoOftweet(start,end):
    file = "input.xlsx"
    df = pd.read_excel(file)
    urls = df.iloc[start - 1 : end, 0].values.tolist()
    tweetNames = df.iloc[start-1:end,1].values.tolist()
    sheet_2 = 'tweet'
    df2 = pd.read_excel(file, sheet_name=sheet_2)
    tags = df.iloc[start - 1 : end, 2].apply(str).values.tolist()
    hashtags = df.iloc[start - 1 : end, 3].apply(str).values.tolist()
    info = []
    for i in tweetNames:
        tmp_df = df2[df2["NAME"] == i]
        info_dict = {"name":i,"content":tmp_df['TWEET'].values[0],"image":tmp_df["IMAGE"].values[0]}
        info.append(info_dict)

    for i in range(len(info)):
        info[i]['url'] = urls[i]
        info[i]['tag'] = tags[i]
        info[i]['hashtag'] = hashtags[i]
    return info

def follow_tweet(driver):
    infos = getInfoOftweet(1,3)
    for i in range(len(infos)):
        try:
            info = infos[i]
            url = info['url']
            driver.get(url)
            time.sleep(3)
            try:
                # Perform actions on the profile here
                followed_button = ["/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div","/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div"]
                follow_element = find_element_in_list(driver,followed_button,3)
                assert follow_element.text == "Follow"
                follow_element.click()
                print(f"Followed profile: {url}")
                time.sleep(2)
            except:
                print(f"Followed profile: {url}")

            driver.find_element(
                "xpath",
                "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a/div",
            ).click()
            time.sleep(2)
            
            # Add picture to twitter post
            try:
                    xpat1 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                    xpat2 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[3]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                    xpat3 = "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[4]/div[1]/div/div/div/div[2]/div[2]/div/div/nav/div/div[2]/div/div[1]/div/input"
                    input = find_element_in_list(driver, [xpat1, xpat2, xpat3], 2)
                    input.send_keys(info['image'])
            except Exception as e:
                    print(str(e))
                    print('can not find image ' + info['image'])
            time.sleep(3)

            # Add content to twitter post
            tweet = str(info['content'])
            this_hashtags = re.split(r'[,\s\n]+', info['hashtag'])
            this_hashtags = ['#' + tag if not tag.startswith('#') else tag for tag in this_hashtags]
            this_tags = re.split(r'[,\s\n]+', info['tag'])
            this_tags = ['@' + tag if not tag.startswith('@') else tag for tag in this_tags]
            # add tagname
            tweet = re.sub(r'&', lambda match: replace_and_increment(this_tags), tweet)
            # add hashtag
            tweet = re.sub(r'#', lambda match: replace_and_increment(this_hashtags), tweet)
            tag_ceo = url.split('/')[-1]
            # if (len(tweet) + len(tag_ceo) > 200):
            #     # log_error_message(error_text, ceo_tweets_names[i] + " too long (" + len(tweet) + len(tag_ceo) - tweet_len_limit + ") . Limit at 280 words (include tag, hastag, space, enter)")
            #     continue
            # driver.find_element(
            #         "xpath",
            #         "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div/div"
            #     ).send_keys(tweet)
            element = driver.find_element("class name","public-DraftEditor-content")
            element.send_keys(tweet)
            time.sleep(2)
            try:
                dropdown = driver.find_element(
                    "xpath",
                    "/html/body/div[1]/div/div/div[1]/div[3]",
                )
                driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", dropdown)
            except:
                print('dropdown hidden')
            time.sleep(2)

            driver.find_element(
                "xpath",
                "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/div[4]",
            ).click()
            print(f"Tweeted at profile: {url} : {tweet}")
            time.sleep(global_delay)
        except:
            print(f"Failed to visit profile: {url}")
            time.sleep(global_delay)
            continue
def find_element_in_list(driver, xpath_list, wait=3):
    for xpath in xpath_list:
        try:
            element = WebDriverWait(driver, wait).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            print(f"Element not found with XPath: {xpath}")
    print("No element found in the provided XPath list.")
    return None
def replace_and_increment(replacement_values):
    if replacement_values:
        return replacement_values.pop(0)
    else:
        return ''


global_delay = 3
driver = webdriver.Chrome()
tweet_len_limit = 280
driver.get("https://twitter.com/login")
try:
    WebDriverWait(driver, 90).until(EC.url_to_be("https://twitter.com/home"))
    print("Logged in!")
except:
    print(f"Failed. Try again")   
follow_tweet(driver)
window = tk.Tk()
window.title("Twitter Follow and Tweet Bot")
window.geometry("400x350")
window.mainloop()

