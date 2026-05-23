# PageFly Searchbox Rekanan - Implementation Plan

## Overview
Build a searchable rekanan directory that:
- Displays company name, Instagram, phone, address, city
- Groups by city with city badge header
- Searchable by city name or company name
- Data sourced from Excel/Google Sheets
- Syncs once daily (not real-time)
- Embeds in Shopify/PageFly

---

## Current Status (Today)

### ✅ Completed
1. **HTML Searchbox UI** - `src/searchbox_allshow.html`
   - 2-column grid layout per city
   - 25 entries across 10 cities
   - Search by city or nama rekanan
   - City groups with badge headers
   - Instagram links (clickable)
   - Phone numbers
   - Address display
   - Responsive design

2. **Unique IDs** - No conflict with `src/searchbox.html`
   - `searchRekananAll` (not `searchRekanan`)
   - `list-rekanan-all` (not `list-rekanan`)
   - `filterRekananAll()` function

3. **Test Server Running**
   - Port: 5005
   - URL: `http://192.168.22.235:5005/searchbox_allshow.html`

4. **Google Sheets CSV Import** - `scripts/generate_from_csv.py`
   - Fetch from published Google Sheets CSV
   - Parse and group by city (auto-sorted)
   - Generate HTML with same structure
   - Output to `outputs/searchbox.html`

5. **Customer Preview Page** - `src/get-code.html`
   - Live preview of generated searchbox
   - Test search functionality
   - "Copy HTML Code" button (1-click)
   - "Copy iframe Code" button
   - Step-by-step PageFly instructions
   - URL: `http://192.168.22.235:5005/src/get-code.html`

### ⏳ Pending (Continue Tomorrow)

1. **Customer Setup**
   - Create Google Sheets with data
   - Publish to Web as CSV
   - Configure CSV URL in script

2. **Cron Job Setup**
   - Daily sync at 2 AM
   - `0 2 * * * cd /home/dev/shopify && . shopifyvenv/bin/activate && python3 scripts/generate_from_csv.py`

3. **PageFly Embed Testing**
   - Test copy-paste HTML method
   - Test iframe method
   - Verify on production server

---

## Excel Format Required

| Column | Header | Required | Example |
|--------|--------|----------|---------|
| A | `nama` | ✅ | CV Ambon Jaya |
| B | `kota` | ✅ | Ambon |
| C | `instagram` | ✅ | @ambonjaya |
| D | `telp` | ✅ | 0911-123456 |
| E | `alamat` | ✅ | Jl. Sultan Hairun No. 12 |

**Notes:**
- Headers in row 1
- Data starts row 2
- No empty rows between data
- Save as `.xlsx` in `/home/dev/ethrsi/data/rekanan.xlsx`

---

## Implementation - FINAL (Completed)

### Chosen: Google Sheets CSV + Server + Cron
```
Google Sheets (Customer edits)
       ↓ (Publish to Web - one-time)
Public CSV URL
       ↓ (Daily cron at 2 AM)
scripts/generate_from_csv.py
       ↓
outputs/searchbox.html (auto-generated)
       ↓
Customer visits: src/get-code.html
       ↓
Click "Copy HTML Code" → Paste in PageFly
```

**Why this approach:**
- ✅ Customer can edit Sheet anytime (add/del/modify)
- ✅ No re-publish needed (auto-updates ~5 min)
- ✅ Daily cron auto-generates HTML
- ✅ Customer preview page with 1-click copy
- ✅ No complex API authentication
- ✅ Works with existing dev1/dev2 server

---

## Next Steps (Tomorrow)

1. [ ] Customer: Create Google Sheets with actual data
2. [ ] Customer: Publish to Web as CSV
3. [ ] Configure CSV URL in `scripts/generate_from_csv.py`
4. [ ] Test: Run script manually
5. [ ] Test: Visit `src/get-code.html` and copy code
6. [ ] Test: Paste in PageFly and verify
7. [ ] Setup cron job for daily sync

---

## Files Modified/Added

### May 6, 2026
- `src/searchbox_allshow.html` - Main searchbox UI
- `docs/pagefly_searchbox_plan.md` - This plan document

### May 7, 2026
- `scripts/generate_from_csv.py` - Google Sheets CSV → HTML generator
- `src/get-code.html` - Customer preview + copy page
- `docs/google_sheets_setup.md` - Google Sheets setup guide
- `README.md` - Updated with new approach

---

## Key Decisions Made

1. **Sync Frequency:** Once daily (not real-time)
2. **Data Source:** Excel file (can export from Google Sheets)
3. **Embed Method:** iframe (to be decided: server vs Shopify CDN)
4. **Search Fields:** City + Nama Rekanan (not IG/phone/address)
5. **Display:** Grouped by city, 2 columns per city group

---

## Server Info

| Server | IP | Port | Role |
|--------|-----|------|------|
| dev1 | 192.168.22.235 | 5005 | Test/Development |
| dev2 | 192.168.22.234 | - | Production |

**Test URL:** `http://192.168.22.235:5005/searchbox_allshow.html`

---

## Notes

- Shopify/PageFly have NO native database for custom data
- Metafields not suitable for this use case (not queryable)
- Client-side search (JavaScript) is the way to go
- Keep data separate from code (Excel → Auto-generate HTML)

---

**Session Date:** May 6-7, 2026
**Status:** ✅ Implementation complete - Ready for customer testing
**Next:** Customer setup Google Sheets + test flow
