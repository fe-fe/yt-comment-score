import flet as ft
from scraper import get_comment_sample, get_video_details
from nlp import get_common_words, get_polarity
from nlp import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colors import *
from elements import *


options = Options()
options.add_argument("--headless=new")
options.add_argument("--mute-audio")

browser = webdriver.Chrome(options)
mainContainer = white_container()
mainContainer.padding = 20

content_row = ft.Row(
    alignment=ft.MainAxisAlignment.CENTER,
    expand=1,
    controls=[mainContainer]
)

header = ft.Text(
    "waiting for input...",  
    text_align=ft.TextAlign.CENTER, 
)

mainContent = ft.Column(
        controls=[header, ft.Divider(height=1, color=color1)],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

mainContainer.content = mainContent

link_input = text_field()


def handleSearchBt(e):
    header.value = "requesting url..."
    link = link_input.value
    e.page.update()
    details = get_video_details(link)
    mainContent.controls = mainContent.controls[:2] # remove o conteudo anterior
    mainContent.controls.append(create_content_box(details[0], details[1])) # cria o conteudo do video
    header.value = "getting comment sample..."
    e.page.update()
    sample = get_comment_sample(link, 20, browser, False)
    header.value = "processing data..."
    e.page.update()
    polarity = get_polarity(sample)
    for p in polarity:
        append_avg_bar(p[0], f"{p[1]}: {p[0]:.0f}%", mainContent)
    header.value = "done!"
    e.page.update()
    

def main(page: ft.Page):

    page.bgcolor = color1
    page.padding = ft.padding.only(bottom=50)
    page.theme_mode = ft.ThemeMode.LIGHT

    vw = page.width / 100
    vh = page.height / 100

    global mainContainer
    mainContainer.width = vw*40

    global link_input
    link_input.value = ""
    link_input.label = "video link"

    global header
    header.style = ft.TextStyle(color=color8, size=3*vh)

    global mainContent

    search_bar = ft.Container(
        bgcolor=white1,
        padding = ft.padding.only(left=7, right=7, top=15, bottom=15),
        content = (
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=color8),
                    link_input,
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=color8, on_click=handleSearchBt),            
                ]
            )
        )
    )

    main_column = ft.Column(
        spacing=20,
        expand=True,
        alignment=ft.alignment.center,
        controls=[
            search_bar,
            content_row
        ]
    )
    
    page.add(main_column)

ft.app(main)
