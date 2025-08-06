#!/usr/bin/env python3
import json, urllib.request, time, pathlib

OUT = pathlib.Path(__file__).resolve().parent / "index.html"

DIGITS = {
    "0": [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
    "1": [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[1,1,1]],
    "2": [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],
    "3": [[1,1,1],[0,0,1],[0,1,1],[0,0,1],[1,1,1]],
    "4": [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
    "5": [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
    "6": [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],
    "7": [[1,1,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0]],
    "8": [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],
    "9": [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[1,1,1]],
    ",": [[0,0,0],[0,0,0],[0,0,0],[0,0,1],[0,1,0]],
    "$": [[0,1,0],[1,1,1],[0,1,0],[1,1,1],[0,1,0]]
}

def fetch_btc_usd():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["bitcoin"]["usd"]

def format_price_int(usd_float):
    value = int(round(usd_float))
    return "${:,}".format(value)

def render_svg_for_text(text, block=24, gap=6, margin=20):
    cols, rows = 3, 5
    char_width = cols * block + (cols - 1) * gap
    char_height = rows * block + (rows - 1) * gap
    char_gap = block
    width = margin*2 + len(text)*char_width + (len(text)-1)*char_gap
    height = margin*2 + char_height

    rects = []
    x_cursor = margin
    for ch in text:
        pattern = DIGITS.get(ch, DIGITS["0"])
        for r in range(rows):
            for c in range(cols):
                if pattern[r][c]:
                    x = x_cursor + c*(block+gap)
                    y = margin + r*(block+gap)
                    rects.append(f'<rect x="{x}" y="{y}" width="{block}" height="{block}" rx="4" ry="4"/>')
        x_cursor += char_width + char_gap

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{text}" style="max-width:100%; height:auto;">
  <title>{text}</title>
  <g fill="#000000">
    {''.join(rects)}
  </g>
</svg>"""
    return svg

def build_html(text, svg):
    last_updated = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    return f"""<!DOCTYPE html>
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
      padding: 1em;
    }}
    .updated {{
      margin-top: 12px;
      font-size: 14px;
      color: #444;
    }}
    svg {{
      display: block;
      margin: 0 auto;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    {svg}
    <div class="updated">Last updated: {last_updated}</div>
  </div>
</body>
</html>"""

def main():
    try:
        price = fetch_btc_usd()
    except Exception:
        text = "ERROR"
        svg = render_svg_for_text(text)
        html = build_html(text, svg)
        OUT.write_text(html, encoding="utf-8")
        return

    text = format_price_int(price)
    svg = render_svg_for_text(text)
    html = build_html(text, svg)
    OUT.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()
