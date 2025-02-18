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

posbar = ft.LinearGradient(
    begin=ft.alignment.center_left,
    end=ft.alignment.center_right,
    colors=[color4, color4, color1, color1],
    stops=[0, 0.0, 0.0, 1]
)

avg = ft.Text(expand_loose=1)

img = ft.Image(src="https://img.youtube.com/vi/HMYO8fqyoXk/mqdefault.jpg", border_radius=15)


def updateVideoInfo(title, url):
    header.value = title
    img.src = url
    

def updatePosBar(polarity):
    avg.value = f"{polarity[1]}% avg polarity | {polarity[2]}/{len(polarity[0])} positive comments" 
    posbar.stops[1] = polarity[2]/len(polarity[0])
    posbar.stops[2] = polarity[2]/len(polarity[0])

def handleSearchBt(e):
    header.value = "please wait..."
    e.page.update()
    link = link_input.value
    sample = get_comment_sample(link, 50, browser, updateVideoInfo, e, False)
    polarity = get_polarity(sample)
    updatePosBar(polarity)
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
            ft.Container(
                gradient=posbar,
                padding=10,
                border_radius=8,
                border=ft.border.all(1, color4),
                content=avg,
            )
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
