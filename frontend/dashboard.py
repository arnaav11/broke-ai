"""BROKE-AI Dashboard — Main Dashboard Content View"""

import flet as ft
from components import (
    MOCK_DATA, create_profile_card, create_stat_card,
    create_daily_limit_card, create_saving_plans_section,
    create_cashflow_section, create_transactions_table,
    create_statistic_section, create_recent_activity,
)


def get_dashboard_view(page: ft.Page, colors: dict) -> ft.Column:
    """Build the 3-column dashboard grid and return it as a scrollable Column."""

    # Left Column
    left_column = ft.Column(
        controls=[
            create_profile_card(MOCK_DATA['user_name'], MOCK_DATA['balance'], MOCK_DATA['exp_date'], MOCK_DATA['cvv'], colors),
            create_daily_limit_card(MOCK_DATA['daily_limit']['spent'], MOCK_DATA['daily_limit']['limit'], MOCK_DATA['daily_limit']['pct'], colors),
            create_saving_plans_section(MOCK_DATA['saving_plans'], colors),
        ],
        width=280,
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
    )

    # Center Column
    center_column = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    create_stat_card('Total Income', MOCK_DATA['income'], ft.Icons.TRENDING_UP, colors),
                    create_stat_card('Total Expense', MOCK_DATA['expense'], ft.Icons.TRENDING_DOWN, colors),
                    create_stat_card('Total Savings', MOCK_DATA['savings'], ft.Icons.ACCOUNT_BALANCE_WALLET, colors),
                ],
                spacing=14,
            ),
            create_cashflow_section(MOCK_DATA['cashflow_monthly'], MOCK_DATA['cashflow_total'], colors),
            create_transactions_table(MOCK_DATA['transactions'], colors),
        ],
        expand=True,
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
    )

    # Right Column
    right_column = ft.Column(
        controls=[
            create_statistic_section(MOCK_DATA['expense_categories'], MOCK_DATA['expense_total'], colors),
            create_recent_activity(MOCK_DATA['recent_activity'], colors),
        ],
        width=280,
        spacing=14,
        scroll=ft.ScrollMode.AUTO,
    )

    # Top-level Row wrapping the 3 columns
    dashboard_row = ft.Row(
        controls=[left_column, center_column, right_column],
        spacing=14,
        expand=True,
    )

    # Wrap in a scrollable Column
    return ft.Column(
        controls=[
            ft.Container(
                padding=20,
                content=dashboard_row,
            ),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )