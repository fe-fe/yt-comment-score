import flet as ft
from scraper import get_comment_sample
from nlp import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colors import *
from elements import *


browser = None


def main(page: ft.Page):

    global browser

    page.bgcolor = color1
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    vw = page.width / 100
    vh = page.height / 100

    link_input = text_field()
    link_input.value = ""
    link_input.label = "video link"

    search_bar = ft.Container(
        bgcolor = white1,
        padding = ft.padding.only(left=7, right=7, top=17, bottom=7),
        content = (
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(icon=ft.Icons.SETTINGS, icon_color=color8),
                    link_input,
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=color8),
                            
                ]
            )
        )
    )

    content = white_container()
    content.width = vw*40
    content.content = ft.Column(
        controls=[
            ft.Text("waiting for input...", expand=1)
        ]
    )

    main_column = ft.Column(
        spacing=20,
        alignment=ft.alignment.center,
        controls=[
            search_bar,
            content
        ]
    )
    

    page.add(main_column)

ft.app(main)
