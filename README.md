# Bitcoin Clock — Kindle Friendly (No JavaScript)

A minimal Bitcoin price "clock" built for Kindle e‑ink browsers.
- ✅ No JavaScript (Kindle-friendly)
- ✅ Big blocky digits rendered as inline SVG
- ✅ Auto-refreshes every 15 seconds (via meta refresh)
- ✅ Updates from server every minute (via GitHub Actions + CoinGecko)

> Kindle refreshes every 15 seconds, but GitHub Actions can only run at **1-minute** granularity on cron.
> That means the displayed price may change at most once per minute.

## Quick Start (GitHub Pages)

1. **Create a new repo** on GitHub named `bitcoin-clock-kindle` (or any name).
2. Upload these files (or push via git).
3. Go to **Settings → Pages** and set:
   - **Build and deployment** → *Deploy from branch*
   - **Branch**: `main` (root)
4. Go to **Actions** and enable workflows if prompted.
5. The clock will be served at `https://YOUR_USER.github.io/YOUR_REPO/`

### Change update frequency
- Kindle page refresh is controlled in the generated HTML: 15 seconds by default.
- GitHub Actions runs **every minute**. 15 seconds is not possible on GitHub cron.
- If you need true ~15s updates, deploy `render.py` on a tiny server/Cloudflare Worker and point Kindle to that URL.

## Files

- `render.py` — Fetches BTC price (USD) and generates `index.html` with inline SVG block digits.
- `.github/workflows/update.yml` — CI that runs every minute: runs `render.py`, commits & pushes result.
- `index.html` — Generated HTML (overwritten each run).

## Local Test

```bash
python3 render.py
# open index.html in your browser (desktop/tablet). On Kindle, upload via web hosting or use Pages.
```

## Configuration

- Currency: USD (BTC/USD). Decimals omitted, as requested.
- Display: `$` + thousands separators (e.g., `$123,456`).
- Theme: Black digits on white background for crisp e‑ink.

---

Made for Kindle e‑ink devices. Enjoy.