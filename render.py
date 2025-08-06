#!/usr/bin/env python3
import json, urllib.request, time, pathlib

OUT = pathlib.Path(__file__).resolve().parent / "index.html"

# 3x5 block font patterns for digits 0-9
# Each digit is a 5-row list of 3 columns (0/1). 1 renders a filled square.
DIGITS = {
    "0": [
        [1,1,1],
        [1,0,1],
        [1,0,1],
        [1,0,1],
        [1,1,1],
    ],
    "1": [
        [0,1,0],
        [1,1,0],
        [0,1,0],
        [0,1,0],
        [1,1,1],
    ],
    "2": [
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [1,0,0],
        [1,1,1],
    ],
    "3": [
        [1,1,1],
        [0,0,1],
        [0,1,1],
        [0,0,1],
        [1,1,1],
    ],
    "4": [
        [1,0,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [0,0,1],
    ],
    "5": [
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [0,0,1],
        [1,1,1],
    ],
    "6": [
        [1,1,1],
        [1,0,0],
        [1,1,1],
        [1,0,1],
        [1,1,1],
    ],
    "7": [
        [1,1,1],
        [0,0,1],
        [0,1,0],
        [0,1,0],
        [0,1,0],
    ],
    "8": [
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [1,0,1],
        [1,1,1],
    ],
    "9": [
        [1,1,1],
        [1,0,1],
        [1,1,1],
        [0,0,1],
        [1,1,1],
    ],
    ",": [  # render comma as a small block at bottom-right
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,1],
        [0,1,0],
    ],
    "$": [  # simple $ representation
        [0,1,0],
        [1,1,1],
        [0,1,0],
        [1,1,1],
        [0,1,0],
    ]
}

def fetch_btc_usd():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["bitcoin"]["usd"]

def format_price_int(usd_float):
    # No decimals, thousands separator, with $ prefix
    value = int(round(usd_float))
    return "${:,}".format(value)

def render_svg_for_text(text, block=28, gap=8, margin=20):
    # Render inline SVG where each char is a 3x5 grid of squares.
    # block: pixel size of each square; gap: spacing; margin: page margin
    cols_per_char = 3
    rows = 5
    char_width = cols_per_char * block + (cols_per_char - 1) * gap
    char_height = rows * block + (rows - 1) * gap
    char_gap = block  # gap between characters
    
    width = margin*2 + len(text)*char_width + (len(text)-1)*char_gap
    height = margin*2 + char_height

    # Build rects
    rects = []
    x_cursor = margin
    for ch in text:
        pattern = DIGITS.get(ch, DIGITS.get("0"))
        for r in range(rows):
            for c in range(cols_per_char):
                if pattern[r][c]:
                    x = x_cursor + c*(block+gap)
                    y = margin + r*(block+gap)
                    rects.append(f'<rect x="{x}" y="{y}" width="{block}" height="{block}" rx="4" ry="4" />')
        x_cursor += char_width + char_gap

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{text}">
  <title>{text}</title>
  <g fill="#000000">
    {''.join(rects)}
  </g>
</svg>'''
    return svg, width, height

def build_html(text, svg):
    # Kindle-friendly HTML: no JS, big centered SVG, meta refresh 15s
    # Light background (#fff) and black blocks for maximum e-ink contrast.
    last_updated = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bitcoin Clock</title>
  <meta http-equiv="refresh" content="15">
  <style>
    html, body {{
      height: 100%;
      margin: 0;
      background: #ffffff;
      color: #000000;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: monospace;
    }}
    .wrap {{
      text-align: center;
    }}
    .updated {{
      margin-top: 12px;
      font-size: 14px;
      color: #444;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    {svg}
    <div class="updated">Last updated: {last_updated}</div>
  </div>
</body>
</html>'''

def main():
    try:
        price = fetch_btc_usd()
    except Exception as e:
        text = "ERROR"
        svg, _, _ = render_svg_for_text(text)
        html = build_html(text, svg)
        OUT.write_text(html, encoding="utf-8")
        return

    price_text = format_price_int(price)  # e.g., "$67,845"
    svg, _, _ = render_svg_for_text(price_text)
    html = build_html(price_text, svg)
    OUT.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()