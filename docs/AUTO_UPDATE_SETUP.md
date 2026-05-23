# Auto-Update Production from Google Sheets

## Overview

Setup cron job di server prod (dev2) untuk auto-generate `carousel_prod.html` dari Google Sheets CSV.

---

## Option 1: Daily Update (Recommended)

Update sekali sehari (misal jam 2 pagi):

### Setup di dev2 (192.168.22.234):

```bash
# SSH ke dev2
ssh dev@192.168.22.234

# Edit crontab
crontab -e

# Tambahkan line ini (update setiap hari jam 02:00):
0 2 * * * cd /home/dev/rekanan-carousel && python3 scripts/generate_carousel.py >> /var/log/carousel_update.log 2>&1

# Save & exit
```

### Verify Cron Job:

```bash
# Lihat cron yang aktif
crontab -l

# Cek cron service status
sudo systemctl status cron

# Lihat log setelah jam 2 pagi
tail -f /var/log/carousel_update.log
```

---

## Option 2: Hourly Update

Update setiap jam:

```bash
# Edit crontab
crontab -e

# Update setiap jam:
0 * * * * cd /home/dev/rekanan-carousel && python3 scripts/generate_carousel.py >> /var/log/carousel_update.log 2>&1
```

---

## Option 3: Every 6 Hours

Update 4 kali sehari:

```bash
# Edit crontab
crontab -e

# Update setiap 6 jam:
0 */6 * * * cd /home/dev/rekanan-carousel && python3 scripts/generate_carousel.py >> /var/log/carousel_update.log 2>&1
```

---

## Setup Logging & Monitoring

### 1. Create Log File

```bash
# SSH ke dev2
ssh dev@192.168.22.234

# Create log file
sudo touch /var/log/carousel_update.log
sudo chown dev:dev /var/log/carousel_update.log
```

### 2. Test Manual Run

```bash
cd /home/dev/rekanan-carousel
python3 scripts/generate_carousel.py
```

Expected output:
```
🎠 Generating Carousel Searchbox...
✅ Generated: outputs/carousel_prod.html
```

### 3. Check Log After Cron Runs

```bash
# Lihat isi log
cat /var/log/carousel_update.log

# Atau tail real-time
tail -f /var/log/carousel_update.log
```

---

## Setup Email Notifications (Optional)

Jika ingin dapat email saat ada error:

```bash
# Edit crontab
crontab -e

# Tambahkan email di atas cron job:
MAILTO=admin@example.com
0 2 * * * cd /home/dev/rekanan-carousel && python3 scripts/generate_carousel.py >> /var/log/carousel_update.log 2>&1
```

---

## Verification Checklist

Setelah setup cron:

- [ ] Cron job aktif: `crontab -l`
- [ ] Log file ada: `ls -lh /var/log/carousel_update.log`
- [ ] Test manual run berhasil
- [ ] Tunggu cron berjalan (jam 2 pagi)
- [ ] Cek log: `cat /var/log/carousel_update.log`
- [ ] Verify file terupdate: `ls -lh outputs/carousel_prod.html`
- [ ] Check timestamp file sesuai dengan waktu cron run
- [ ] Test di browser: https://rekanan-carousel.pages.dev/carousel_prod.html

---

## Troubleshooting

### Cron tidak jalan?

```bash
# Cek cron service
sudo systemctl status cron

# Restart jika perlu
sudo systemctl restart cron

# Cek cron log
grep CRON /var/log/syslog | tail -20
```

### Script tidak ter-eksekusi?

```bash
# Pastikan script executable
chmod +x /home/dev/rekanan-carousel/scripts/generate_carousel.py

# Test manual
cd /home/dev/rekanan-carousel
python3 scripts/generate_carousel.py
```

### Python tidak ditemukan?

```bash
# Cek lokasi python3
which python3

# Update cron dengan full path
# Contoh:
0 2 * * * cd /home/dev/rekanan-carousel && /usr/bin/python3 scripts/generate_carousel.py >> /var/log/carousel_update.log 2>&1
```

### Permission denied?

```bash
# Pastikan user dev punya akses
sudo chown -R dev:dev /home/dev/rekanan-carousel
```

---

## Alternative: Webhook-Based Update (Advanced)

Jika ingin update **real-time** saat Google Sheet diubah:

### 1. Setup Google Apps Script di Google Sheet

```javascript
// Di Google Sheet: Extensions → Apps Script
function onEdit(e) {
  // Trigger webhook setiap ada edit
  UrlFetchApp.fetch("https://your-webhook-url.com/update");
}
```

### 2. Buat Webhook Endpoint di dev2

```python
# scripts/webhook_server.py
from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update():
    subprocess.run(['python3', 'scripts/generate_carousel.py'])
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 3. Run sebagai Service

```bash
# Install dependencies
pip3 install flask

# Run dengan systemd
sudo nano /etc/systemd/system/carousel-webhook.service
```

```ini
[Unit]
Description=Carousel Webhook Server
After=network.target

[Service]
User=dev
WorkingDirectory=/home/dev/rekanan-carousel
ExecStart=/usr/bin/python3 /home/dev/rekanan-carousel/scripts/webhook_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable & start
sudo systemctl enable carousel-webhook
sudo systemctl start carousel-webhook
```

**Note:** Option ini lebih kompleks, gunakan Option 1 (daily cron) untuk simplicity.

---

## Recommended Setup

**Untuk production:**
- **Frequency:** Daily at 2 AM (`0 2 * * *`)
- **Log:** `/var/log/carousel_update.log`
- **Monitoring:** Check log weekly

**Rationale:**
- Google Sheets tidak berubah terlalu sering
- Daily update cukup untuk keep data fresh
- Minimal resource usage
- Easy to debug jika ada masalah

---

## Quick Setup Script

Copy-paste ini di dev2 untuk setup instan:

```bash
#!/bin/bash
# Setup auto-update cron job di dev2

# Create log file
sudo touch /var/log/carousel_update.log
sudo chown dev:dev /var/log/carousel_update.log

# Add cron job (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * cd /home/dev/rekanan-carousel && python3 scripts/generate_carousel.py >> /var/log/carousel_update.log 2>&1") | crontab -

# Verify
echo "=== Cron Job Added ==="
crontab -l

echo ""
echo "=== Test Manual Run ==="
cd /home/dev/rekanan-carousel
python3 scripts/generate_carousel.py

echo ""
echo "=== Setup Complete ==="
echo "Check log tomorrow at: /var/log/carousel_update.log"
```

---

**Setup Date:** _______________
**Frequency:** ☐ Daily ☐ Hourly ☐ Every 6 hours
**Status:** ☐ Active ☐ Pending
