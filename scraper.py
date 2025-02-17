from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#https://www.selenium.dev/pt-br/documentation/webdriver/actions_api/wheel/

def get_comment_sample(link: str, qtd: int, browser: webdriver.Chrome, exceed=True) -> list:
    sample = []
    browser.get(link)
    sleep(1) # espera o conteudo da pagina ser carregado

    """
    enquanto a quantidade desejada de comentarios para amostra nao for alcancada,
    scrollar a pagina para baixo e procurar por mais comentarios

    o elemento do comentario pode ser identificado pelo id do seu elemento pai 'content-text'

    Os comentarios podem nao estar disponiveis de primeira mao, 
    portanto tratamos a execao ElementNotInteractableException com continue
    exceed diz se a quantidade de comentarios da sample pode ser excedida ou nao
    Ex: caso  qtd = 25 exceed=true, a funcao pode retornar 20 ou mais comentarios, geralmente variando de 1 a 10
    """

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

