"""
BROKE-AI Dashboard — Reusable Components & Chart Generators

Provides theme colors, mock data, widget factories for cards/tables/feeds,
and matplotlib-based chart renderers (cashflow bar chart, expense donut chart).
"""

import flet as ft
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for rendering to buffer
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import io
import base64


# ──────────────────────────────────────────────────────────────
#  THEME SYSTEM
# ──────────────────────────────────────────────────────────────

def get_theme_colors(is_dark: bool) -> dict:
    """Return the full color palette for the current theme mode."""
    if is_dark:
        return {
            "primary_accent":  "#4ADE80",
            "page_bg":         "#0F1714",
            "sidebar_bg":      "#1A2420",
            "card_bg":         "#1E2D27",
            "active_tab_bg":   "#2A3E33",
            "text_primary":    "#E8F0EC",
            "text_secondary":  "#8A9B92",
            "border":          "#2A3E33",
            "success":         "#4ADE80",
            "warning":         "#FBBF24",
            "error":           "#F87171",
            "chart_bg":        "#1E2D27",
            "chart_grid":      "#2A3E33",
            "chart_text":      "#8A9B92",
            "chart_income":    "#4ADE80",
            "chart_expense":   "#2A3E33",
            "profile_gradient_start": "#1E4D33",
            "profile_gradient_end":   "#0F1714",
            "hover_bg":        "#243D30",
        }
    else:
        return {
            "primary_accent":  "#37C372",
            "page_bg":         "#F4F7F6",
            "sidebar_bg":      "#FFFFFF",
            "card_bg":         "#FFFFFF",
            "active_tab_bg":   "#E5F4E9",
            "text_primary":    "#2D3B34",
            "text_secondary":  "#89968F",
            "border":          "#E0E5E2",
            "success":         "#37C372",
            "warning":         "#F5A623",
            "error":           "#E74C3C",
            "chart_bg":        "#FFFFFF",
            "chart_grid":      "#E0E5E2",
            "chart_text":      "#89968F",
            "chart_income":    "#37C372",
            "chart_expense":   "#2D3B34",
            "profile_gradient_start": "#2D6B45",
            "profile_gradient_end":   "#1A3D28",
            "hover_bg":        "#F0F5F2",
        }


# ──────────────────────────────────────────────────────────────
#  MOCK DATA
# ──────────────────────────────────────────────────────────────

