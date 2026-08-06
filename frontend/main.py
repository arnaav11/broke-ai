"""
BROKE-AI Tracker — Application Entry Point

Single entry point that assembles the sidebar, header, theme toggle,
and tab-routed content area. Run with: python main.py
"""

import flet as ft
from components import get_theme_colors, MOCK_DATA
from sidebar import create_sidebar
from dashboard import get_dashboard_view


def main(page: ft.Page):
    # ── Page Configuration ──────────────────────────────────
    page.title = "BROKE-AI Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#F4F7F6"
    page.fonts = {"Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700;900&display=swap"}
    page.theme = ft.Theme(font_family="Roboto")

    # ── State ───────────────────────────────────────────────
    is_dark = False
    active_tab = "Dashboard"
    colors = get_theme_colors(is_dark)

    # ── Content Area (swapped on tab change) ────────────────
    content_area = ft.Container(expand=True)
    header_title = ft.Text(
        active_tab, size=28, weight=ft.FontWeight.BOLD,
        color=colors["text_primary"],
    )

    # ── Placeholder views for non-Dashboard tabs ────────────
    def _placeholder_view(name: str) -> ft.Container:
        c = get_theme_colors(is_dark)
        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            padding=40,
            content=ft.Column([
                ft.Icon(ft.Icons.CONSTRUCTION, size=48, color=c["text_secondary"]),
                ft.Container(height=12),
                ft.Text(
                    f"{name} — Coming Soon",
                    size=22, weight=ft.FontWeight.W_600, color=c["text_primary"],
                ),
                ft.Text(
                    "This section is under construction.",
                    size=14, color=c["text_secondary"],
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
        )

    def _load_content():
        """Load the content for the currently active tab."""
        c = get_theme_colors(is_dark)
        if active_tab == "Dashboard":
            return get_dashboard_view(page, c)
        else:
            return _placeholder_view(active_tab)

    content_area.content = _load_content()

    # ── Tab Change Handler ──────────────────────────────────
    def on_tab_change(tab_name: str):
        nonlocal active_tab
        active_tab = tab_name
        _rebuild_layout()

    # ── Theme Toggle Handler ────────────────────────────────
    def on_theme_toggle(e):
        nonlocal is_dark
        is_dark = not is_dark
        _rebuild_layout()

    # ── Full Rebuild (called on tab change or theme toggle) ─
    def _rebuild_layout():
        nonlocal colors
        colors = get_theme_colors(is_dark)

        # Update page-level properties
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        page.bgcolor = colors["page_bg"]

        # Rebuild header
        header_title.value = active_tab
        header_title.color = colors["text_primary"]
        search_field.hint_text = "Search placeholder"
        search_field.bgcolor = colors["card_bg"]
        search_field.color = colors["text_primary"]
        search_field.hint_style = ft.TextStyle(color=colors["text_secondary"])
        theme_btn.icon = ft.Icons.DARK_MODE if not is_dark else ft.Icons.LIGHT_MODE
        theme_btn.icon_color = colors["text_secondary"]
        msg_btn.icon_color = colors["text_secondary"]
        notif_btn.icon_color = colors["text_secondary"]
        profile_name.color = colors["text_primary"]
        header_container.bgcolor = colors["page_bg"]

        # Rebuild sidebar
        new_sidebar = create_sidebar(on_tab_change, active_tab, colors)

        # Rebuild content
        content_area.content = _load_content()

        # Reassemble
        main_row.controls = [
            new_sidebar,
            ft.Column([
                header_container,
                content_area,
            ], expand=True, spacing=0),
        ]
        page.update()

    # ── Header Widgets ──────────────────────────────────────
    search_field = ft.TextField(
        hint_text="Search placeholder",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=20,
        height=40,
        text_size=14,
        content_padding=ft.Padding(left=15, top=0, bottom=0, right=15),
        bgcolor=colors["card_bg"],
        border_color=ft.Colors.TRANSPARENT,
        color=colors["text_primary"],
        hint_style=ft.TextStyle(color=colors["text_secondary"]),
    )

    theme_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        icon_color=colors["text_secondary"],
        tooltip="Toggle theme",
        on_click=on_theme_toggle,
    )
    msg_btn = ft.IconButton(
        icon=ft.Icons.MESSAGE_OUTLINED,
        icon_color=colors["text_secondary"],
    )
    notif_btn = ft.IconButton(
        icon=ft.Icons.NOTIFICATIONS_OUTLINED,
        icon_color=colors["text_secondary"],
    )
    profile_name = ft.Text(
        MOCK_DATA["user_name"],
        weight=ft.FontWeight.BOLD,
        color=colors["text_primary"],
    )

    header_container = ft.Container(
        bgcolor=colors["page_bg"],
        padding=ft.Padding(left=30, right=30, top=20, bottom=10),
        content=ft.Row([
            header_title,
            ft.Row([
                ft.Container(content=search_field, width=250),
                theme_btn,
                msg_btn,
                notif_btn,
                ft.Row([
                    profile_name,
                    ft.CircleAvatar(
                        content=ft.Icon(ft.Icons.PERSON, color=colors["primary_accent"]),
                        bgcolor=colors["active_tab_bg"],
                        radius=18,
                    ),
                ], spacing=10),
            ], spacing=12),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
    )

    # ── Sidebar ─────────────────────────────────────────────
    sidebar = create_sidebar(on_tab_change, active_tab, colors)

    # ── Assemble Layout ─────────────────────────────────────
    main_row = ft.Row([
        sidebar,
        ft.Column([
            header_container,
            content_area,
        ], expand=True, spacing=0),
    ], expand=True, spacing=0)

    page.add(main_row)


# Run the app natively
if __name__ == "__main__":
    ft.app(target=main)