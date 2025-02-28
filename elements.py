import flet as ft
from colors import *


def text_field():
    return ft.TextField(
        border_radius=6,
        bgcolor=black1,
        label_style=ft.TextStyle(color=color6),
        text_style=ft.TextStyle(color=color8, weight=ft.FontWeight.W_200),
        border_width=1,
        border_color=color4,
    )


def white_container():
    return ft.Container(
        padding=10,
        bgcolor=white1,
        border_radius=8,
        border=ft.border.all(1, color4),
    )


def create_content_box(title, img):
    # sobrescreve o conteudo do container pelo novo content box (caixa onde estara o video)
    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        controls=[
            ft.Image(src=img, border_radius=15),
            ft.Text(value=title)
        ]
    )


def append_avg_bar(avg, title, contentBox: ft.Column):

    avgBar = ft.LinearGradient(
        begin=ft.alignment.center_left,
        end=ft.alignment.center_right,
        colors=[color4, color4, color1, color1],
        stops=[0, avg, avg, 1]
    )
    
    avgContainer = ft.Container(
        gradient=avgBar,
        padding=10,
        border_radius=8,
        border=ft.border.all(1, color4),
        content=ft.Text(value=title, expand_loose=1),
        expand=True
    )

    contentBox.controls.append(ft.Row(controls=[avgContainer]))