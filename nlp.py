from dotenv import load_dotenv
from google import genai
import os
from nltk.sentiment import SentimentIntensityAnalyzer
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

client = genai.Client(api_key=GEMINIKEY)


def translate(sample: list) -> list:
    # ";;;;;;" eh o delimitador dos comentarios
    prompt = ";;;;;;".join(sample)
    prompt = """Traduza para ingles o seguinte prompt e mantenha os comentarios 
    separados por ';;;;;;'. Responda apenas o texto traduzido, nada mais:"""+prompt

    # traduz a amostra de comentarios para ingles utilizando a Gemini AI.
    # Textos em ingles sao processados com mais precisao pelo modulo de sentimentos.
    traduzido = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
    )

    sample_ingles = traduzido.text.split(";;;;;;")
    return sample_ingles


def get_polarity(sample: list) -> list:
    sample_ingles = translate(sample)
    positive = 0
    polarity = []
    for s in sample_ingles:
        p = sia.polarity_scores(s) # processa os sentimentos do texto
        polarity.append(p["compound"])
        if p["compound"] > 0:
            positive += 1

    media = (fmean(polarity)+1)*50 # faz a media das polaridades e converte em porcentagem, variando entre 0 e 100%
    return polarity, media, positive


def get_common_words(sample: list) -> list:
    
    sample = ".".join(sample) # une a sample em uma string separando os indices por pontos
    tokens = word_tokenize(sample.lower()) # extrai os tokens da string

    # filtra os tokens por palavras importantes
    filtrada = []
    for t in tokens:
        if t not in swp:
            filtrada.append(t)
    
    freq = FreqDist(filtrada) # extrai as palavras mais comuns
    return freq.most_common(5) # retorna as 5 palavras mais frequentes