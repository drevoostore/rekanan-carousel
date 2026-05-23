# Deploy to Production Server (dev2)

## Server Info

| Server | IP | Role |
|--------|-----|------|
| dev1 | 192.168.22.235 | Development & Testing |
| dev2 | 192.168.22.234 | **Production** |

---

## Option 1: Deploy via SSH (Recommended)

### Step 1: SSH to dev2
```bash
ssh root@192.168.22.234
# atau
ssh dev2  # jika sudah ada SSH config
```

### Step 2: Clone/Pull Repository
```bash
cd /home/dev
# Jika belum ada:
git clone https://github.com/drevoostore/rekanan-carousel.git
cd rekanan-carousel

# Jika sudah ada:
cd /home/dev/rekanan-carousel
git pull origin main
```

### Step 3: Verify Production Config
Edit `scripts/generate_carousel.py` line 17:
```python
OUTPUT_FILE = Path("outputs") / "carousel_prod.html"  # ✅ Production
```

### Step 4: Generate Production HTML
```bash
python3 scripts/generate_carousel.py
```

Expected output:
```
✅ Generated: outputs/carousel_prod.html
Total rekanans embedded: 493
```

### Step 5: Verify Output
```bash
ls -lh outputs/carousel_prod.html
# Should be ~65 KB
```

### Step 6: Test Locally on dev2
Open browser on dev2:
```
file:///home/dev/rekanan-carousel/outputs/carousel_prod.html
```

Or serve with Python:
```bash
cd /home/dev/rekanan-carousel
python3 -m http.server 8080
# Open: http://localhost:8080/outputs/carousel_prod.html
```

### Step 7: Upload to Cloudflare (if not using Git auto-deploy)
If Cloudflare Pages is connected to GitHub:
```bash
git add outputs/carousel_prod.html
git commit -m "prod: deploy carousel_prod.html"
git push origin main
```

Then wait for Cloudflare auto-deploy (~1-2 min).

---

## Option 2: Copy Files from dev1 to dev2

### On dev1 (this server):
```bash
# Create production archive
cd /home/dev/rekanan-carousel
tar -czf /tmp/rekanan-carousel-prod.tar.gz \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  .

# Copy to dev2 (requires SSH access)
scp /tmp/rekanan-carousel-prod.tar.gz root@192.168.22.234:/tmp/
```

### On dev2:
```bash
# Extract
cd /home/dev
mkdir -p rekanan-carousel
tar -xzf /tmp/rekanan-carousel-prod.tar.gz -C rekanan-carousel/
cd rekanan-carousel

# Generate production HTML
python3 scripts/generate_carousel.py

# Verify
ls -lh outputs/carousel_prod.html
```

---

## Option 3: Direct Cloudflare Upload (No Server)

If you don't need dev2 for anything else:

1. Download `carousel_prod.html` from dev1:
   ```bash
   scp root@192.168.22.235:/home/dev/rekanan-carousel/outputs/carousel_prod.html /tmp/
   ```

2. Upload directly to Cloudflare Pages:
   - Go to Cloudflare Dashboard → Pages
   - Select project → Create deployment
   - Upload `carousel_prod.html` directly

---

## Post-Deployment Verification

### 1. Check Cloudflare Deployment
```
https://rekanan-carousel.pages.dev/carousel_prod.html
```

### 2. Test Features
- [ ] Carousel shows 16 random cards
- [ ] Autorotate every 2 seconds
- [ ] Search displays all results in grid
- [ ] No autorotate during search
- [ ] Mobile responsive works
- [ ] No console errors

### 3. Update PageFly (Production)
Edit PageFly iframe:
```html
<iframe 
  src="https://rekanan-carousel.pages.dev/carousel_prod.html"
  style="width: 100%; height: 520px; border: none; border-radius: 12px;"
  id="rekanan-iframe"
></iframe>
```

---

## Rollback (If Issues)

### Quick Rollback to Dev URL
Change PageFly iframe back to dev:
```html
<iframe src="https://rekanan-carousel.pages.dev/carousel_dev.html" ...>
```

### Restore Previous Production
On dev2:
```bash
cd /home/dev/rekanan-carousel
git log --oneline -10
git checkout <previous-commit> -- outputs/carousel_prod.html
python3 scripts/generate_carousel.py
git add outputs/carousel_prod.html
git commit -m "rollback: restore previous version"
git push
```

---

## Production Checklist

Before marking deployment complete:

- [ ] Files deployed to dev2
- [ ] `carousel_prod.html` generated successfully
- [ ] Cloudflare Pages deployment complete
- [ ] Production URL accessible
- [ ] All features tested (carousel, search, autorotate)
- [ ] Mobile responsive verified
- [ ] PageFly iframe updated
- [ ] No console errors
- [ ] Customer notified

---

**Deployment Date:** _______________
**Deployed To:** dev2 (192.168.22.234)
**Deployed By:** _______________
**Status:** ☐ Success ☐ Issues

**Notes:**
_______________________________________________
