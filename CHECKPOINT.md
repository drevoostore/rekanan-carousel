# Session Checkpoint - 2026-05-23

## What We Did Today

### Morning Session (Already Done)
- Confirmed all development and testing will **stay on dev1 (this server, 192.168.22.235)**. No prod deployment.
- **Copied all needed files** into a clean directory: `/home/dev/rekanan-carousel/`
- **Updated `scripts/generate_carousel.py`** to use relative paths (no hardcoded `/home/dev/shopify` paths), portable across directories.
- **Fixed iframe height issue** — added `postMessage` auto-height script so PageFly receives the correct iframe height dynamically. No scrollbar.
- **Successfully tested** the iframe embed in PageFly. Works as expected.

### Afternoon Session (Today's New Work)

#### 1. Added Searchbox 🔍
- Added a **search input** with magnifying glass icon above the carousel
- **Live filtering** by `data-nama` (nama rekanan) and `data-kota` (city)
- "No results" message appears when nothing matches
- Auto-height `sendHeight()` called after filtering so PageFly resizes correctly
- Removed the header title/subtitle ("Rekanan Directory" / "Cari rekanan...")

#### 2. Consistent Card Height 📐
- Cards now use `display: flex; flex-direction: column`
- `.card-content` wrapper with `flex: 1 1 auto` fills available space
- `.address` has `margin-top: auto` — **pinned to bottom**
- `min-height: 280px` (desktop) / 250px (tablet) / 240px (mobile)
- All cards same height regardless of content length

#### 3. Fixed PageFly iFrame Code 🐛
The user's original code had 4 bugs:
- `widht` → `width` (typo)
- `stylee.height` → `style.height` (typo)
- Missing `id="carousel-container"` and `id="rekanan-iframe"` attributes
- `e.origin` check must match exact domain

Corrected code documented below.

#### 4. Card Sizing — Fixed Width → Responsive 📱
**Problem:** Fixed `flex: 0 0 350px` meant 3 cards on 1743px with fragments. Used `window.innerWidth` instead of actual wrapper width.

**Solution:**
- JS dynamically calculates card width based on **actual wrapper width**
- Uses CSS custom property `--card-width` set by JS
- `wrapper.clientWidth` instead of `window.innerWidth`
- Track has `padding: 0 55px` so first card starts after nav buttons
- Nav buttons sit at `left: 5px / right: 5px` inside padding

#### 5. Card Config Testing
We tested multiple configs and settled on **4 cards desktop**:

| Config | Card Width | Result | Verdict |
|--------|-----------|--------|---------|
| 330px fixed | ~370px total | 3 cards + fragment | ❌ Wrong math |
| **4-card responsive** | ~397px | **4 exact** | ✅ **FINAL** |
| 5-card | ~319px | 5 exact | Too crowded, reverted |

#### 6. Mobile Breakpoints Reworked 📱
**Problem:** 320px showed 2 unreadable tiny cards.

**Final breakpoints:**

| Screen Width | Cards Shown | Card Width (at 320px) |
|-------------|-------------|----------------------|
| **<420px** | **1 card** | **~260px** (readable!) |
| 420–720px | 2 cards | ~160px each |
| 720–1000px | 3 cards | ~220px each |
| ≥1000px | 4 cards | ~397px each |

**Mobile-specific CSS:**
- Reduced track padding to 40px on ≤480px
- Smaller nav buttons (32px vs 44px)
- Smaller fonts: title 13px, info 12px, badge 11px
- Nav space reduced to 60px for single-card mode

#### 7. Updated Data Source 📊
- **New Google Sheet** with **493 rekanans** (was 16)
- CSV URL updated in `scripts/generate_carousel.py`
- Parser auto-detects columns by header name (`nama`, `kota`, `instagram`, `telp`, `alamat`)

#### 8. Instagram Icon Fixed 📷
- **Bug:** Instagram row showed **phone icon** instead of camera
- **Fix:** Replaced SVG path with Instagram logo: rounded rectangle + circle + flash dot

#### 9. JS-Randomized 16 Cards Per Visit 🎲
**Problem:** 493 cards was too many for a carousel — huge file, slow, endless scrolling.

**Solution:**
- Python embeds **all 493 records as JSON array** in HTML (~60 KB)
- File size reduced from ~495 KB → ~65 KB (87% smaller)
- **Browser JS shuffles** all 493 with Fisher-Yates sort:
  ```javascript
  const shuffled = allRekanans.slice().sort(() => Math.random() - 0.5);
  const selected = shuffled.slice(0, 16);
  ```
- **Renders 16 random cards** per visit
- Every page refresh = **new 16 cards**

**Configurable:** Edit `CARDS_PER_VISIT = 16` in `generate_carousel.py`

#### 10. Bug Fixes — Autorotate & Search 🔧
**Issues reported:**
1. Autorotate function not working at all
2. Search only worked on the 16 random cards, not all 493 rekanans

**Root causes found:**
1. **`sendHeight is not defined`** ReferenceError — The `sendHeight()` function was defined in a second `<script>` block, but `renderCarousel()` was calling it before it existed. This crashed the JS before `resetAutoScroll()` could start.
2. **`filterCards()` only searched DOM elements** — It was looping through `allCards` (the 16 rendered cards) instead of searching `allRekanans` (all 493 records).

