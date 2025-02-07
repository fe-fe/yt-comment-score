from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from google import genai
import os
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from statistics import fmean
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import string

swp = stopwords.words("portuguese")
swp.extend(string.punctuation)

sia = SentimentIntensityAnalyzer()

load_dotenv()

GEMINIKEY = os.getenv("GEMINIKEY")
print(GEMINIKEY)

client = genai.Client(api_key=GEMINIKEY)


browser = webdriver.Chrome()

link = "https://www.youtube.com/watch?v=W9AO7g2Cgdc"

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

prompt = "Traduza para ingles o seguinte prompt e mantenha os comentarios separados por ';;;;;;'. Responda apenas o texto traduzido, nada mais:"+prompt

traduzido = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

sample_ingles = traduzido.text.split(";;;;;;")


i = 0
sentiments = []
for s in sample:
    if len(s) > 100:
        print(s[0:100]+"...")
    else:
        print(s) 
    
    sentiment = sia.polarity_scores(sample_ingles[i])
    sentiments.append(sentiment["compound"])
    print(f"Result: {round((sentiment["compound"]+1)*50, 2)}%")
    print("-"*50)
    i+=1


print(f"media final: {(fmean(sentiments)+1)*50}%")
print("-"*50)



sample = ".".join(sample)
tokens = word_tokenize(sample.lower())

filtrada = []
for t in tokens:
    if t not in swp:
        filtrada.append(t)

freq = FreqDist(filtrada)

print(freq.most_common(30))