# Quick Start - PageFly Searchbox

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd /home/dev/shopify
python3 -m venv --upgrade-deps shopifyvenv
source shopifyvenv/bin/activate
pip install -r requirements.txt
```

### Step 2: Start Server

```bash
python3 scripts/server.py
```

Server runs on: `http://0.0.0.0:5005`

---

### Step 3: Create Google Sheets

1. Go to [sheets.google.com](https://sheets.google.com)
2. Create new sheet with headers (row 1):
   - `nama` | `kota` | `instagram` | `telp` | `alamat`
3. Add your data (starting row 2)

Example:
| nama | kota | instagram | telp | alamat |
|------|------|-----------|------|--------|
| CV Ambon Jaya | Ambon | @ambonjaya | 0911-123456 | Jl. Sultan Hairun No. 12 |
| PT Bandung Makmur | Bandung | @bandungmakmur | 022-4567890 | Jl. Asia Afrika No. 45 |

---

### Step 4: Publish to Web (One-Time)

1. In Google Sheets: **File** → **Share** → **Publish to web**
2. Choose: **Entire Document**
3. Change format: **Web page** → **Comma-separated values (.csv)**
4. Click **Publish**
5. **Copy the URL**

Example URL:
```
https://docs.google.com/spreadsheets/d/e/2PACX-1vR.../pub?output=csv
```

---

### Step 5: Generate & Copy

1. Visit: `http://your-server-ip:5005/get-code.html`
2. Paste CSV URL in the input field
3. Click **"Update from Google Sheets"**
4. Wait for preview to load
5. Test search functionality
6. Click **"Copy HTML Code"**
7. Paste in PageFly → Custom Code element

---

## Workflow Summary

```
Edit Google Sheets
       ↓
Visit server/get-code.html
       ↓
Click "Update" button
       ↓
Preview appears
       ↓
Click "Copy HTML"
       ↓
Paste in PageFly
```

**No cron needed!** Update anytime by clicking the button.

---

## Customer Instructions

### To Update Data:

1. **Edit your Google Sheets** (add/edit/delete rows)
2. **Wait ~5 minutes** for Google to update the CSV
3. **Visit** `http://your-server-ip:5005/get-code.html`
4. **Click** "Update from Google Sheets" button
5. **Copy** the new HTML code
6. **Replace** the old code in PageFly

---

## Troubleshooting

### "No CSV URL provided"
- Enter your Google Sheets CSV URL in the input field
- Make sure URL ends with `?output=csv`

### "Failed to fetch CSV"
- Check URL is correct and published
- Test URL in browser (should download CSV file)
- Ensure Google Sheets is accessible (not restricted)

### "No data found in CSV"
- Check headers are lowercase: `nama`, `kota`, `instagram`, `telp`, `alamat`
- Ensure data starts from row 2
- No empty rows between data

### Preview not loading
- Wait for "Update" to complete
- Check server is running (`python3 scripts/server.py`)
- Check browser console for errors

---

## Server Management

### Start Server
```bash
cd /home/dev/shopify
source shopifyvenv/bin/activate
python3 scripts/server.py
```

### Run in Background (Production)
```bash
# Using nohup
nohup python3 scripts/server.py > logs/server.log 2>&1 &

# Or using systemd (create service file)
```

### Stop Server
```bash
# Find process
ps aux | grep "scripts/server.py"

# Kill process
kill <PID>
```

---

## Files

| File | Purpose |
|------|---------|
| `scripts/server.py` | Flask server + API |
| `src/get-code.html` | Customer UI (update + copy) |
| `outputs/searchbox.html` | Generated HTML |
| `data/sheet_config.json` | Saved CSV URL (auto-created) |

---

**Created:** May 7, 2026
**Version:** 2.0 (On-demand generation, no cron)