MOCK_DATA = {
    "user_name": "Demo User",
    "balance": "$X,XXX.XX",
    "exp_date": "XX/XX",
    "cvv": "XXX",
    "income": "$X,XXX.XX",
    "expense": "$X,XXX.XX",
    "savings": "$X,XXX.XX",
    "daily_limit": {
        "spent": "$XXX.XX",
        "limit": "$X,XXX.XX",
        "pct": 0.45,
    },
    "saving_plans": {
        "total": "$XX,XXX.XX",
        "plans": [
            {"name": "Emergency Fund",    "current": "$X,XXX", "target": "$XX,XXX", "pct": 0.50},
            {"name": "Vacation Fund",     "current": "$X,XXX", "target": "$X,XXX",  "pct": 0.60},
            {"name": "Home Down Payment", "current": "$X,XXX", "target": "$XX,XXX", "pct": 0.36},
        ],
    },
    "cashflow_monthly": {
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "income":  [4000, 5000, 3000, 6000, 5500, 6000, 4500, 5000, 7000, 6500, 8000, 7000],
        "expense": [3000, 4000, 3500, 5000, 4000, 4000, 3500, 4500, 5500, 5000, 6000, 5500],
    },
    "cashflow_total": "$X,XXX.XX",
    "transactions": [
        {"name": "Electricity Bill", "category": "Payments",      "date": "20XX-XX-01\n04:28:48", "amount": "$XXX.XX", "note": "Monthly electricity bill",    "status": "Failed"},
        {"name": "Weekly Groceries", "category": "Shopping",      "date": "20XX-XX-04\n04:28:48", "amount": "$XXX.XX", "note": "Groceries at local store",     "status": "Completed"},
        {"name": "Movie Night",      "category": "Entertainment", "date": "20XX-XX-07\n04:28:48", "amount": "$XX.XX",  "note": "Tickets for movies and snacks", "status": "Pending"},
        {"name": "Medical Check-up", "category": "Healthcare",    "date": "20XX-XX-10\n04:28:48", "amount": "$XXX.XX", "note": "Routine health check-up",      "status": "Pending"},
        {"name": "Dinner Out",       "category": "Dining Out",    "date": "20XX-XX-11\n04:28:48", "amount": "$XXX.XX", "note": "Family dinner at restaurant",  "status": "Pending"},
    ],
    "expense_categories": [
        {"name": "Rent & Living",   "pct": 0.60, "amount": "$X,XXX"},
        {"name": "Investment",      "pct": 0.15, "amount": "$XXX"},
        {"name": "Education",       "pct": 0.12, "amount": "$XXX"},
        {"name": "Food & Drink",    "pct": 0.08, "amount": "$XXX"},
        {"name": "Entertainment",   "pct": 0.05, "amount": "$XXX"},
    ],
    "expense_total": "$X,XXX",
    "recent_activity": [
        {"user": "Jamie Smith",     "action": "updated account settings", "time": "16:05", "group": "Today"},
        {"user": "Alex Johnson",    "action": "logged in",                "time": "13:05", "group": "Today"},
        {"user": "Morgan Lee",      "action": "added a new savings goal", "time": "02:05", "group": "Today"},
        {"user": "Taylor Green",    "action": "reviewed transactions",    "time": "17:05", "group": "Yesterday"},
        {"user": "Wilson Baptista", "action": "transferred funds",        "time": "12:05", "group": "Yesterday"},
    ],
}


# ──────────────────────────────────────────────────────────────
#  PROFILE / BALANCE CARD
# ──────────────────────────────────────────────────────────────

def create_profile_card(name: str, balance: str, exp: str, cvv: str, colors: dict) -> ft.Container:
    """Dark-green gradient card showing user name, balance, and card details."""
    return ft.Container(
        border_radius=16,
        padding=20,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[colors["profile_gradient_start"], colors["profile_gradient_end"]],
        ),
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.GRAIN, color="#FFFFFF", size=28),
                ft.Icon(ft.Icons.WIFI, color="#FFFFFF99", size=18),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=8),
            ft.Text(name, size=16, weight=ft.FontWeight.W_600, color="#FFFFFFDD"),
            ft.Container(height=4),
            ft.Text("Balance Amount", size=11, color="#FFFFFF99"),
            ft.Text(balance, size=28, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ft.Container(height=8),
            ft.Row([
                ft.Column([
                    ft.Text("EXP", size=10, color="#FFFFFF80"),
                    ft.Text(exp, size=12, weight=ft.FontWeight.W_600, color="#FFFFFFCC"),
                ], spacing=2),
                ft.Column([
                    ft.Text("CVV", size=10, color="#FFFFFF80"),
                    ft.Text(cvv, size=12, weight=ft.FontWeight.W_600, color="#FFFFFFCC"),
                ], spacing=2),
            ], spacing=20),
        ], spacing=0),
    )


# ──────────────────────────────────────────────────────────────
#  SUMMARY STAT CARDS
# ──────────────────────────────────────────────────────────────

def create_stat_card(title: str, amount: str, icon: str, colors: dict) -> ft.Container:
    """A summary stat card (Total Income, Total Expense, Total Savings)."""
    return ft.Container(
        expand=True,
        border_radius=14,
        bgcolor=colors["card_bg"],
        border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
        padding=18,
        content=ft.Column([
            ft.Row([
                ft.Container(
                    width=40, height=40,
                    border_radius=10,
                    bgcolor=colors["active_tab_bg"],
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(icon, color=colors["primary_accent"], size=20),
                ),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.MORE_VERT, color=colors["text_secondary"], size=18),
            ]),
            ft.Container(height=10),
            ft.Text(amount, size=24, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
            ft.Text(title, size=12, color=colors["text_secondary"]),
        ], spacing=2),
    )


