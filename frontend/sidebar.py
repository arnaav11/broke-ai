"""BROKE-AI Dashboard — Sidebar Navigation"""

import flet as ft


def create_sidebar(on_tab_change, active_tab: str, colors: dict) -> ft.Container:
    nav_items_data = [
        ("Dashboard", ft.Icons.SPACE_DASHBOARD_OUTLINED),
        ("Transactions", ft.Icons.SWAP_HORIZ_OUTLINED),
        ("Invoices", ft.Icons.RECEIPT_OUTLINED),
        ("Saving Plans", ft.Icons.SAVINGS_OUTLINED),
        ("Inbox", ft.Icons.INBOX_OUTLINED),
        ("Promos", ft.Icons.LOCAL_OFFER_OUTLINED),
        ("Insights", ft.Icons.INSIGHTS_OUTLINED),
        ("Settings", ft.Icons.SETTINGS_OUTLINED),
    ]

    nav_controls = []
    for text, icon in nav_items_data:
        is_active = text == active_tab
        item = ft.Container(
            data=text,
            content=ft.Row(
                [
                    ft.Icon(
                        icon,
                        size=20,
                        color=colors['text_primary'] if is_active else colors['text_secondary'],
                    ),
                    ft.Text(
                        text,
                        size=14,
                        color=colors['text_primary'] if is_active else colors['text_secondary'],
                        weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                    ),
                ]
            ),
            padding=ft.Padding(left=15, top=12, right=15, bottom=12),
            border_radius=10,
            bgcolor=colors['active_tab_bg'] if is_active else ft.Colors.TRANSPARENT,
            on_click=lambda e, t=text: on_tab_change(t),
        )
        nav_controls.append(item)

    logo_row = ft.Row(
        [
            ft.Icon(ft.Icons.GRAIN, color=colors['primary_accent'], size=30),
            ft.Text(
                'BROKE-AI',
                size=20,
                weight=ft.FontWeight.W_900,
                color=colors['text_primary'],
            ),
        ]
    )

    divider = ft.Container(height=30)

    nav_column = ft.Column(
        controls=nav_controls,
        spacing=5,
    )

    return ft.Container(
        width=220,
        bgcolor=colors['sidebar_bg'],
        padding=20,
        border=ft.Border(right=ft.BorderSide(1, colors['border'])),
        content=ft.Column(
            [
                logo_row,
                divider,
                nav_column,
            ]
        ),
    )
