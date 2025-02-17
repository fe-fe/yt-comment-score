import flet as ft
from scraper import get_comment_sample
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
content = white_container()

link_input = text_field()


header = ft.Text(
    "waiting for input...",  
    text_align=ft.TextAlign.CENTER, 
)

avg = ft.Text()

img = ft.Image(src="https://img.youtube.com/vi/NRLP2_ZyiyE/maxresdefault.jpg", width=400, border_radius=15)

def handleSearchBt(e):
    global header
    header.value = "please wait..."
    e.page.update()
    link = link_input.value
    sample = get_comment_sample(link, 5, browser, False)
    header.value = sample[1]
    print(sample[2])
    img.src = sample[2]
    e.page.update()
    sample_ingles = translate(sample[0])
    polarity = get_polarity(sample_ingles)
    avg.value = str(polarity[1])
    common_words = get_common_words(sample[0])
    e.page.update()
    
    

def main(page: ft.Page):

    page.bgcolor = color1
    page.padding = ft.padding.only(bottom=50)
    page.theme_mode = ft.ThemeMode.LIGHT

    vw = page.width / 100
    vh = page.height / 100

    global link_input
    link_input.value = ""
    link_input.label = "video link"

    global header

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

    header.style = ft.TextStyle(color=color8, size=3*vh)

    content.width = vw*40
    content.content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            header,
            ft.Divider(height=1, color=color1),
            img,
            avg
        ],
        expand=True
    )

    main_column = ft.Column(
        spacing=20,
        expand=True,
        alignment=ft.alignment.center,
        controls=[
            search_bar,
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[content],
                expand=1
            ),
            
        ]
    )
    

    page.add(main_column)

ft.app(main)