# ──────────────────────────────────────────────────────────────
#  DAILY LIMIT CARD
# ──────────────────────────────────────────────────────────────

def create_daily_limit_card(spent: str, limit: str, pct: float, colors: dict) -> ft.Container:
    """Card with a progress bar showing daily spending vs limit."""
    return ft.Container(
        border_radius=14,
        bgcolor=colors["card_bg"],
        border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
        padding=18,
        content=ft.Column([
            ft.Row([
                ft.Text("Daily Limit", size=16, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                ft.Icon(ft.Icons.MORE_VERT, color=colors["text_secondary"], size=18),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=8),
            ft.Row([
                ft.Text(spent, size=14, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
                ft.Text(f"spent of {limit}", size=12, color=colors["text_secondary"]),
                ft.Container(expand=True),
                ft.Text(f"{int(pct * 100)}%", size=12, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
            ], spacing=5),
            ft.Container(height=6),
            ft.ProgressBar(
                value=pct,
                bgcolor=colors["border"],
                color=colors["primary_accent"],
                bar_height=8,
                border_radius=4,
            ),
        ], spacing=0),
    )


# ──────────────────────────────────────────────────────────────
#  SAVING PLANS
# ──────────────────────────────────────────────────────────────

def create_saving_plan_card(name: str, current: str, target: str, pct: float, colors: dict) -> ft.Container:
    """Individual saving fund card with progress bar."""
    return ft.Container(
        border_radius=12,
        bgcolor=colors["card_bg"],
        border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
        padding=14,
        content=ft.Column([
            ft.Row([
                ft.Container(
                    width=32, height=32,
                    border_radius=8,
                    bgcolor=colors["active_tab_bg"],
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.ACCOUNT_BALANCE, color=colors["primary_accent"], size=16),
                ),
                ft.Text(name, size=13, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.MORE_VERT, color=colors["text_secondary"], size=16),
            ], spacing=10),
            ft.Container(height=6),
            ft.ProgressBar(
                value=pct,
                bgcolor=colors["border"],
                color=colors["primary_accent"],
                bar_height=6,
                border_radius=3,
            ),
            ft.Container(height=4),
            ft.Row([
                ft.Text(current, size=12, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
                ft.Text(f"{int(pct * 100)}%", size=11, color=colors["text_secondary"]),
                ft.Container(expand=True),
                ft.Text(f"Target: {target}", size=11, color=colors["text_secondary"]),
            ], spacing=5),
        ], spacing=0),
    )


def create_saving_plans_section(plans_data: dict, colors: dict) -> ft.Container:
    """Full Saving Plans section with header and individual plan cards."""
    plan_cards = [
        create_saving_plan_card(
            p["name"], p["current"], p["target"], p["pct"], colors
        )
        for p in plans_data["plans"]
    ]

    return ft.Container(
        border_radius=14,
        bgcolor=colors["card_bg"],
        border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
        padding=18,
        content=ft.Column([
            ft.Row([
                ft.Text("Saving Plans", size=16, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                ft.Container(expand=True),
                ft.TextButton(
                    content=ft.Text("+ Add Plan"),
                    style=ft.ButtonStyle(color=colors["primary_accent"]),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.Text("Total Savings", size=12, color=colors["text_secondary"]),
            ]),
            ft.Text(plans_data["total"], size=26, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
            ft.Container(height=6),
            ft.Column(plan_cards, spacing=10),
        ], spacing=4),
    )


# ──────────────────────────────────────────────────────────────
#  TRANSACTIONS TABLE
# ──────────────────────────────────────────────────────────────

def _status_badge(status: str, colors: dict) -> ft.Container:
    """Small colored text badge for transaction status."""
    color_map = {
        "Completed": colors["success"],
        "Pending":   colors["warning"],
        "Failed":    colors["error"],
    }
    c = color_map.get(status, colors["text_secondary"])
    return ft.Text(status, size=12, color=c, weight=ft.FontWeight.W_600)


def create_transactions_table(transactions: list, colors: dict) -> ft.Container:
    """Full Recent Transactions section with data table."""
    header_style = ft.TextStyle(
        size=12, weight=ft.FontWeight.W_600, color=colors["text_secondary"]
    )

    rows = []
    for t in transactions:
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Column([
                            ft.Text(t["name"], size=13, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                            ft.Text(t["category"], size=11, color=colors["text_secondary"]),
                        ], spacing=2)
                    ),
                    ft.DataCell(ft.Text(t["date"], size=12, color=colors["text_secondary"])),
                    ft.DataCell(ft.Text(t["amount"], size=13, weight=ft.FontWeight.W_600, color=colors["text_primary"])),
                    ft.DataCell(ft.Text(t["note"], size=12, color=colors["text_secondary"])),
                    ft.DataCell(_status_badge(t["status"], colors)),
                ],
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Transaction Name", style=header_style)),
            ft.DataColumn(ft.Text("Date & Time", style=header_style)),
            ft.DataColumn(ft.Text("Amount", style=header_style)),
            ft.DataColumn(ft.Text("Note", style=header_style)),
            ft.DataColumn(ft.Text("Status", style=header_style)),
        ],
        rows=rows,
        border_radius=10,
        heading_row_color=colors["active_tab_bg"],
        data_row_max_height=70,
        column_spacing=20,
    )

    return ft.Container(
        border_radius=14,
        bgcolor=colors["card_bg"],
        border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
        padding=18,
        content=ft.Column([
            ft.Row([
                ft.Text("Recent Transactions", size=16, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                ft.Container(expand=True),
                ft.Container(
                    border_radius=8,
                    border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
                    padding=ft.Padding(left=12, top=6, right=12, bottom=6),
                    content=ft.Row([
                        ft.Text("This Month", size=12, color=colors["text_secondary"]),
                        ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=16, color=colors["text_secondary"]),
                    ], spacing=4),
                ),
                ft.Container(
                    width=32, height=32,
                    border_radius=8,
                    border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.TUNE, size=16, color=colors["text_secondary"]),
                ),
            ], spacing=10),
            ft.Container(height=6),
            ft.Container(
                content=table,
                expand=True,
            ),
        ], spacing=0),
    )


# ──────────────────────────────────────────────────────────────
#  RECENT ACTIVITY FEED
# ──────────────────────────────────────────────────────────────

_AVATAR_COLORS = ["#37C372", "#F5A623", "#3B82F6", "#A855F7", "#EC4899"]


def create_activity_item(user: str, action: str, time: str, index: int, colors: dict) -> ft.Container:
    """Single activity feed entry with colored avatar."""
    avatar_color = _AVATAR_COLORS[index % len(_AVATAR_COLORS)]
    initials = "".join(w[0] for w in user.split()[:2]).upper()

    return ft.Container(
        padding=ft.Padding(left=0, top=6, right=0, bottom=6),
        content=ft.Row([
            ft.CircleAvatar(
                content=ft.Text(initials, size=11, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                bgcolor=avatar_color,
                radius=18,
            ),
            ft.Column([
                ft.Row([
                    ft.Text(user, size=13, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                    ft.Text(action, size=12, color=colors["text_secondary"]),
                ], spacing=4, wrap=True),
                ft.Text(time, size=11, color=colors["text_secondary"]),
            ], spacing=2, expand=True),
        ], spacing=10),
    )


def create_recent_activity(activities: list, colors: dict) -> ft.Container:
    """Recent Activity feed grouped by Today/Yesterday."""
    groups: dict[str, list] = {}
    for a in activities:
        groups.setdefault(a["group"], []).append(a)

    controls = []
    global_idx = 0
    for group_name, items in groups.items():
        controls.append(
            ft.Container(
                padding=ft.Padding(top=10 if controls else 0, bottom=4),
                content=ft.Text(group_name, size=13, weight=ft.FontWeight.W_700, color=colors["text_primary"]),
            )
        )
        for item in items:
            controls.append(create_activity_item(item["user"], item["action"], item["time"], global_idx, colors))
            global_idx += 1

    return ft.Container(
        border_radius=14,
        bgcolor=colors["card_bg"],
        border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
        padding=18,
        content=ft.Column([
            ft.Row([
                ft.Text("Recent Activity", size=16, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.MORE_VERT, color=colors["text_secondary"], size=18),
            ]),
            ft.Container(height=4),
            ft.Column(controls, spacing=0, scroll=ft.ScrollMode.AUTO),
        ], spacing=0),
    )


# ──────────────────────────────────────────────────────────────
#  MATPLOTLIB CHARTS
# ──────────────────────────────────────────────────────────────

def _fig_to_base64(fig) -> str:
    """Render a matplotlib figure to a base64-encoded PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", transparent=True)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def generate_cashflow_chart(monthly_data: dict, colors: dict) -> ft.Image:
    """Grouped bar chart — Income vs. Expense per month, returned as ft.Image."""
    months = monthly_data["months"]
    income = monthly_data["income"]
    expense = monthly_data["expense"]

    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    x = range(len(months))
    bar_width = 0.35

    ax.bar([i - bar_width / 2 for i in x], income,  bar_width, label="Income",  color=colors["chart_income"])
    ax.bar([i + bar_width / 2 for i in x], expense, bar_width, label="Expense", color=colors["chart_expense"])

    ax.set_xticks(list(x))
    ax.set_xticklabels(months, fontsize=9, color=colors["chart_text"])
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v / 1000:.0f}K" if v != 0 else "0"))
    ax.tick_params(axis="y", labelsize=9, colors=colors["chart_text"])
    ax.spines[:].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.grid(axis="y", color=colors["chart_grid"], linewidth=0.5, alpha=0.5)
    ax.set_axisbelow(True)

    legend = ax.legend(
        loc="upper right", fontsize=9, frameon=True,
        facecolor=colors["chart_bg"], edgecolor=colors["chart_grid"],
        labelcolor=colors["chart_text"],
    )
    legend.get_frame().set_alpha(0.8)

    b64 = _fig_to_base64(fig)
    return ft.Image(src=f"data:image/png;base64,{b64}", fit=ft.BoxFit.CONTAIN)


def generate_statistic_donut(categories: list, total_label: str, colors: dict) -> ft.Image:
    """Donut / ring chart for expense categories, returned as ft.Image."""
    labels = [c["name"] for c in categories]
    sizes = [c["pct"] for c in categories]

    # Graduated green palette for slices
    slice_colors = [
        colors["primary_accent"],
        "#5BB98B",
        "#7ECBA4",
        "#A8DDBF",
        "#D2F0DE",
    ]

    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    fig.patch.set_alpha(0)

    wedges, _ = ax.pie(
        sizes,
        labels=None,
        colors=slice_colors[:len(sizes)],
        startangle=90,
        wedgeprops=dict(width=0.35, edgecolor="none"),
    )

    # Center text
    ax.text(0, 0.08, "Total Expense", ha="center", va="center",
            fontsize=7, color=colors["chart_text"])
    ax.text(0, -0.12, total_label, ha="center", va="center",
            fontsize=12, fontweight="bold", color=colors["text_primary"] if colors["text_primary"] != "#2D3B34" else "#2D3B34")

    b64 = _fig_to_base64(fig)
    return ft.Image(src=f"data:image/png;base64,{b64}", fit=ft.BoxFit.CONTAIN, width=180, height=180)


def create_statistic_section(categories: list, total_label: str, colors: dict) -> ft.Container:
    """Full Statistic panel — donut chart + category legend with toggles."""
    donut = generate_statistic_donut(categories, total_label, colors)

    # Legend rows
    legend_rows = []
    pct_colors = ["#37C372", "#5BB98B", "#7ECBA4", "#A8DDBF", "#D2F0DE"]
    for i, cat in enumerate(categories):
        legend_rows.append(
            ft.Container(
                padding=ft.Padding(left=0, top=3, right=0, bottom=3),
                content=ft.Row([
                    ft.Container(
                        width=32, height=20, border_radius=4,
                        bgcolor=pct_colors[i % len(pct_colors)],
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text(f"{int(cat['pct'] * 100)}%", size=10, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ),
                    ft.Text(cat["name"], size=12, color=colors["text_primary"], expand=True),
                    ft.Text(cat["amount"], size=12, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                ], spacing=8),
            )
        )

    return ft.Container(
        border_radius=14,
        bgcolor=colors["card_bg"],
        border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
        padding=18,
        content=ft.Column([
            # Header with toggle tabs
            ft.Row([
                ft.Text("Statistic", size=16, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                ft.Container(expand=True),
                ft.Container(
                    border_radius=8,
                    border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
                    padding=ft.Padding(left=10, top=5, right=10, bottom=5),
                    content=ft.Row([
                        ft.Text("This Month", size=11, color=colors["text_secondary"]),
                        ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=14, color=colors["text_secondary"]),
                    ], spacing=2),
                ),
            ]),
            ft.Container(height=4),
            # Income / Expense toggle
            ft.Row([
                ft.Container(
                    border_radius=6,
                    padding=ft.Padding(left=12, top=6, right=12, bottom=6),
                    border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
                    content=ft.Text("Income ($X,XXX)", size=11, color=colors["text_secondary"]),
                ),
                ft.Container(
                    border_radius=6,
                    padding=ft.Padding(left=12, top=6, right=12, bottom=6),
                    bgcolor=colors["text_primary"],
                    content=ft.Text("Expense ($X,XXX)", size=11, color=colors["card_bg"], weight=ft.FontWeight.W_600),
                ),
            ], spacing=6),
            ft.Container(height=4),
            # Donut chart
            ft.Container(content=donut, alignment=ft.Alignment.CENTER),
            ft.Container(height=8),
            # Legend
            ft.Column(legend_rows, spacing=2),
        ], spacing=2),
    )


# ──────────────────────────────────────────────────────────────
#  CASHFLOW SECTION WRAPPER
# ──────────────────────────────────────────────────────────────

def create_cashflow_section(monthly_data: dict, total: str, colors: dict) -> ft.Container:
    """Full Cashflow panel — total balance + bar chart."""
    chart_image = generate_cashflow_chart(monthly_data, colors)

    return ft.Container(
        border_radius=14,
        bgcolor=colors["card_bg"],
        border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
        padding=18,
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Cashflow", size=16, weight=ft.FontWeight.W_600, color=colors["text_primary"]),
                    ft.Container(height=2),
                    ft.Row([
                        ft.Text("Total Balance", size=12, color=colors["text_secondary"]),
                    ]),
                    ft.Text(total, size=26, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
                ], spacing=0),
                ft.Container(expand=True),
                ft.Container(
                    border_radius=8,
                    border=ft.Border(left=ft.BorderSide(1, colors["border"]), top=ft.BorderSide(1, colors["border"]), right=ft.BorderSide(1, colors["border"]), bottom=ft.BorderSide(1, colors["border"])),
                    padding=ft.Padding(left=12, top=6, right=12, bottom=6),
                    content=ft.Row([
                        ft.Text("This Year", size=12, color=colors["text_secondary"]),
                        ft.Icon(ft.Icons.ARROW_DROP_DOWN, size=16, color=colors["text_secondary"]),
                    ], spacing=4),
                ),
            ]),
            ft.Container(height=8),
            chart_image,
        ], spacing=0),
    )
