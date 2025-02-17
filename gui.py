import flet as ft
from scraper import get_comment_sample
from nlp import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

browser = None

def main(page: ft.Page):

    global browser

    page.theme = ft.Theme(color_scheme_seed=ft.Colors.PINK)
    page.theme_mode = ft.ThemeMode.LIGHT

    link_input = ft.TextField(
        value="",
        label="video link",
        prefix_icon=ft.Icons.ONDEMAND_VIDEO
    )

    search_bar = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Row(
                controls=[
                    link_input,
                    ft.IconButton(
                        icon=ft.Icons.SEARCH
                    )
                ]
            ),
            ft.IconButton(icon=ft.Icons.SETTINGS)         
        ]
    )

    page.add(search_bar)

browser = webdriver.Chrome()
ft.app(main)
