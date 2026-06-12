"""
Generate 3 schematic diagrams for S0016 article.
Run: python generate_diagrams.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Chinese font
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

# Color palette
C_PRICE = "#2c3e50"
C_ZONE = "#3498db"
C_ZONE_FILL = "#3498db"
C_SUPPORT_LINE = "#e74c3c"
C_BUY = "#27ae60"
C_SELL = "#e74c3c"
C_TEXT = "#2c3e50"
C_BG = "#fafafa"
C_GRID = "#ecf0f1"
C_ARROW = "#e67e22"
C_SHADE = "#eaf2f8"
C_SHADE_BORDER = "#2980b9"


def style_ax(ax, title=""):
    ax.set_facecolor(C_BG)
    ax.grid(True, color=C_GRID, linewidth=0.5, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#bdc3c7")
    ax.spines["bottom"].set_color("#bdc3c7")
    ax.tick_params(colors="#7f8c8d", labelsize=9)
    if title:
        ax.set_title(title, fontsize=15, fontweight="bold", color=C_TEXT, pad=12)


def draw_candle(ax, x, o, h, l, c, width=0.6):
    body_color = C_BUY if c >= o else C_SELL
    edge_color = "#1e8449" if c >= o else "#c0392b"
    body_bottom = min(o, c)
    body_height = abs(c - o)
    if body_height < 0.05:
        body_height = 0.05
        body_bottom = min(o, c)
    rect = patches.FancyBboxPatch(
        (x - width / 2, body_bottom), width, body_height,
        boxstyle="round,pad=0.02", facecolor=body_color, edgecolor=edge_color, linewidth=1.2, alpha=0.9
    )
    ax.add_patch(rect)
    ax.plot([x, x], [l, body_bottom], color=edge_color, linewidth=1, alpha=0.8)
    ax.plot([x, x], [body_bottom + body_height, h], color=edge_color, linewidth=1, alpha=0.8)


def save(fig, name):
    fig.savefig(name, dpi=180, bbox_inches="tight", facecolor="white", edgecolor="none")
    plt.close(fig)
    print(f"Saved: {name}")


# ============================================================================
# Diagram 1: Failed case - support line illusion
# ============================================================================
def diagram1():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    style_ax(ax)

    np.random.seed(42)

    # Segment 1: downward to point a, then bounce up
    seg1_x = list(range(10))
    seg1_prices = [28, 27.2, 26.5, 25.8, 25.0, 24.2, 23.5, 22.8, 22.5, 23.0]

    # Bounce / consolidation
    mid_x = list(range(10, 18))
    mid_prices = [23.0, 23.8, 24.5, 25.2, 25.0, 24.8, 24.5, 24.0]

    # Drop back and break below
    seg2_x = list(range(18, 28))
    seg2_prices = [23.5, 23.0, 22.5, 22.3, 22.0, 21.5, 20.8, 20.2, 19.5, 19.0]

    all_x = seg1_x + mid_x + seg2_x
    all_p = seg1_prices + mid_prices + seg2_prices

    ax.plot(all_x, all_p, color=C_PRICE, linewidth=2, zorder=3)

    # Mark point a (lowest point of first segment)
    a_idx = 8
    a_price = 22.5
    ax.annotate("前低 a", xy=(a_idx, a_price), xytext=(a_idx + 1.5, a_price + 2.5),
                fontsize=13, fontweight="bold", color=C_TEXT,
                arrowprops=dict(arrowstyle="->", color=C_ARROW, lw=1.5))
    ax.plot(a_idx, a_price, "o", color=C_SELL, markersize=8, zorder=5)

    # Horizontal support line at a
    ax.axhline(y=a_price, color=C_SUPPORT_LINE, linewidth=1.5, linestyle="--", alpha=0.7, zorder=2)
    ax.text(26, a_price + 0.3, "支撑线？", fontsize=11, color=C_SUPPORT_LINE, ha="center", style="italic")

    # Buy point where price touches the line
    buy_x = 20
    buy_y = 22.5
    ax.annotate("买入", xy=(buy_x, buy_y), xytext=(buy_x + 2, buy_y + 1.8),
                fontsize=12, fontweight="bold", color=C_BUY,
                arrowprops=dict(arrowstyle="->", color=C_BUY, lw=1.5))
    ax.plot(buy_x, buy_y, "^", color=C_BUY, markersize=12, zorder=5)

    # Arrow showing continued drop
    ax.annotate("", xy=(25, 19.2), xytext=(23, 21.0),
                arrowprops=dict(arrowstyle="-|>", color=C_SELL, lw=2.5))
    ax.text(25.5, 19.0, "继续下跌", fontsize=12, fontweight="bold", color=C_SELL, ha="center")

    # Shade the "breakdown" area
    ax.fill_between(range(20, 28), a_price, [22.3, 22.0, 21.5, 20.8, 20.2, 19.5, 19.0, 18.5],
                    alpha=0.1, color=C_SELL, zorder=1)

    ax.set_xlim(-1, 29)
    ax.set_ylim(18, 29)
    ax.set_xlabel("")
    ax.set_ylabel("")

    fig.text(0.5, 0.02, "图1：在前低一条线上抄底，结果被套", ha="center", fontsize=11, color="#7f8c8d", style="italic")

    save(fig, "CLXS0016-1.png")


# ============================================================================
# Diagram 2: Core logic - fractal zones
# ============================================================================
def diagram2():
    fig, ax = plt.subplots(figsize=(10, 6))
    style_ax(ax)

    # Previous downward segment 1 (left side, higher)
    # - High start, low end around y=18
    prev1_x = list(range(12))
    prev1_p = [32, 30.5, 29, 27.5, 26, 24.5, 23.5, 22.5, 21.5, 22.0, 23.5, 25.0]

    # Upward segment
    up_x = list(range(12, 20))
    up_p = [25.0, 26.5, 28, 29.5, 30, 29.5, 29.0, 28.5]

    # Previous downward segment 2
    prev2_x = list(range(20, 32))
    prev2_p = [28.5, 27.0, 25.5, 24.0, 23.0, 22.0, 21.0, 20.5, 20.0, 21.0, 22.5, 24.0]

    # Upward segment 2
    up2_x = list(range(32, 38))
    up2_p = [24.0, 25.5, 27.0, 28.0, 27.5, 27.0]

    # Current downward segment entering zones
    cur_x = list(range(38, 50))
    cur_p = [27.0, 25.5, 24.0, 22.5, 21.5, 20.5, 19.5, 19.0, 18.5, 19.2, 20.5, 22.0]

    all_x = prev1_x + up_x + prev2_x + up2_x + cur_x
    all_p = prev1_p + up_p + prev2_p + up2_p + cur_p

    ax.plot(all_x, all_p, color=C_PRICE, linewidth=2, zorder=3)

    # Fractal zone for prev segment 1 (around the low area, x=7~9)
    zone1_high = 23.5
    zone1_low = 21.5
    zone1_left = 6
    zone1_right = 10
    rect1 = patches.FancyBboxPatch(
        (zone1_left, zone1_low), zone1_right - zone1_left, zone1_high - zone1_low,
        boxstyle="round,pad=0.3", facecolor=C_ZONE_FILL, edgecolor=C_SHADE_BORDER,
        linewidth=1.5, alpha=0.15, zorder=2
    )
    ax.add_patch(rect1)
    ax.text(8, (zone1_high + zone1_low) / 2, "分型区间①", fontsize=10, ha="center",
            color=C_SHADE_BORDER, fontweight="bold", alpha=0.8)

    # Fractal zone for prev segment 2 (around the low area, x=26~29)
    zone2_high = 22.0
    zone2_low = 19.5
    zone2_left = 25
    zone2_right = 31
    rect2 = patches.FancyBboxPatch(
        (zone2_left, zone2_low), zone2_right - zone2_left, zone2_high - zone2_low,
        boxstyle="round,pad=0.3", facecolor=C_ZONE_FILL, edgecolor=C_SHADE_BORDER,
        linewidth=1.5, alpha=0.15, zorder=2
    )
    ax.add_patch(rect2)
    ax.text(28, (zone2_high + zone2_low) / 2, "分型区间②", fontsize=10, ha="center",
            color=C_SHADE_BORDER, fontweight="bold", alpha=0.8)

    # Highlight: current segment's low enters zone
    cur_low_x = 45
    cur_low_y = 18.5
    ax.plot(cur_low_x, cur_low_y, "o", color=C_SELL, markersize=8, zorder=5)
    ax.annotate("最低价进入区间", xy=(cur_low_x, cur_low_y),
                xytext=(cur_low_x + 2.5, cur_low_y - 1.5),
                fontsize=10, color=C_TEXT,
                arrowprops=dict(arrowstyle="->", color=C_ARROW, lw=1.5))

    # Previous segments' extreme points (lowest prices)
    prev1_extreme = 21.5  # zone1 extreme (lowest of prev segment 1)
    prev2_extreme = 20.0  # zone2 extreme (lowest of prev segment 2)

    # Mark extreme lines
    ax.axhline(y=prev1_extreme, color="#8e44ad", linewidth=1, linestyle=":", alpha=0.5, zorder=1,
               xmin=0.76, xmax=1.0)
    ax.text(48, prev1_extreme + 0.3, "线段①极值", fontsize=9, color="#8e44ad", ha="center")

    ax.axhline(y=prev2_extreme, color="#c0392b", linewidth=1, linestyle=":", alpha=0.5, zorder=1,
               xmin=0.76, xmax=1.0)
    ax.text(48, prev2_extreme + 0.3, "线段②极值", fontsize=9, color="#c0392b", ha="center")

    # Signal point: above BOTH extremes (close > prev.extreme_price)
    # Price bounces from zone low back above extremes
    sig_x = 48
    sig_y = 22.0
    ax.plot(sig_x, sig_y, "*", color="#f39c12", markersize=18, zorder=6)
    ax.annotate("收盘价 > 极值\n反转信号", xy=(sig_x, sig_y),
                xytext=(sig_x + 1.8, sig_y + 2.2),
                fontsize=10, fontweight="bold", color="#f39c12",
                arrowprops=dict(arrowstyle="->", color="#f39c12", lw=1.5))

    # Label the segments
    ax.text(5, 33, "向下线段①", fontsize=11, color="#7f8c8d", ha="center")
    ax.text(15, 30.5, "向上线段", fontsize=10, color="#7f8c8d", ha="center")
    ax.text(25, 29.5, "向下线段②", fontsize=11, color="#7f8c8d", ha="center")
    ax.text(35, 28.5, "向上线段", fontsize=10, color="#7f8c8d", ha="center")
    ax.text(43, 28, "当前向下线段\n（≥5笔）", fontsize=11, color=C_TEXT, fontweight="bold", ha="center")

    # Bi markers on current segment (at least 5)
    for bx, label in [(39, "笔1"), (41, "笔2"), (43, "笔3"), (45, "笔4"), (47, "笔5")]:
        idx = bx
        ax.plot(idx, all_p[idx], "o", color="#95a5a6", markersize=4, zorder=4)

    ax.set_xlim(-2, 52)
    ax.set_ylim(17, 34)

    fig.text(0.5, 0.02, "图2：S0016 核心逻辑——分型区间 vs 单点支撑", ha="center", fontsize=11,
             color="#7f8c8d", style="italic")

    save(fig, "CLXS0016-2.png")


# ============================================================================
# Diagram 3: Three pullbacks to same zone
# ============================================================================
def diagram3():
    fig, ax = plt.subplots(figsize=(10, 6))
    style_ax(ax)

    # Zone
    zone_high = 20.0
    zone_low = 18.0
    zone_left = 0
    zone_right = 48

    # Draw support zone as background
    rect = patches.FancyBboxPatch(
        (zone_left, zone_low), zone_right - zone_left, zone_high - zone_low,
        boxstyle="round,pad=0.3", facecolor=C_ZONE_FILL, edgecolor=C_SHADE_BORDER,
        linewidth=2, alpha=0.12, zorder=1
    )
    ax.add_patch(rect)
    ax.text(24, (zone_high + zone_low) / 2, "分型区间（支撑带）", fontsize=12,
            ha="center", color=C_SHADE_BORDER, fontweight="bold", alpha=0.5)

    # Price path: down to zone, bounce, down again, bounce, down third, bounce
    np.random.seed(7)

    # Pullback 1: x=0~15
    x1 = list(range(0, 16))
    p1 = [25, 23.5, 22, 20.5, 19.5, 18.5, 18.2, 19.0, 20.5, 22.0, 23.0, 23.5, 23.0, 22.5, 22.0, 22.5]

    # Pullback 2: x=15~32
    x2 = list(range(16, 33))
    p2_start = 22.5
    p2 = [22.5, 21.5, 20.5, 19.5, 18.8, 18.3, 18.5, 19.5, 20.0, 21.5, 22.5, 23.0, 22.5, 22.0, 21.5, 22.0, 22.5]

    # Pullback 3: x=32~48
    x3 = list(range(33, 49))
    p3 = [22.5, 21.0, 20.0, 19.0, 18.5, 18.0, 18.3, 19.0, 19.5, 20.5, 21.5, 22.0, 22.5, 23.0, 22.5, 22.0]

    all_x = x1 + x2 + x3
    all_p = p1 + p2 + p3

    ax.plot(all_x, all_p, color=C_PRICE, linewidth=2, zorder=3)

    # Pullback 1 signal
    pb1_x, pb1_y = 6, 18.2
    ax.plot(pb1_x, pb1_y, "*", color="#f39c12", markersize=16, zorder=6)
    ax.annotate(
        "第1次回踩\nPin Bar 信号",
        xy=(pb1_x, pb1_y), xytext=(pb1_x - 6, pb1_y + 3.5),
        fontsize=10, fontweight="bold", color="#f39c12",
        arrowprops=dict(arrowstyle="->", color="#f39c12", lw=1.5)
    )
    # Pin bar visual: long lower wick
    ax.plot([pb1_x, pb1_x], [18.2, 17.2], color="#f39c12", linewidth=2.5, alpha=0.6, zorder=5)
    ax.plot([pb1_x - 0.3, pb1_x + 0.3], [19.0, 19.0], color="#f39c12", linewidth=3, alpha=0.6, zorder=5)

    # Pullback 2 signal
    pb2_x, pb2_y = 22, 18.3
    ax.plot(pb2_x, pb2_y, "*", color="#2ecc71", markersize=16, zorder=6)
    ax.annotate(
        "第2次回踩\nMACD 金叉",
        xy=(pb2_x, pb2_y), xytext=(pb2_x - 6, pb2_y - 3.5),
        fontsize=10, fontweight="bold", color="#2ecc71",
        arrowprops=dict(arrowstyle="->", color="#2ecc71", lw=1.5)
    )

    # Pullback 3 signal
    pb3_x, pb3_y = 38, 18.0
    ax.plot(pb3_x, pb3_y, "*", color="#9b59b6", markersize=16, zorder=6)
    ax.annotate(
        "第3次回踩\nMA5 拐头",
        xy=(pb3_x, pb3_y), xytext=(pb3_x + 3, pb3_y + 3.5),
        fontsize=10, fontweight="bold", color="#9b59b6",
        arrowprops=dict(arrowstyle="->", color="#9b59b6", lw=1.5)
    )

    # Zone boundary lines
    ax.axhline(y=zone_high, color=C_SHADE_BORDER, linewidth=1, linestyle="--", alpha=0.4, zorder=1)
    ax.axhline(y=zone_low, color=C_SHADE_BORDER, linewidth=1, linestyle="--", alpha=0.4, zorder=1)

    ax.set_xlim(-2, 50)
    ax.set_ylim(16, 26)

    fig.text(0.5, 0.02, "图3：同一支撑区间的三次回踩，信号类型各不相同", ha="center", fontsize=11,
             color="#7f8c8d", style="italic")

    save(fig, "CLXS0016-3.png")


if __name__ == "__main__":
    diagram1()
    diagram2()
    diagram3()
    print("All diagrams generated.")
