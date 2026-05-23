# Google Sheets Template - Rekanan Directory

## Google Sheets Setup

### 1. Create New Google Sheet

1. Go to [sheets.google.com](https://sheets.google.com)
2. Click "+ Blank" to create new sheet
3. Name it: "Rekanan Directory"

### 2. Setup Column Headers (Row 1)

| Cell A1 | Cell B1 | Cell C1 | Cell D1 | Cell E1 |
|---------|---------|---------|---------|---------|
| `nama` | `kota` | `instagram` | `telp` | `alamat` |

### 3. Add Sample Data (Starting Row 2)

| nama | kota | instagram | telp | alamat |
|------|------|-----------|------|--------|
| CV Ambon Jaya | Ambon | @ambonjaya | 0911-123456 | Jl. Sultan Hairun No. 12 |
| PT Nusantara Ambon | Ambon | @nusantaraambon | 0911-234567 | Jl. A.Y. Patty No. 45 |
| CV Bandung Makmur | Bandung | @bandungmakmur | 022-4567890 | Jl. Asia Afrika No. 45 |
| PT Priangan Jaya | Bandung | @prianganjaya | 022-5678901 | Jl. Braga No. 88 |

### 4. Publish to Web (One-Time Setup)

1. Click **File** → **Share** → **Publish to web**
2. In the dialog:
   - Choose: **Entire Document** (or specific sheet)
   - Change format: **Web page** → **Comma-separated values (.csv)**
3. Click **Publish**
4. Click **OK** to confirm
5. **Copy the generated URL** (save this!)

Example URL:
```
https://docs.google.com/spreadsheets/d/e/2PACX-1vR.../pub?output=csv
```

### 5. Configure Script

Edit `scripts/generate_from_csv.py`:

```python
# Line 12: Replace with your CSV URL
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/YOUR_SHEET_ID/pub?output=csv"
```

### 6. Test

```bash
cd /home/dev/shopify
source shopifyvenv/bin/activate
python3 scripts/generate_from_csv.py
```

Check output: `outputs/searchbox.html`

---

## Data Entry Guidelines

### Column Requirements

| Column | Header | Required | Format | Example |
|--------|--------|----------|--------|---------|
| A | `nama` | ✅ | Text | CV Ambon Jaya |
| B | `kota` | ✅ | Text | Ambon |
| C | `instagram` | ✅ | @username or username | @ambonjaya |
| D | `telp` | ✅ | Text | 0911-123456 |
| E | `alamat` | ✅ | Text | Jl. Sultan Hairun No. 12 |

### Tips

- ✅ **Headers must be lowercase** (nama, kota, instagram, telp, alamat)
- ✅ **No empty rows** between data
- ✅ **Instagram**: Can include @ or without (both work)
- ✅ **City names**: Will be auto-grouped and sorted alphabetically
- ✅ **Company names**: Will be sorted within each city

### Auto-Update

After publishing:
- ✅ Edit Sheet anytime (add/edit/delete rows)
- ✅ Wait ~5 minutes for Google to propagate
- ✅ Run script or wait for cron (2 AM daily)
- ✅ HTML auto-updates with new data

---

## Cron Setup (Auto Daily Sync)

```bash
# Edit crontab
crontab -e

# Add this line (daily at 2 AM)
0 2 * * * cd /home/dev/shopify && . shopifyvenv/bin/activate && python3 scripts/generate_from_csv.py
```

---

## Customer Access

After script runs, customers can:

1. **Preview & Copy**: Visit `http://192.168.22.235:5005/src/get-code.html`
2. **Test**: Search functionality works in preview
3. **Copy**: Click "Copy HTML Code" button
4. **Paste**: In PageFly → Custom Code element

---

## Troubleshooting

### "Preview tidak tersedia"
- Run script first: `python3 scripts/generate_from_csv.py`
- Check HTTP server is running: `python3 -m http.server 5005 --directory src`

### CSV not loading
- Check URL is correct (must end with `?output=csv`)
- Ensure sheet is published (File → Share → Publish to web)
- Test URL in browser (should download CSV file)

### Wrong data format
- Check headers are lowercase: `nama`, `kota`, `instagram`, `telp`, `alamat`
- No empty rows in middle of data
- Save changes in Google Sheet (auto-saves, but wait 1-2 min)

---

**Created:** May 7, 2026
**Version:** 1.0
