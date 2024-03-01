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

def log(log_text):
    log_text = str(time.strftime("%Y.%m.%d %H:%M:%S")) + " ➾ " + log_text
    print(log_text)
    log_file = open("log.txt", "a", encoding="utf-8")
    log_file.write(log_text + "\n")
    log_file.close()

global_delay = 3
driver = webdriver.Chrome()
tweet_len_limit = 280
driver.get("https://twitter.com/login")
log("Program started")
log("Twitter opened")
try:
    WebDriverWait(driver, 90).until(EC.url_to_be("https://twitter.com/home"))
    log("Logged in!")
except:
    log(f"Failed. Try again")   

def run(command):  # follow the person only
    switch_dict = {
        'follow_only': follow_only,
        'follow_tweet': follow_tweet,
        'personal_tweet': personal_tweet,
    }

    switch_dict.get(command)(driver)
###
     ###cannot follow some test case 
###
def follow_only(driver):
    iloc_start = int(iloc_start_entry.get())
    iloc_end = int(iloc_end_entry.get())
    file = "input.xlsx"
    df = pd.read_excel(file)
    urls = df.iloc[iloc_start - 1 : iloc_end, 0].values.tolist()
    n = len(urls)
    log(f"Visiting {len(urls)} profiles.")

    for i in range(n):
        try:
            url = urls[i]
            driver.get(url)
            time.sleep(global_delay)
            try:
                # Perform actions on the profile here
                followed_button = ["/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div","/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div"]
                follow_element = find_element_in_list(driver,followed_button,3)
                assert follow_element.text == "Follow"
                follow_element.click()
                log(f"Followed profile: {url}")
                time.sleep(2)
            except:
                log(f"Followed profile: {url}")
        except:
            log(f"Failed to visit profile: {url}")
            time.sleep(global_delay)
            continue


def follow_tweet(driver):
    iloc_start = int(iloc_start_entry.get())
    iloc_end = int(iloc_end_entry.get())
    infos = getInfoOftweet(iloc_start,iloc_end)
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
            if (len(tweet) + len(tag_ceo) > tweet_len_limit):
                log_error_message(error_text, info['name'] + " too long (" + len(tweet) + len(tag_ceo) - tweet_len_limit + ") . Limit at 280 words (include tag, hastag, space, enter)")
                continue
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


def personal_tweet(driver):
    iloc_start = int(iloc_start_entry.get())
    iloc_end = int(iloc_end_entry.get())
    infos = getInfoOftweet(iloc_start,iloc_end)
    log(f"Tweeting")

    for i in range(len(infos)):
        try:
            # url = urls[i]
            info = infos[i]
            driver.get("https://twitter.com/compose/tweet")
            time.sleep(global_delay)
            # Perform actions on the profile here
            
            # add image
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
            ##content of tweet
            tweet = str(info['content'])
            this_hashtags = re.split(r'[,\s\n]+', info['hashtag'])
            this_hashtags = ['#' + tag if not tag.startswith('#') else tag for tag in this_hashtags]
            this_tags = re.split(r'[,\s\n]+', info['tag'])
            this_tags = ['@' + tag if not tag.startswith('@') else tag for tag in this_tags]
            # add tagname
            tweet = re.sub(r'&', lambda match: replace_and_increment(this_tags), tweet)
            # add hashtag
            tweet = re.sub(r'#', lambda match: replace_and_increment(this_hashtags), tweet)
            if (len(tweet) > tweet_len_limit):
                log_error_message(error_text, "post " + info['name'] + " too long (" + len(tweet) - tweet_len_limit + ") . Limit at 280 words (include tag, hastag, space, enter)")
                continue
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
            log(f"Tweeted : {tweet}")
            time.sleep(global_delay)
        except Exception as e:
            print(str(e))
            log(f"Failed to tweet")
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
def replace_and_increment(replacement_values):
    if replacement_values:
        return replacement_values.pop(0)
    else:
        return ''
    
def log_error_message(text_widget, message):
    current_content = text_widget.get("1.0", tk.END).strip()
    if message in current_content:
        line_number = current_content.count(message) + 1
        updated_line = f"{message} (x{line_number})"
        text_widget.replace(f"{line_number}.0", f"{line_number + 1}.0", updated_line + "\n")
    else:
        text_widget.insert(tk.END, message + "\n")
    # Scroll to the end to show the latest message
    text_widget.see(tk.END)

# Create tkinter window
window = tk.Tk()
window.title("Twitter Follow and Tweet Bot")
window.geometry("400x350")

# iloc start entry
iloc_start_label = tk.Label(window, text="Starting Row:")
iloc_start_label.pack()
iloc_start_entry = tk.Entry(
    window,
    width=10,
    justify="center",
)
iloc_start_entry.pack()

# iloc end entry
iloc_end_label = tk.Label(window, text="Ending Row:")
iloc_end_label.pack()
iloc_end_entry = tk.Entry(window, width=10, justify="center")
iloc_end_entry.pack(pady=10)

# follow button
follow_button = tk.Button(
    window, text="Follow the Twitter user Only", command=lambda: run('follow_only')
)
follow_button.pack(pady=10)

# follow and tweet button
follow_tweet_button = tk.Button(
    window, text="Follow and Tweet at the Twitter user", command=lambda: run('follow_tweet')
)
follow_tweet_button.pack(pady=10)

# personal tweet button
tweet_button = tk.Button(window, text="Personal Tweets", command=lambda: run('personal_tweet'))
tweet_button.pack(pady=10)

error_text = tk.Text(window, height=10, width=40, wrap=tk.WORD, fg="red")
error_text.pack(pady=10)

# Create a Scrollbar and connect it to the Text widget
scrollbar = tk.Scrollbar(window, command=error_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
error_text.config(yscrollcommand=scrollbar.set)

window.mainloop()
