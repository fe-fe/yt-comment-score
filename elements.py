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