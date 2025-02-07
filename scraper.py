from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

GEMINIKEY = os.getenv("GEMINIKEY")
print(GEMINIKEY)

client = genai.Client(api_key=GEMINIKEY)


from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

browser = webdriver.Chrome()

link = "https://www.youtube.com/watch?v=L1czIgvo3-I"

#https://www.selenium.dev/pt-br/documentation/webdriver/actions_api/wheel/

def get_comment_sample(link: str, qtd: int, browser: webdriver.Chrome, exceed=True) -> list:
    sample = []
    browser.get(link)
    sleep(1)
    while len(sample) < qtd:
        try:
            ActionChains(browser)\
                .scroll_by_amount(0, 200)\
                .perform()

            comments = []
            for comment in browser.find_elements(By.ID, "content-text"):
                comments.append(comment.find_element(By.TAG_NAME, "span").text)

            sample.extend(list(set(comments) - set(sample))) # garante que nao vai se repetir

        except ElementNotInteractableException:
            continue

    browser.close()
    
    if not exceed:
        sample = sample[0:qtd]
    return sample


sample = get_comment_sample(link, 20, browser, False)

prompt = ";;;;;;".join(sample)

prompt = "Traduza para ingles o seguinte prompt e mantenha os comentarios separados por ';;;;;;':"+prompt

traduzido = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

sample_ingles = traduzido.text.split(";;;;;;")


i = 0
for s in sample:
    print(s)
    print("traduzido: "+sample_ingles[i])
    print(TextBlob(sample_ingles[i], analyzer=NaiveBayesAnalyzer()).sentiment)
    print("==========")
    i+=1