**Fixes applied:**
1. **Moved `sendHeight` script to run FIRST** — Added `window.sendHeight = sendHeight` to expose it globally before main JS runs
2. **Rewrote `filterCards(query)`** — Now filters from `allRekanans` array and re-renders carousel with matching results
3. **Changed autorotate interval** — Set to 2000ms (2 seconds per card)

**Files modified:**
- `scripts/generate_carousel.py` — Fixed script order, rewrote `filterCards()`, changed interval to 2000ms
- `outputs/carousel_dev.html` — Regenerated with fixes

**Test:** Open browser console — should see "AutoScroll tick" logs every 2 seconds. Search for a rekanan not in the initial 16 cards — it should appear.

#### 11. Search Results — Grid Layout (All Results Shown) 📦
**User request:** Search results should display ALL matching cards, not in carousel format.

**Implementation:**
- When search query entered:
  - Hide carousel nav buttons & dots
  - Change track from `flex-wrap: nowrap` (carousel) to `flex-wrap: wrap` (grid)
  - Remove padding (no need for nav space)
  - Render ALL matching cards from `allRekanans`
  - Stop autorotate completely
- When search cleared:
  - Restore carousel nav & dots
  - Change back to `flex-wrap: nowrap`
  - Restore padding for nav buttons
  - Show 16 random cards again
  - Restart autorotate

**Added `isSearchMode` flag:**
- Tracks whether user is currently searching
- Prevents mouseenter/mouseleave from triggering autorotate during search
- Ensures clean state when switching between carousel and grid modes

**Files modified:**
- `scripts/generate_carousel.py` — Updated `filterCards()`, added `isSearchMode` flag, modified mouse event handlers

## Cloudflare Pages URL

Dev (canonical, used in PageFly):
```
https://rekanan-carousel.pages.dev/carousel_dev.html
```

> Note: Both with and without `1e251801` subdomain work. PageFly uses the clean URL.

## PageFly iFrame Code (Corrected)

```html
<div id="carousel-container" style="width: 100%; min-height: 520px;">
  <iframe
    id="rekanan-iframe"
    src="https://rekanan-carousel.pages.dev/carousel_dev.html"
    style="width: 100%; height: 520px; border: none; border-radius: 12px;"
    loading="lazy"
    allowtransparency="true"
  ></iframe>
</div>

<script>
(function(){
  var container = document.getElementById('carousel-container');
  var iframe = document.getElementById('rekanan-iframe');
  window.addEventListener('message', function(e){
    if (e.origin !== 'https://rekanan-carousel.pages.dev') return;
    if (e.data && typeof e.data.height === 'number') {
      if (container) container.style.height = e.data.height + 'px';
      if (iframe) iframe.style.height = e.data.height + 'px';
    }
  });
})();
</script>
```

## Current Carousel Features

- ✅ **493 rekanans** embedded as JSON data
- ✅ **16 random cards** per visit (shuffled in browser)
- ✅ **Search** by nama rekanan or kota (searches ALL 493 rekanans, not just 16)
- ✅ **4 cards** per view on desktop (responsive: 3→2→1)
- ✅ **Consistent card height** with address at bottom
- ✅ **Auto-scroll** (2s interval), pauses on hover
- ✅ **Drag/swipe** navigation
- ✅ **Prev/Next** buttons + dot indicators
- ✅ **Auto-height iframe** — no scrollbar, parent resizes dynamically
- ✅ **Mobile-optimized** — 1 readable card at 320px
- ✅ **Instagram icon** (camera, not phone)

## Project Structure

```
/home/dev/rekanan-carousel/
├── scripts/
│   ├── generate_carousel.py         # Main generator (JS-randomized 16 from 493)
│   └── deploy.sh                    # Git push → Cloudflare deploy
├── outputs/
│   └── carousel_dev.html            # Generated HTML (~65 KB with JSON data)
├── docs/
│   ├── pagefly_searchbox_plan.md
│   ├── google_sheets_setup.md
│   ├── QUICKSTART.md
│   └── LOGGING.md
├── .gitignore
├── requirements.txt
└── CHECKPOINT.md                    # This file
```

## Deployment

```bash
# On dev1 (development & testing)
python3 scripts/generate_carousel.py   # fetches CSV, outputs carousel_dev.html
./scripts/deploy.sh                    # commits and pushes to GitHub
```

## Notes

- `carousel_*.html` is fully self-contained (CSS + JS inline).
- No server-side dependencies needed for hosting.
- **Dev vs Prod switch:** Edit line 17 in `scripts/generate_carousel.py`
  - dev1: `OUTPUT_FILE = Path("outputs") / "carousel_dev.html"`
  - dev2: `OUTPUT_FILE = Path("outputs") / "carousel_prod.html"`
- **Cards per visit:** Edit `CARDS_PER_VISIT = 16` in `scripts/generate_carousel.py`
- **Card sizing is dynamic** — JS calculates `--card-width` based on wrapper width.
- **Breakpoints:** <420px=1 card, 420-720px=2, 720-1000px=3, >1000px=4.
- **Data source:** Google Sheets CSV (auto-fetched during generation).

---

**Session Date:** May 23, 2026
**Status:** ✅ All bugs fixed — Autorotate & Search working properly
**Next:** Customer testing → Prod deployment on dev2 (when approved)
